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


const fs = require('fs');

class BellandeFormat {
  parseBellande(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const parsedData = this.parseLines(lines);
    return this.toStringRepresentation(parsedData);
  }

  parseLines(lines) {
    const result = {};
    let currentKey = null;
    let currentList = null;
    const indentStack = [[-1, result]];

    for (const line of lines) {
      const stripped = line.trim();
      if (!stripped || stripped.startsWith('#')) continue;

      const indent = line.length - line.trimLeft().length;

      while (indentStack.length && indent <= indentStack[indentStack.length - 1][0]) {
        const popped = indentStack.pop();
        if (Array.isArray(popped[1])) {
          currentList = null;
        }
      }

      if (stripped.includes(':')) {
        const [key, value] = stripped.split(':').map(s => s.trim());
        currentKey = key;
        if (value) {
          result[key] = this.parseValue(value);
        } else {
          result[key] = [];
          currentList = result[key];
          indentStack.push([indent, currentList]);
        }
      } else if (stripped.startsWith('-')) {
        const value = stripped.slice(1).trim();
        const parsedValue = this.parseValue(value);
        if (currentList !== null) {
          currentList.push(parsedValue);
        } else {
          if (Object.keys(result).length === 0) {
            result = [parsedValue];
            currentList = result;
            indentStack = [[-1, result]];
          } else {
            result[currentKey] = [parsedValue];
            currentList = result[currentKey];
            indentStack.push([indent, currentList]);
          }
        }
      }
    }

    return result;
  }

  parseValue(value) {
    if (value.toLowerCase() === 'true') return true;
    if (value.toLowerCase() === 'false') return false;
    if (value.toLowerCase() === 'null') return null;
    if (value.startsWith('"') && value.endsWith('"')) return value.slice(1, -1);
    if (/^-?\d+$/.test(value)) return parseInt(value, 10);
    if (/^-?\d*\.\d+$/.test(value)) return parseFloat(value);
    return value;
  }

  toStringRepresentation(data) {
    if (typeof data === 'object' && data !== null) {
      if (Array.isArray(data)) {
        const items = data.map(item => this.toStringRepresentation(item));
        return '[' + items.join(', ') + ']';
      } else {
        const items = Object.entries(data).map(([k, v]) => `"${k}": ${this.toStringRepresentation(v)}`);
        return '{' + items.join(', ') + '}';
      }
    } else if (typeof data === 'string') {
      return `"${data}"`;
    } else if (typeof data === 'number') {
      return data.toString();
    } else if (data === null) {
      return 'null';
    } else if (typeof data === 'boolean') {
      return data.toString().toLowerCase();
    } else {
      return String(data);
    }
  }

  writeBellande(data, filePath) {
    fs.writeFileSync(filePath, this.toBellandeString(data));
  }

  toBellandeString(data, indent = 0) {
    if (typeof data === 'object' && data !== null) {
      if (Array.isArray(data)) {
        return data.map(item => `${' '.repeat(indent)}- ${this.toBellandeString(item, indent + 2)}`).join('\n');
      } else {
        return Object.entries(data)
          .map(([key, value]) => {
            if (typeof value === 'object' && value !== null) {
              return `${' '.repeat(indent)}${key}:\n${this.toBellandeString(value, indent + 2)}`;
            } else {
              return `${' '.repeat(indent)}${key}: ${this.formatValue(value)}`;
            }
          })
          .join('\n');
      }
    } else {
      return this.formatValue(data);
    }
  }

  formatValue(value) {
    if (typeof value === 'string') {
      if (value.includes(' ') || value.includes(':') || ['true', 'false', 'null'].includes(value.toLowerCase())) {
        return `"${value}"`;
      }
      return value;
    }
    if (typeof value === 'boolean') {
      return value.toString().toLowerCase();
    }
    if (value === null) {
      return 'null';
    }
    return String(value);
  }
}

module.exports = BellandeFormat;
