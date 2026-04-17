import os
import argparse
from pathlib import Path

from sniptex import extractor
from sniptex import fetcher
from sniptex import validate

def main() -> int:
    parser = argparse.ArgumentParser(
        description="SnipTeX is a Python package for extracting tagged code snippets from local files or remote sources. " \
        "It locates marked regions in source code and returns their contents for further processing or integration into other tools.",
        usage="""
        sniptex -h/--help

        sniptex -s/--source <url/file path> -t/--tag <tag>
            Example: sniptex -s https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example.py -t 1

        sniptex -s/--source <url/file path> -t/--tag <tag> -o/--out <out file>
            Example: sniptex -s https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example.py -t 1 -o out/out.txt
        """
    )

    parser.add_argument(
        "-s", "--source", 
        required=True, 
        help="Path to the local source file."
    )
    parser.add_argument(
        "-t", "--tag", 
        required=True, 
        help="Snippet tag name."
    )
    parser.add_argument(
        "-o", "--out", 
        help="Path to the output file. If omitted, prints to stdout."
    )

    args = parser.parse_args()

    try:
        if validate.is_url(args.source):
            fetch = fetcher.FetcherClient()
            text = fetch.fetch_text(args.source)
        else:
            text = Path(args.source).read_text(encoding="utf-8")

        snippet = extractor.extract_tagged_block(text, args.tag)

    except fetcher.FetcherError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print(f"Error: Could not read file: {args.source}", file=sys.stderr)
        return 1
    except extractor.SniptexError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.out:
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
        output_path = Path(args.out)

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