# Bellande Format Python Example

```
from bellande_format import Bellande_Format
from core.types import SchemaDefinition
from datetime import datetime
import os

# Initialize formatter
formatter = Bellande_Format()

# Example 1: Basic Usage
data = {
    "name": "Project X",
    "version": 1.0,
    "created_at": datetime.now(),
    "settings": {
        "debug": True,
        "max_retries": 3
    },
    "users": [
        {"name": "John", "role": "admin"},
        {"name": "Jane", "role": "user"}
    ]
}

# Write data
formatter.write_bellande(data, "config.bellande")

# Read data
loaded_data = formatter.parse_bellande("config.bellande")

# Example 2: Schema Validation
user_schema = SchemaDefinition(
    type="object",
    properties={
        "name": SchemaDefinition(type="string", pattern=r"^[a-zA-Z\s]+$"),
        "age": SchemaDefinition(type="integer", minimum=0, maximum=150),
        "email": SchemaDefinition(type="string", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    },
    required=["name", "email"]
)

formatter.register_schema("user", user_schema)

# Validate data
user_data = {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
}

result = formatter.validate(user_data, "user")
print(f"Validation result: {result.is_valid}")

# Example 3: Encryption and Compression
key = os.urandom(32)  # Generate encryption key

# Encrypt data
encrypted = formatter.encrypt(data, key)

# Decrypt data
decrypted_data = formatter.decrypt(encrypted, key)

# Compress data
compressed = formatter.compress(data)

# Decompress data
decompressed_data = formatter.decompress(compressed)

# Example 4: Custom Types
class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Register custom type
formatter.type_registry.register(
    "point2d",
    Point2D,
    lambda p: f"{p.x},{p.y}",
    lambda s: Point2D(*map(float, s.split(',')))
)

# Use custom type
location_data = {
    "points": [
        Point2D(1.0, 2.0),
        Point2D(3.0, 4.0)
    ]
}

formatter.write_bellande(location_data, "locations.bellande")
```

## Website PYPI
- https://pypi.org/project/bellande_format

### Installation
- `$ pip install bellande_format`

### Upgrade (if not upgraded)
- `$ pip install --upgrade bellande_format`

```
Name: bellande_format
Summary: File type Formats
Home-page: github.com/RonaldsonBellande/bellande_format
Author: Ronaldson Bellande
Author-email: ronaldsonbellande@gmail.com
License: GNU General Public License v3.0
```

## License
This Algorithm or Models is distributed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/), see [LICENSE](https://github.com/RonaldsonBellande/bellande_format/blob/main/LICENSE) and [NOTICE](https://github.com/RonaldsonBellande/bellande_format/blob/main/LICENSE) for more information.
