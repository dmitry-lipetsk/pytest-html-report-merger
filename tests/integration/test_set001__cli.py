import subprocess
import os
import typing

# //////////////////////////////////////////////////////////////////////////////


def run_cli(args: typing.List[str]) -> subprocess.CompletedProcess:
    """
    Helper to run the CLI with correct PYTHONPATH.
    """
    env = os.environ.copy()
    # Add 'src' to PYTHONPATH so python can find the package
    env["PYTHONPATH"] = "src" + os.pathsep + env.get("PYTHONPATH", "")

    return subprocess.run(
        ["python3", "-m", "pytest_html_report_merger"] + args,
        capture_output=True,
        text=True,
        env=env,
    )


# //////////////////////////////////////////////////////////////////////////////


def test_cli_no_args():
    """
    Test calling the utility without any arguments.
    """
    result = run_cli([])

    # Check for usage info or argparse error
    assert "usage:" in result.stdout.lower() or "error" in result.stderr.lower()
    assert result.returncode in [0, 2]
    return


# ------------------------------------------------------------------------
def test_cli_empty_input_dir(tmp_path):
    """
    Test calling with an empty input directory using -i flag.
    """
    empty_dir = tmp_path / "empty_reports"
    empty_dir.mkdir()

    # Using our helper
    result = run_cli(["-i", str(empty_dir)])

    # Our custom log message should be there (check both stdout/stderr depending on your logger)
    output = result.stdout + result.stderr
    assert "No HTML reports found" in output
    return


# ------------------------------------------------------------------------
def test_cli_help():
    """
    Test calling the utility with --help.
    It should exit with 0 and show the description.
    """
    # Вызываем с -h
    result = run_cli(["-h"])

    assert result.returncode == 0
    # Проверяем, что наши ключевые слова есть в выводе
    output = result.stdout.lower()
    assert "usage:" in output
    assert "merge multiple pytest-html reports" in output
    assert "--input-dir" in output
    assert "--out" in output
    return


# ------------------------------------------------------------------------
def test_cli_non_existent_file():
    """
    Test calling with a file path that does not exist.
    Should report an error and exit with code 1.
    """
    result = run_cli(["non_existent_report.html"])

    assert result.returncode == 1
    # Check that we collected the error message
    assert "Invalid input" in result.stderr
    assert "non_existent_report.html" in result.stderr
    assert "Termination due to input errors" in result.stderr
    return


# ------------------------------------------------------------------------
def test_cli_invalid_input_dir():
    """
    Test calling with a directory that does not exist.
    Glob will return empty list, and we should see the 'No reports found' error.
    """
    C_UNK_DIR = "/tmp/path/that/definitely/does/not/exist"
    result = run_cli(["-i", C_UNK_DIR])

    # In this case, has_errors is False (glob just found nothing),
    # but not raw_files will be True.
    assert "Input directory does not exist: '{}'".format(C_UNK_DIR) in result.stderr
    assert "Termination due to input errors" in result.stderr
    return


# ------------------------------------------------------------------------
def test_cli_two_unk_dirs_and_two_unk_files():
    """
    Test calling with a directory that does not exist.
    Glob will return empty list, and we should see the 'No reports found' error.
    """
    C_UNK_DIR1 = "/tmp/path/that/definitely/does/not/exist_dir1"
    C_UNK_DIR2 = "/tmp/path/that/definitely/does/not/exist_dir2"
    C_UNK_FILE1 = "/tmp/path/that/definitely/does/not/exist_file1.html"
    C_UNK_FILE2 = "/tmp/path/that/definitely/does/not/exist_file2.html"
    result = run_cli(
        [
            "-i",
            C_UNK_DIR1,
            "-i",
            C_UNK_DIR2,
            C_UNK_FILE1,
            C_UNK_FILE2,
        ]
    )

    assert "Input directory does not exist: '{}'".format(C_UNK_DIR1) in result.stderr
    assert "Input directory does not exist: '{}'".format(C_UNK_DIR2) in result.stderr
    assert (
        "Invalid input: '{}' is not a file or does not exist.".format(C_UNK_FILE1)
        in result.stderr
    )
    assert (
        "Invalid input: '{}' is not a file or does not exist.".format(C_UNK_FILE2)
        in result.stderr
    )
    assert "Termination due to input errors" in result.stderr
    return


# ------------------------------------------------------------------------
def test_cli_error_on_duplicate_files(tmp_path):
    """
    Test that providing the same file via different paths (relative/absolute)
    triggers a 'Duplicate input' error.
    """
    report = tmp_path / "report.html"
    report.write_text("<html></html>")

    # Пытаемся скормить файл двумя путями: относительным и абсолютным
    report_rel = os.path.relpath(report)
    report_abs = os.path.abspath(report)

    result = run_cli([report_rel, report_abs])

    assert result.returncode == 1
    assert "Duplicate input file detected" in result.stderr
    assert "Termination due to input errors" in result.stderr
    return


# //////////////////////////////////////////////////////////////////////////////
