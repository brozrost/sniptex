import argparse
from pathlib import Path

import extractor

def main() -> int:
    parser = argparse.ArgumentParser(
        description="sniptex",
        usage="..."
    )

    parser.add_argument("-s", "--source", required=True, help="Path to the local source file.")
    parser.add_argument("-t", "--tag", required=True, help="Snippet tag name.")
    parser.add_argument("-o", "--out", help="Path to the output file. If omitted, prints to stdout.")

    args = parser.parse_args()

    try:
        snippet = extractor.extract_from_file(args.source, args.tag)
    except extractor.SniptexError as exc:
        print(f"Error: {exc}")
        return 1

    if args.out:
        output_path = Path(args.output)

        try:
            output_path.write_text(snippet, encoding="utf-8")
        except OSError as exc:
            print(f"Error: Could not write file: {output_path}")
            return 1
    else:
        print(snippet)

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())