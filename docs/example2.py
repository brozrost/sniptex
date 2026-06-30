"""
tagsnip-start comm0
pip install tagsnip
tagsnip-end comm0

tagsnip-start comm1
\IncludeCode[options]{source}{tag}{language}{caption}
tagsnip-end comm1

tagsnip-start comm2
\IncludeCode[firstnumber=1, fontsize=\scriptsize, style=monokai] {source}{tag}{language}{caption}
tagsnip-end comm2

tagsnip-start comm3
\IncludeCode{example.py}{tag1}{Python}{Úryvek 2: ...}
tagsnip-end comm3

tagsnip-start comm4
\IncludeCode{raw.githubusercontent.com/brozrost /tagsnip/main/docs/example2.py}{tag2}{Python}{Úryvek 3: ...}
tagsnip-end comm4
"""

import re

class TagsnipError(RuntimeError):
    pass

def marker_matches(line: str, marker: str) -> bool:
    pattern = rf"{re.escape(marker)}(?!\S)"
    return re.search(pattern, line) is not None

def extract_tagged_block(text: str, tag: str):
    start_marker = f"tagsnip-start {tag}"
    end_marker = f"tagsnip-end {tag}"

    lines = text.splitlines()

    start_index = None
    end_index = None

    # tagsnip-start tag2
    for i, line in enumerate(lines):
        if marker_matches(line, start_marker):
            if start_index is not None:
                raise TagsnipError(f"Multiple start tags found for '{tag}'")

            start_index = i

    if start_index is None:
        raise TagsnipError(f"Start tag not found for '{tag}'")
    # tagsnip-end tag2
    
    for i in range(start_index + 1, len(lines)):
        if end_marker in lines[i]:
            end_index = i
            break

    if end_index is None:
        raise TagsnipError(f"End tag not found for '{tag}'")
    
    # tagsnip-start return
    return "\n".join(lines[start_index + 1:end_index]), start_index + 2, end_index
    # tagsnip-end return