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

from typing import Dict, Any, Callable, Type
import re
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import base64
import struct

class CustomTypeRegistry:
    def __init__(self):
        self.types: Dict[str, Type] = {}
        self.serializers: Dict[str, Callable] = {}
        self.deserializers: Dict[str, Callable] = {}

    def register(self, type_name: str, type_class: Type, 
                serializer: Callable, deserializer: Callable):
        self.types[type_name] = type_class
        self.serializers[type_name] = serializer
        self.deserializers[type_name] = deserializer

class Complex:
    def __init__(self):
        self.pattern = re.compile(r'([-+]?\d*\.?\d*)([-+]\d*\.?\d*)j')
    
    def serialize(self, value: complex) -> str:
        return f"{value.real}{'+' if value.imag >= 0 else ''}{value.imag}j"
    
    def deserialize(self, value: str) -> complex:
        match = self.pattern.match(value)
        if not match:
            raise ValueError("Invalid complex number format")
        real = float(match.group(1))
        imag = float(match.group(2))
        return complex(real, imag)

class BinaryData:
    def serialize(self, value: bytes) -> str:
        return base64.b64encode(value).decode()
    
    def deserialize(self, value: str) -> bytes:
        return base64.b64decode(value)

class DateTime:
    def serialize(self, value: datetime) -> str:
        return value.isoformat()
    
    def deserialize(self, value: str) -> datetime:
        return datetime.fromisoformat(value)

class TimeDelta:
    def serialize(self, value: timedelta) -> str:
        return str(value.total_seconds())
    
    def deserialize(self, value: str) -> timedelta:
        return timedelta(seconds=float(value))
