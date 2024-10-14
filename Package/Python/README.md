# Bellande Format Python Example

```
from bellande_format import Bellande_Format

bellande_formatter = Bellande_Format()

# Parse a Bellande file
parsed_data = bellande_formatter.parse_bellande("path/to/your/file.bellande")

# Write data to a Bellande file
data_to_write = {"key": "value", "list": [1, 2, 3]}
bellande_formatter.write_bellande(data_to_write, "path/to/output/file.bellande")
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
