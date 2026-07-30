import unittest

from envexport_cli.core import format_docker, format_json, format_shell, parse_env_file, shell_quote


class TestParseEnvFile(unittest.TestCase):
    def test_parses_simple_pairs(self) -> None:
        result = parse_env_file("FOO=bar\nBAZ=qux\n")
        self.assertEqual(result, {"FOO": "bar", "BAZ": "qux"})

    def test_ignores_blank_lines_and_comments(self) -> None:
        result = parse_env_file("\n# a comment\nFOO=bar\n")
        self.assertEqual(result, {"FOO": "bar"})

    def test_strips_export_prefix(self) -> None:
        result = parse_env_file("export FOO=bar\n")
        self.assertEqual(result, {"FOO": "bar"})

    def test_strips_surrounding_quotes(self) -> None:
        result = parse_env_file('FOO="bar baz"\nQUX=\'quux\'\n')
        self.assertEqual(result, {"FOO": "bar baz", "QUX": "quux"})

    def test_preserves_insertion_order(self) -> None:
        result = parse_env_file("B=2\nA=1\n")
        self.assertEqual(list(result.keys()), ["B", "A"])


class TestShellQuote(unittest.TestCase):
    def test_wraps_value_in_single_quotes(self) -> None:
        self.assertEqual(shell_quote("bar"), "'bar'")

    def test_escapes_embedded_single_quote(self) -> None:
        self.assertEqual(shell_quote("it's"), "'it'\\''s'")


class TestFormatters(unittest.TestCase):
    def test_format_shell_produces_export_lines(self) -> None:
        result = format_shell({"FOO": "bar"})
        self.assertEqual(result, "export FOO='bar'")

    def test_format_docker_produces_dash_e_flags(self) -> None:
        result = format_docker({"FOO": "bar", "BAZ": "qux"})
        self.assertEqual(result, "-e FOO=bar\n-e BAZ=qux")

    def test_format_json_round_trips(self) -> None:
        import json

        result = format_json({"FOO": "bar"})
        self.assertEqual(json.loads(result), {"FOO": "bar"})


if __name__ == "__main__":
    unittest.main()
