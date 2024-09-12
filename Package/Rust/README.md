# Bellande Format Rust Example

```
use std::collections::HashMap;
use bellande::{BellandeFormat, BellandeValue};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create a BellandeFormat instance
    let bellande_formatter = BellandeFormat;

    // Parse a Bellande file
    let parsed_data = bellande_formatter.parse_bellande("path/to/your/file.bellande")?;
    println!("{:#?}", parsed_data);

    // Create data to write
    let mut data_to_write = HashMap::new();
    data_to_write.insert("key".to_string(), BellandeValue::String("value".to_string()));
    data_to_write.insert("list".to_string(), BellandeValue::List(vec![
        BellandeValue::Integer(1),
        BellandeValue::Integer(2),
        BellandeValue::Integer(3),
    ]));
    let bellande_value = BellandeValue::Map(data_to_write);

    // Write data to a Bellande file
    bellande_formatter.write_bellande(&bellande_value, "path/to/output/file.bellande")?;

    Ok(())
}
```

## Website NPM
- https://crates.io/crates/bellande_format

### Installation
- `cargo add bellande_format`


```
Name: bellande_format
Version: 0.1.0
Summary: File type Formats
Home-page: github.com/RonaldsonBellande/bellande_format
Author: Ronaldson Bellande
Author-email: ronaldsonbellande@gmail.com
License: GNU General Public License v3.0
```

## License
This Algorithm or Models is distributed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/), see [LICENSE](https://github.com/RonaldsonBellande/bellande_format/blob/main/LICENSE) and [NOTICE](https://github.com/RonaldsonBellande/bellande_format/blob/main/LICENSE) for more information.
