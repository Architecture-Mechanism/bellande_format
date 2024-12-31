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

from typing import Dict, Any, List
import re
from datetime import datetime
from decimal import Decimal
from .types import SchemaDefinition, ValidationResult

class Validator:
    def __init__(self):
        self.type_validators = {
            'string': self._validate_string,
            'number': self._validate_number,
            'integer': self._validate_integer,
            'boolean': self._validate_boolean,
            'array': self._validate_array,
            'object': self._validate_object,
            'null': self._validate_null
        }

    def validate(self, data: Any, schema: SchemaDefinition, path: str = "") -> ValidationResult:
        if schema.type not in self.type_validators:
            return ValidationResult(False, [f"Unknown type: {schema.type}"], [])
            
        return self.type_validators[schema.type](data, schema, path)

    def _validate_string(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, str):
            return ValidationResult(False, [f"{path}: Expected string, got {type(data).__name__}"], [])
            
        errors = []
        if schema.pattern and not re.match(schema.pattern, data):
            errors.append(f"{path}: String does not match pattern {schema.pattern}")
            
        if schema.enum and data not in schema.enum:
            errors.append(f"{path}: Value not in enum: {schema.enum}")
            
        return ValidationResult(not errors, errors, [])

    def _validate_number(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, (int, float, Decimal)):
            return ValidationResult(False, [f"{path}: Expected number, got {type(data).__name__}"], [])
            
        errors = []
        if schema.minimum is not None and data < schema.minimum:
            errors.append(f"{path}: Value below minimum: {schema.minimum}")
            
        if schema.maximum is not None and data > schema.maximum:
            errors.append(f"{path}: Value above maximum: {schema.maximum}")
            
        return ValidationResult(not errors, errors, [])

    def _validate_integer(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, int):
            return ValidationResult(False, [f"{path}: Expected integer, got {type(data).__name__}"], [])
        return self._validate_number(data, schema, path)

    def _validate_boolean(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, bool):
            return ValidationResult(False, [f"{path}: Expected boolean, got {type(data).__name__}"], [])
        return ValidationResult(True, [], [])

    def _validate_array(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, list):
            return ValidationResult(False, [f"{path}: Expected array, got {type(data).__name__}"], [])
            
        errors = []
        for i, item in enumerate(data):
            item_path = f"{path}[{i}]"
            if 'items' in schema.properties:
                result = self.validate(item, schema.properties['items'], item_path)
                errors.extend(result.errors)
                
        return ValidationResult(not errors, errors, [])

    def _validate_object(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if not isinstance(data, dict):
            return ValidationResult(False, [f"{path}: Expected object, got {type(data).__name__}"], [])
            
        errors = []
        for required in schema.required:
            if required not in data:
                errors.append(f"{path}: Missing required field: {required}")
                
        for key, value in data.items():
            if key in schema.properties:
                prop_schema = schema.properties[key]
                result = self.validate(value, prop_schema, f"{path}.{key}")
                errors.extend(result.errors)
                
        return ValidationResult(not errors, errors, [])

    def _validate_null(self, data: Any, schema: SchemaDefinition, path: str) -> ValidationResult:
        if data is not None:
            return ValidationResult(False, [f"{path}: Expected null, got {type(data).__name__}"], [])
        return ValidationResult(True, [], [])
