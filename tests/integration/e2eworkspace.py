# /////////////////////////////////////////////////////////////////////////////
import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path


# /////////////////////////////////////////////////////////////////////////////


class E2EWorkspace:
    def __init__(self, prefix="merger_e2e_"):
        self.root = Path(tempfile.mkdtemp(prefix=prefix))
        self.reports_dir = self.root / "reports"
        self.reports_dir.mkdir()
        self.src_path = Path(__file__).parent.parent.parent / "src"

    def cleanup(self):
        """Удаляем всё за собой."""
        if self.root.exists():
            shutil.rmtree(self.root)

    def generate_report(self, name: str, test_code: str, metadata: dict = None):
        test_file = self.root / f"test_{name}.py"
        test_file.write_text(test_code)

        report_path = self.reports_dir / f"{name}.html"

        # Use sys.executable, to be in our venv
        cmd = [
            sys.executable, "-m", "pytest",
            f"--html={report_path}",
            "--self-contained-html",
            "-c", "/dev/null",
            "-p", "no:cacheprovider",  # it disables create ,pytest_cache in /dev
            str(test_file),
        ]

        if metadata:
            for k, v in metadata.items():
                cmd.extend(["--metadata", str(k), str(v)])

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Code 0 — OK,
        # Code 1 — there are failed tests.
        # Code 5 - no any tests were executed
        if result.returncode not in [0, 1, 5]:
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd)

        # CRITICAL CHECK: Verify that the report file was actually created
        if not report_path.exists():
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            raise FileNotFoundError(
                f"Pytest finished with code {result.returncode}, "
                f"but failed to generate report at: {report_path}"
            )

        return report_path

    def run_merger(self, args: list):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.src_path)
        cmd = [sys.executable, "-m", "pytest_html_report_merger"] + args
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

# /////////////////////////////////////////////////////////////////////////////
