# Copyright (C) 2024 Bellande Algorithm Model Research Innovation Center, Ronaldson Bellande

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

import re
from typing import Dict, List, Union, Any

class bellande_format:
    def parse_bellande(self, file_path: str) -> Dict:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return self.parse_lines(lines)

    def parse_lines(self, lines: List[str]) -> Dict:
        result = {}
        stack = [(-1, result)]
    
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
        
            indent = len(line) - len(line.lstrip())
            while stack and indent <= stack[-1][0]:
                stack.pop()
        
            parent = stack[-1][1]
        
            if ':' in stripped:
                key, value = map(str.strip, stripped.split(':', 1))
                if value:
                    parent[key] = self.parse_value(value)
                else:
                    new_dict = {}
                    parent[key] = new_dict
                    stack.append((indent, new_dict))
            elif stripped.startswith('-'):
                value = stripped[1:].strip()
                
                if isinstance(parent, list):
                    parent.append(self.parse_value(value))
                else:
                    new_list = [self.parse_value(value)]
                    last_key = list(parent.keys())[-1]
                    parent[last_key] = new_list
                    stack.append((indent, new_list))
    
        return result

    def parse_value(self, value: str) -> Union[str, int, float, bool, None]:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'null':
            return None
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif re.match(r'^-?\d+$', value):
            return int(value)
        elif re.match(r'^-?\d*\.\d+$', value):
            return float(value)
        else:
            return value

    def write_bellande(self, data: Any, file_path: str):
        with open(file_path, 'w') as file:
            file.write(self.to_bellande_string(data))

    def to_bellande_string(self, data: Any, indent: int = 0) -> str:
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{' ' * indent}{key}:")
                    lines.append(self.to_bellande_string(value, indent + 4))
                else:
                    lines.append(f"{' ' * indent}{key}: {self.format_value(value)}")
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = []
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(f"{' ' * indent}-")
                    lines.append(self.to_bellande_string(item, indent + 4))
                else:
                    lines.append(f"{' ' * indent}- {self.format_value(item)}")
            return '\n'.join(lines)
        else:
            return f"{' ' * indent}{self.format_value(data)}"

    def format_value(self, value: Any) -> str:
        if isinstance(value, str):
            if ' ' in value or ':' in value:
                return f'"{value}"'
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return 'null'
        else:
            return str(value)
