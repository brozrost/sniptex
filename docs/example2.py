"""
sniptex-start comm
\IncludeCode{docs/example.py}{demo}{Python}{Snippet 1: Local code snippet}
sniptex-end comm
"""

class SniptexError(RuntimeError):
    pass

def extract_tagged_block(text: str, tag: str):
    start_marker = f"sniptex-start {tag}"
    end_marker = f"sniptex-end {tag}"

    lines = text.splitlines()

    start_index = None
    end_index = None

    # sniptex-start 1
    for i, line in enumerate(lines):
        if start_marker in line:
            if start_index is not None:
                raise SniptexError(f"Multiple start tags found for '{tag}'")

            start_index = i

    if start_index is None:
        raise SniptexError(f"Start tag not found for '{tag}'")
    # sniptex-end 1
    
    for i in range(start_index + 1, len(lines)):
        if end_marker in lines[i]:
            end_index = i
            break

    if end_index is None:
        raise SniptexError(f"End tag not found for '{tag}'")
    
    # sniptex-start return
    return "\n".join(lines[start_index + 1:end_index]), start_index + 2, end_index
    # sniptex-end return