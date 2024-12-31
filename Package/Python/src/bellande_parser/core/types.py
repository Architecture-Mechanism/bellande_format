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

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    path: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VersionInfo:
    version: int
    timestamp: datetime
    author: str
    changes: Dict[str, Any]
    checksum: str

@dataclass
class SchemaDefinition:
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    pattern: Optional[str] = None
    enum: Optional[List[Any]] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    format: Optional[str] = None

class BellandeValue:
    def __init__(self, value: Any, metadata: Dict = None):
        self.value = value
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.modified_at = self.created_at
        self.version = 1
        self.checksum = self._calculate_checksum()
        self.history: List[VersionInfo] = []

    def _calculate_checksum(self) -> str:
        return hashlib.sha256(str(self.value).encode()).hexdigest()

    def update(self, new_value: Any, author: str):
        old_value = self.value
        self.value = new_value
        self.modified_at = datetime.now()
        self.version += 1
        new_checksum = self._calculate_checksum()
        
        version_info = VersionInfo(
            version=self.version,
            timestamp=self.modified_at,
            author=author,
            changes={"old": old_value, "new": new_value},
            checksum=new_checksum
        )
        self.history.append(version_info)
        self.checksum = new_checksum
