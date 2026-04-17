SnipTeX is a Python package for extracting tagged code snippets from local files or remote URLs (e.g. GitHub raw files). It serves as the backend for the SnipTeX LaTeX package, enabling dynamic inclusion of code snippets directly in documents.

<div align="center">
  <a href="https://github.com/brozrost/sniptex/actions">
    <img src="https://github.com/brozrost/sniptex/actions/workflows/python-package.yml/badge.svg">
  </a>
  <a href="https://github.com/brozrost/sniptex/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/brozrost/sniptex">
  </a>
  <a href="https://github.com/brozrost/sniptex/issues">
    <img src="https://img.shields.io/github/issues/brozrost/sniptex">
  </a>
  <a href="https://github.com/brozrost/sniptex/pulls">
    <img src="https://img.shields.io/github/issues-pr/brozrost/sniptex">
  </a>
</div>

## Quick example

### Source file

```python
# sniptex-start demo
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# sniptex-end demo

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### CLI usage

```bash
sniptex --help
```

#### Write the snippet to stdout:

```bash    
sniptex -s example.py -t demo
```

#### Write the snippet to a file:
```bash  
sniptex -s example.py -t demo -o out/out.txt
```

#### Get snippet from URL:
```bash
sniptex -s https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example.py -t demo
```


### Python usage

```python
from sniptex import extractor

snippet = extractor.extract_from_file("example.py", "demo")
```

## Tag format

SnipTeX extracts code between two matching markers:

```bash
sniptex-start <tag>
...
sniptex-end <tag>
```

Tags are case-sensitive and markers must appear on separate lines.

## Supported sources

+ Local file paths
+ Remote URLs (e.g. GitHub raw files)

## Error handling

SnipTeX raises errors when:

+ the tag is not found
+ start/end markers are mismatched
+ multiple start markers exist
+ the source cannot be fetched