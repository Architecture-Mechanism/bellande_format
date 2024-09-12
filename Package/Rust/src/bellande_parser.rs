// Copyright (C) 2024 Bellande Algorithm Model Research Innovation Center, Ronaldson Bellande

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone)]
enum BellandeValue {
    String(String),
    Integer(i64),
    Float(f64),
    Boolean(bool),
    Null,
    List(Vec<BellandeValue>),
    Map(HashMap<String, BellandeValue>),
}

struct BellandeFormat;

impl BellandeFormat {
    pub fn parse_bellande<P: AsRef<Path>>(
        &self,
        file_path: P,
    ) -> Result<BellandeValue, std::io::Error> {
        let content = fs::read_to_string(file_path)?;
        let lines: Vec<&str> = content.lines().collect();
        let parsed_data = self.parse_lines(&lines);
        Ok(parsed_data)
    }

    fn parse_lines(&self, lines: &[&str]) -> BellandeValue {
        let mut result = HashMap::new();
        let mut current_key = String::new();
        let mut current_list: Option<Vec<BellandeValue>> = None;
        let mut indent_stack = vec![(0, &mut result)];

        for line in lines {
            let stripped = line.trim();
            if stripped.is_empty() || stripped.starts_with('#') {
                continue;
            }

            let indent = line.len() - line.trim_start().len();

            while indent_stack.last().map_or(false, |&(i, _)| indent <= i) {
                indent_stack.pop();
                current_list = None;
            }

            if let Some(colon_pos) = stripped.find(':') {
                let (key, value) = stripped.split_at(colon_pos);
                let key = key.trim().to_string();
                let value = value[1..].trim();

                current_key = key.clone();
                if !value.is_empty() {
                    let parsed_value = self.parse_value(value);
                    indent_stack.last_mut().unwrap().1.insert(key, parsed_value);
                } else {
                    let new_list = Vec::new();
                    indent_stack
                        .last_mut()
                        .unwrap()
                        .1
                        .insert(key, BellandeValue::List(new_list));
                    if let BellandeValue::List(list) = indent_stack
                        .last_mut()
                        .unwrap()
                        .1
                        .get_mut(&current_key)
                        .unwrap()
                    {
                        current_list = Some(list);
                        indent_stack.push((indent, list));
                    }
                }
            } else if stripped.starts_with('-') {
                let value = stripped[1..].trim();
                let parsed_value = self.parse_value(value);
                if let Some(list) = &mut current_list {
                    list.push(parsed_value);
                } else {
                    let mut new_list = Vec::new();
                    new_list.push(parsed_value);
                    indent_stack
                        .last_mut()
                        .unwrap()
                        .1
                        .insert(current_key.clone(), BellandeValue::List(new_list));
                    if let BellandeValue::List(list) = indent_stack
                        .last_mut()
                        .unwrap()
                        .1
                        .get_mut(&current_key)
                        .unwrap()
                    {
                        current_list = Some(list);
                        indent_stack.push((indent, list));
                    }
                }
            }
        }

        BellandeValue::Map(result)
    }

    fn parse_value(&self, value: &str) -> BellandeValue {
        if value.eq_ignore_ascii_case("true") {
            BellandeValue::Boolean(true)
        } else if value.eq_ignore_ascii_case("false") {
            BellandeValue::Boolean(false)
        } else if value.eq_ignore_ascii_case("null") {
            BellandeValue::Null
        } else if value.starts_with('"') && value.ends_with('"') {
            BellandeValue::String(value[1..value.len() - 1].to_string())
        } else if let Ok(int_value) = value.parse::<i64>() {
            BellandeValue::Integer(int_value)
        } else if let Ok(float_value) = value.parse::<f64>() {
            BellandeValue::Float(float_value)
        } else {
            BellandeValue::String(value.to_string())
        }
    }

    pub fn write_bellande<P: AsRef<Path>>(
        &self,
        data: &BellandeValue,
        file_path: P,
    ) -> Result<(), std::io::Error> {
        let content = self.to_bellande_string(data, 0);
        fs::write(file_path, content)
    }

    fn to_bellande_string(&self, data: &BellandeValue, indent: usize) -> String {
        match data {
            BellandeValue::Map(map) => map
                .iter()
                .map(|(key, value)| {
                    let value_str = match value {
                        BellandeValue::Map(_) | BellandeValue::List(_) => {
                            format!("\n{}", self.to_bellande_string(value, indent + 2))
                        }
                        _ => format!(" {}", self.format_value(value)),
                    };
                    format!("{}{}: {}", " ".repeat(indent), key, value_str)
                })
                .collect::<Vec<_>>()
                .join("\n"),
            BellandeValue::List(list) => list
                .iter()
                .map(|item| {
                    format!(
                        "{}- {}",
                        " ".repeat(indent),
                        self.to_bellande_string(item, indent + 2)
                    )
                })
                .collect::<Vec<_>>()
                .join("\n"),
            _ => self.format_value(data),
        }
    }

    fn format_value(&self, value: &BellandeValue) -> String {
        match value {
            BellandeValue::String(s) => {
                if s.contains(' ')
                    || s.contains(':')
                    || ["true", "false", "null"].contains(&s.to_lowercase().as_str())
                {
                    format!("\"{}\"", s)
                } else {
                    s.clone()
                }
            }
            BellandeValue::Integer(i) => i.to_string(),
            BellandeValue::Float(f) => f.to_string(),
            BellandeValue::Boolean(b) => b.to_string().to_lowercase(),
            BellandeValue::Null => "null".to_string(),
            BellandeValue::List(_) | BellandeValue::Map(_) => unreachable!(),
        }
    }
}
