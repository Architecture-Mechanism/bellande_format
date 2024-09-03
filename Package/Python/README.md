# Bellande Format Example

```
bellande_formatter = Bellande_Format()

# Parse a Bellande file
parsed_data = bellande_formatter.parse_bellande("path/to/your/file.bellande")

# Write data to a Bellande file
data_to_write = {"key": "value", "list": [1, 2, 3]}
bellande_formatter.write_bellande(data_to_write, "path/to/output/file.bellande")
```
