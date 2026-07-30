"""Core parsing and formatting logic for envexport-cli."""
from __future__ import annotations

import json


def parse_env_file(text: str) -> dict[str, str]:
    """Parse KEY=VALUE lines from .env-style text into an ordered dict.

    Blank lines and lines starting with `#` are ignored. An optional
    `export ` prefix is stripped. Surrounding single or double quotes
    around the value are stripped. Insertion order is preserved, matching
    the order keys appear in the file.
    """
    result: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            result[key] = value
    return result


def shell_quote(value: str) -> str:
    """Single-quote a value for POSIX shell, escaping any embedded single quotes."""
    return "'" + value.replace("'", "'\\''") + "'"


def format_shell(env: dict[str, str]) -> str:
    """Format env vars as `export KEY='VALUE'` lines, one per line."""
    return "\n".join(f"export {key}={shell_quote(value)}" for key, value in env.items())


def format_docker(env: dict[str, str]) -> str:
    """Format env vars as `-e KEY=VALUE` flags, one per line, for `docker run`."""
    return "\n".join(f"-e {key}={value}" for key, value in env.items())


def format_json(env: dict[str, str]) -> str:
    """Format env vars as a flat JSON object."""
    return json.dumps(env, indent=2)
