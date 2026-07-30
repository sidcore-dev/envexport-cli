import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from envexport_cli.cli import main


class TestCli(unittest.TestCase):
    def test_default_format_is_shell_exports(self) -> None:
        with TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text("FOO=bar\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(env_file)])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "export FOO='bar'")

    def test_docker_format(self) -> None:
        with TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text("FOO=bar\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(env_file), "--format", "docker"])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "-e FOO=bar")

    def test_json_format_is_valid_json(self) -> None:
        with TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text("FOO=bar\nBAZ=qux\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main([str(env_file), "--format", "json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue()), {"FOO": "bar", "BAZ": "qux"})

    def test_missing_file_returns_exit_code_two(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["/no/such/file.env"])
        self.assertEqual(code, 2)
        self.assertIn("could not read", err.getvalue())

    def test_defaults_to_dot_env_in_cwd(self) -> None:
        with TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("FOO=bar\n")
            import os

            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                out = io.StringIO()
                with redirect_stdout(out):
                    code = main([])
                self.assertEqual(code, 0)
                self.assertIn("FOO", out.getvalue())
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
