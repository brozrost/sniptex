from pathlib import Path

class SniptexError(RuntimeError):
    pass

def extract_tagged_block(text: str, tag: str) -> str:
    start_marker = f"sniptex-start {tag}"
    end_marker = f"sniptex-end {tag}"

    lines = text.splitlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if start_marker in line:
            if start_index is not None:
                raise SniptexError(f"Multiple start tags found for `{tag}`")

            start_index = i

    if start_index is None:
        raise SniptexError(f"Start tag not found for `{tag}`")
    
    for i in range(start_index + 1, len(lines)):
        if end_marker in lines[i]:
            end_index = i
            break

    if end_index is None:
        raise SniptexError(f"End tag not found for `{tag}`")
    
    return "\n".join(lines[start_index + 1:end_index])

def extract_from_file(path: str | Path, tag: str) -> str:
    file_path = Path(path)

    if not file_path.is_file():
        raise SniptexError(f"File not found: {file_path}")
    
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SniptexError(f"Could not read file: {file_path}") from exc

    return extract_tagged_block(text, tag)
