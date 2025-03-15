# Copyright (C) 2024 Bellande Architecture Mechanism Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

from typing import Dict, List, Any, Union
from .core.types import ValidationResult, SchemaDefinition
from .core.encryption import Encryption
from .core.compression import Compression
from .core.custom_types import CustomTypeRegistry
from .core.validation import Validator
import re
import json

class Bellande_Format:
    def __init__(self):
        self.encryption = Encryption()
        self.compression = Compression()
        self.type_registry = CustomTypeRegistry()
        self.validator = Validator()
        self.references: Dict[str, Any] = {}
        self.schemas: Dict[str, SchemaDefinition] = {}

    def register_schema(self, name: str, schema: SchemaDefinition):
        self.schemas[name] = schema

    def validate(self, data: Any, schema_name: str) -> ValidationResult:
        if schema_name not in self.schemas:
            raise ValueError(f"Schema {schema_name} not found")
        return self.validator.validate(data, self.schemas[schema_name])

    def parse_bellande(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return self.parse_content(content)

    def parse_content(self, content: str) -> Any:
        lines = content.split('\n')
        return self.parse_lines(lines)

    def parse_lines(self, lines: List[str]) -> Union[Dict, List]:
        result = {}
        current_key = None
        current_list = None
        indent_stack = [(-1, result)]

        for line_num, line in enumerate(lines, 1):
            try:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue

                indent = len(line) - len(line.lstrip())

                while indent_stack and indent <= indent_stack[-1][0]:
                    popped = indent_stack.pop()
                    if isinstance(popped[1], list):
                        current_list = None

                if ':' in stripped:
                    key, value = map(str.strip, stripped.split(':', 1))
                    current_key = key
                    if value:
                        result[key] = self._process_value(value)
                    else:
                        result[key] = []
                        current_list = result[key]
                        indent_stack.append((indent, current_list))
                elif stripped.startswith('-'):
                    value = stripped[1:].strip()
                    parsed_value = self._process_value(value)
                    if current_list is not None:
                        current_list.append(parsed_value)
                    else:
                        if not result:
                            result = [parsed_value]
                            current_list = result
                            indent_stack = [(-1, result)]
                        else:
                            result[current_key] = [parsed_value]
                            current_list = result[current_key]
                            indent_stack.append((indent, current_list))

            except Exception as e:
                raise ValueError(f"Error parsing line {line_num}: {str(e)}")

        return result

    def _process_value(self, value: str) -> Any:
        # Process custom types
        for type_name, deserializer in self.type_registry.deserializers.items():
            if value.startswith(f"type:{type_name}:"):
                type_value = value[len(f"type:{type_name}:"):]
                return deserializer(type_value)

        # Process standard types
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'null':
            return None
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif value.startswith('ref:'):
            ref_key = value[4:].strip()
            if ref_key not in self.references:
                raise ValueError(f"Reference not found: {ref_key}")
            return self.references[ref_key]
        elif re.match(r'^-?\d+$', value):
            return int(value)
        elif re.match(r'^-?\d*\.\d+$', value):
            return float(value)
        
        return value

    def write_bellande(self, data: Any, file_path: str):
        content = self.to_bellande_string(data)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def to_bellande_string(self, data: Any, indent: int = 0) -> str:
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{' ' * indent}{key}:")
                    lines.append(self.to_bellande_string(value, indent + 2))
                else:
                    lines.append(f"{' ' * indent}{key}: {self._format_value(value)}")
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = []
            for item in data:
                if isinstance(item, dict):
                    dict_lines = self.to_bellande_string(item, indent + 2).split('\n')
                    lines.append(f"{' ' * indent}- {dict_lines[0]}")
                    lines.extend(dict_lines[1:])
                else:
                    lines.append(f"{' ' * indent}- {self._format_value(item)}")
            return '\n'.join(lines)
        else:
            return f"{' ' * indent}{self._format_value(data)}"

    def _format_value(self, value: Any) -> str:
        # Format custom types
        for type_name, serializer in self.type_registry.serializers.items():
            try:
                if isinstance(value, self.type_registry.types[type_name]):
                    return f"type:{type_name}:{serializer(value)}"
            except:
                continue

        # Format standard types
        if isinstance(value, str):
            if ' ' in value or ':' in value or value.lower() in ['true', 'false', 'null']:
                return f'"{value}"'
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return 'null'
        
        return str(value)

    def encrypt(self, data: Any, key: bytes) -> bytes:
        content = self.to_bellande_string(data)
        return self.encryption.encrypt(content.encode(), key)

    def decrypt(self, encrypted_data: bytes, key: bytes) -> Any:
        decrypted = self.encryption.decrypt(encrypted_data, key)
        return self.parse_content(decrypted.decode())

    def compress(self, data: Any) -> bytes:
        content = self.to_bellande_string(data)
        return self.compression.encode_data(content.encode())[0]

    def decompress(self, compressed_data: bytes) -> Any:
        decompressed = self.compression.decode_data(compressed_data, {})
        return self.parse_content(decompressed.decode())

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: bellande_format <command> [<file_path>] [<input_data>]")
        return 1

    formatter = Bellande_Format()
    command = sys.argv[1]

    try:
        if command == 'parse':
            if len(sys.argv) < 3:
                print("Error: Please provide a file path to parse.")
                return 1
            result = formatter.parse_bellande(sys.argv[2])
            print(json.dumps(result, default=str))
            return 0

        elif command == 'write':
            if len(sys.argv) < 4:
                print("Error: Please provide a file path and input data.")
                return 1
            data = json.loads(sys.argv[3])
            formatter.write_bellande(data, sys.argv[2])
            print(f"Data written to {sys.argv[2]}")
            return 0

        else:
            print(f"Unknown command: {command}")
            return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
