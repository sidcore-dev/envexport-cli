# envexport-cli

A small, dependency-free command-line tool that turns a `.env`-style file
into shell `export` lines, `docker run` flags, or a flat JSON object.

![demo](demo.gif)

## Why

Loading a `.env` file into your current shell, or forwarding it to a
`docker run` command, usually means writing a one-off loop or reaching
for a dependency. `envexport-cli` does the conversion in one call and
handles quoting correctly, including values containing single quotes.

## Install

```bash
pip install .
```

This installs an `envexport-cli` command on your PATH.

## Usage

Given a `.env` file:

```
DATABASE_URL=postgres://localhost/app
API_KEY=it's-a-secret
```

```bash
envexport-cli .env
```

```
export DATABASE_URL='postgres://localhost/app'
export API_KEY='it'\''s-a-secret'
```

Load it directly into your shell:

```bash
eval $(envexport-cli .env)
```

Docker flags, for forwarding into a container:

```bash
docker run $(envexport-cli .env --format docker) myimage
```

```
-e DATABASE_URL=postgres://localhost/app
-e API_KEY=it's-a-secret
```

JSON, for tooling that wants structured input:

```bash
envexport-cli .env --format json
```

```json
{
  "DATABASE_URL": "postgres://localhost/app",
  "API_KEY": "it's-a-secret"
}
```

### Options

| Flag              | Description                                                       |
|--------------------|-----------------------------------------------------------------------|
| `file` (positional) | Path to the `.env` file (default: `.env`)                            |
| `--format`         | Output format: `shell` (default), `docker`, or `json`                |

### Exit codes

- `0` — success
- `2` — the input file couldn't be read

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
