from sniptex import extractor

PATH = "./docs/example.py"

TEXT = """
def extract_tagged_block(text: str, tag: str) -> str:
    start_marker = f"sniptex-start {tag}"
    end_marker = f"sniptex-end {tag}"

    lines = text.splitlines()

    start_index = None
    end_index = None

    # sniptex-start 1
    for i, line in enumerate(lines):
        if start_marker in line:
            if start_index is not None:
                raise SniptexError("Multiple start tags found for `{tag}`")

            start_index = i

    if start_index is None:
        raise SniptexError("Start tag not found for `{tag}`")
    # sniptex-end 1
    
    for i in range(start_index + 1, len(lines)):
        if end_marker in lines[i]:
            end_index = i
            break

    if end_index is None:
        raise SniptexError("End tag not found for `{tag}`")
    
    return "\n".join(lines[start_index + 1:end_index])
"""

OUT = """    for i, line in enumerate(lines):
        if start_marker in line:
            if start_index is not None:
                raise SniptexError("Multiple start tags found for `{tag}`")

            start_index = i

    if start_index is None:
        raise SniptexError("Start tag not found for `{tag}`")"""

def test_extract_tagged_block():
    assert extractor.extract_tagged_block(TEXT, "1") == OUT

def test_extract_from_file():
    assert extractor.extract_from_file(PATH, "1") == OUT

def test_missing_start_tag():
    text = """
    hello
    # sniptex-end 1
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected SniptexError"
    except extractor.SniptexError as err:
        assert str(err) == "Start tag not found for `1`"


def test_missing_end_tag():
    text = """
    # sniptex-start 1
    hello
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected SniptexError"
    except extractor.SniptexError as err:
        assert str(err) == "End tag not found for `1`"


def test_multiple_start_tags():
    text = """
    # sniptex-start 1
    hello
    # sniptex-start 1
    world
    # sniptex-end 1
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected SniptexError"
    except extractor.SniptexError as err:
        assert str(err) == "Multiple start tags found for `1`"

def test_missing_file():
    try:
        extractor.extract_from_file("./does_not_exist.py", "1")
        assert False, "Expected SniptexError"
    except extractor.SniptexError:
        pass

def main():
    test_extract_tagged_block()
    test_extract_from_file()
    test_missing_start_tag()
    test_missing_end_tag()
    test_multiple_start_tags()
    test_missing_file()

if __name__ == "__main__":
    main()
