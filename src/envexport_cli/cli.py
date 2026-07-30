"""Command-line entry point for envexport-cli."""
from __future__ import annotations

import argparse
import sys

from .core import format_docker, format_json, format_shell, parse_env_file

FORMATTERS = {
    "shell": format_shell,
    "docker": format_docker,
    "json": format_json,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="envexport-cli",
        description="Read a .env-style file and print shell exports, docker flags, or JSON.",
    )
    parser.add_argument("file", nargs="?", default=".env", help="Path to the .env file (default: .env)")
    parser.add_argument(
        "--format",
        choices=sorted(FORMATTERS),
        default="shell",
        help="Output format: shell exports, docker -e flags, or a flat JSON object (default: shell)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        with open(args.file, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"envexport-cli: error: could not read {args.file}: {exc}", file=sys.stderr)
        return 2

    env = parse_env_file(text)
    output = FORMATTERS[args.format](env)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
