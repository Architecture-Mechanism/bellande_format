const fs = require('fs');

class BellandeFormat {
  parseBellande(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    return this.parseLines(lines);
  }

  parseLines(lines) {
    const result = {};
    const stack = [[-1, result]];

    for (const line of lines) {
      const stripped = line.trim();
      if (!stripped || stripped.startsWith('#')) continue;

      const indent = line.length - line.trimLeft().length;
      while (stack.length && indent <= stack[stack.length - 1][0]) {
        stack.pop();
      }

      const parent = stack[stack.length - 1][1];

      if (stripped.includes(':')) {
        const [key, value] = stripped.split(':').map(s => s.trim());
        if (value) {
          parent[key] = this.parseValue(value);
        } else {
          const newDict = {};
          parent[key] = newDict;
          stack.push([indent, newDict]);
        }
      } else if (stripped.startsWith('-')) {
        const value = stripped.slice(1).trim();
        if (Array.isArray(parent)) {
          parent.push(this.parseValue(value));
        } else {
          const newList = [this.parseValue(value)];
          const lastKey = Object.keys(parent).pop();
          parent[lastKey] = newList;
          stack.push([indent, newList]);
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

  writeBellande(data, filePath) {
    const content = this.toBellandeString(data);
    fs.writeFileSync(filePath, content);
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
      return value.includes(' ') || value.includes(':') ? `"${value}"` : value;
    }
    if (typeof value === 'boolean') {
      return value.toString();
    }
    if (value === null) {
      return 'null';
    }
    return value.toString();
  }
}
