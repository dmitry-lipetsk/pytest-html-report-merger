# //////////////////////////////////////////////////////////////////////////////
import pytest
import dataclasses
import typing
import bs4
import re

from packaging.version import Version

from .e2eworkspace import E2EWorkspace

# //////////////////////////////////////////////////////////////////////////////


class HTML_FEATURES:
    @staticmethod
    def has_filter__failed(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__passed(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__skipped(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__xfailed(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__xpassed(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__error(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__rerun(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        return True

    # --------------------------------------------------------------------
    @staticmethod
    def has_filter__retried(html_ver: Version) -> bool:
        assert type(html_ver) is Version
        if html_ver > Version("4.1.1"):
            return True
        return False


# //////////////////////////////////////////////////////////////////////////////


class HTML_CHECKER:
    _content: str
    _soup: bs4.BeautifulSoup
    _html_version_text: str
    _html_version: Version

    # --------------------------------------------------------------------
    def __init__(self, content: str):
        assert type(content) is str
        self._content = content
        self._soup = bs4.BeautifulSoup(content, features="html.parser")
        self._html_version_text = __class__._extract_pytest_html_version(self._soup)
        self._html_version = Version(self._html_version_text)
        return

    # --------------------------------------------------------------------
    def check_filter__failed(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__failed(self._html_version):
            return

        if disabled:
            assert 'data-test-result="failed" disabled' in self._content
        else:
            assert 'data-test-result="failed"' in self._content
            assert 'data-test-result="failed" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__passed(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__passed(self._html_version):
            return

        if disabled:
            assert 'data-test-result="passed" disabled' in self._content
        else:
            assert 'data-test-result="passed"' in self._content
            assert 'data-test-result="passed" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__skipped(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__skipped(self._html_version):
            return

        if disabled:
            assert 'data-test-result="skipped" disabled' in self._content
        else:
            assert 'data-test-result="skipped"' in self._content
            assert 'data-test-result="skipped" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__xfailed(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__xfailed(self._html_version):
            return

        if disabled:
            assert 'data-test-result="xfailed" disabled' in self._content
        else:
            assert 'data-test-result="xfailed"' in self._content
            assert 'data-test-result="xfailed" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__xpassed(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__xpassed(self._html_version):
            return

        if disabled:
            assert 'data-test-result="xpassed" disabled' in self._content
        else:
            assert 'data-test-result="xpassed"' in self._content
            assert 'data-test-result="xpassed" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__error(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__error(self._html_version):
            return

        if disabled:
            assert 'data-test-result="error" disabled' in self._content
        else:
            assert 'data-test-result="error"' in self._content
            assert 'data-test-result="error" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__rerun(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__rerun(self._html_version):
            return

        if disabled:
            assert 'data-test-result="rerun" disabled' in self._content
        else:
            assert 'data-test-result="rerun"' in self._content
            assert 'data-test-result="rerun" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    def check_filter__retried(self, disabled: bool):
        assert type(self._content) is str

        if not HTML_FEATURES.has_filter__retried(self._html_version):
            return

        if disabled:
            assert 'data-test-result="retried" disabled' in self._content
        else:
            assert 'data-test-result="retried"' in self._content
            assert 'data-test-result="retried" disabled' not in self._content
        return

    # --------------------------------------------------------------------
    @staticmethod
    def _extract_pytest_html_version(soup: bs4.BeautifulSoup) -> str:
        assert isinstance(soup, bs4.BeautifulSoup)

        """
        Robustly extract pytest-html version from the report footer/header.
        Example text: '... by pytest-html v4.0.2'
        """
        link = soup.find("a", href=re.compile(r"pytest-html"))
        if link is None:
            raise RuntimeError("Report does not have section with pytest-html link.")

        parent_text = link.parent.get_text()

        # Looking for pattern 'v' and digits (v4.0.2)
        match = re.search(r"v(\d+\.\d+\.\d+[\w\.]*)", parent_text)
        if not match:
            raise RuntimeError(
                "Cannot extract pytest-html version from {0!r}.".format(parent_text)
            )

        return match.group(1)


# //////////////////////////////////////////////////////////////////////////////


def test_e2e_001__single_report_metadata():
    """
    E2E Test: Generate one report with specific metadata and merge it.
    Verifies that metadata and basic structure are preserved.
    """
    ws = E2EWorkspace(prefix="e2e_single_")
    try:
        # 1. Generate a single report with metadata
        # We use a simple test that definitely passes
        test_code = "def test_logic(): assert 2 + 2 == 4"
        metadata = {"Project": "Alpha-Centauri", "User": "Tester-Dima"}

        ws.generate_report("run1", test_code, metadata=metadata)

        # 2. Define output path and run merger
        output_html = ws.root / "merged_output.html"
        # We point to the directory where run1.html was generated
        result = ws.run_merger(
            [
                "-i",
                str(ws.reports_dir),
                "-o",
                str(output_html),
                "--title",
                "Single Report Test",
            ]
        )

        # 3. Assertions
        assert result.returncode == 0, f"Merger failed: {result.stderr}"
        assert output_html.exists(), "Merged HTML file was not created"

        content = output_html.read_text()

        # Check Title
        assert "Single Report Test" in content

        # Check Metadata (Environment table)
        assert "Project" in content
        assert "Alpha-Centauri" in content
        assert "User" in content
        assert "Tester-Dima" in content

        # Check Summary
        assert "1 test took" in content

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_002__merge_two_reports_metadata():
    ws = E2EWorkspace(prefix="e2e_double_")
    try:
        # 1. Generate first report
        ws.generate_report(
            "run_a", "def test_a(): assert True", metadata={"Project": "Alpha"}
        )

        # 2. Generate second report
        ws.generate_report(
            "run_b", "def test_b(): assert True", metadata={"Environment": "Staging"}
        )

        # 3. Merge them
        output_html = ws.root / "merged_final.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        # 4. Critical Checks
        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        # Check that BOTH metadata entries exist (our main fix!)
        assert "Project" in content
        assert "Alpha" in content
        assert "Environment" in content
        assert "Staging" in content

        # Check summary logic
        assert "2 tests took" in content

        # Check that both test names are visible in the report
        assert "test_a" in content
        assert "test_b" in content

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_003__statistics_consistency():
    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        # Run 1: 1 Pass, 1 Fail
        code1 = """
def test_p1(): assert True
def test_f1(): assert False
"""
        ws.generate_report("run1", code1)

        # Run 2: 1 Pass, 1 Skip
        code2 = """
import pytest
def test_p2(): assert True
@pytest.mark.skip(reason="testing skip")
def test_s1(): pass
"""
        ws.generate_report("run2", code2)

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "4 tests took" in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "2 Passed" in content
        assert "1 Failed" in content
        assert "1 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        # --- Advanced check: Ensure 'disabled' attribute is removed for active filters ---
        # The 'failed', 'passed', and 'skipped' filters must be clickable now.
        # We check that they DON'T have the 'disabled' string inside their tag.
        html_checker.check_filter__failed(disabled=False)
        html_checker.check_filter__passed(disabled=False)
        html_checker.check_filter__error(disabled=True)

    finally:
        pass

    ws.cleanup()


# ------------------------------------------------------------------------
@dataclasses.dataclass
class tagData004:
    counts: list


# ------------------------------------------------------------------------
C_COUNT004 = 3

g_Data004: typing.List[tagData004] = [
    tagData004(counts=[x, C_COUNT004 - x]) for x in range(0, C_COUNT004 + 1)
]


# ------------------------------------------------------------------------
@pytest.fixture(params=g_Data004, ids=["-".join(map(str, x.counts)) for x in g_Data004])
def data004(request: pytest.FixtureRequest) -> tagData004:
    assert isinstance(request, pytest.FixtureRequest)
    return request.param


# ------------------------------------------------------------------------
def test_e2e_004A__statistics_consistency__failed(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = ""
            for n in range(data004.counts[i]):
                code += "def test_p{}_{}(): assert False\n".format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "{} Failed".format(cTests) in content
        assert "0 Passed" in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=False)
        html_checker.check_filter__passed(disabled=True)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004B__statistics_consistency__passed(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = ""
            for n in range(data004.counts[i]):
                code += "def test_p{}_{}(): assert True\n".format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "{} Passed".format(cTests) in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=False)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004C__statistics_consistency__skipped(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = "import pytest\n"
            for n in range(data004.counts[i]):
                code += 'def test_p{}_{}(): pytest.skip("AAAA")\n'.format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "0 Passed" in content
        assert "{} Skipped".format(cTests) in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=True)
        html_checker.check_filter__skipped(disabled=False)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004D__statistics_consistency__xfailed(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = "import pytest\n"
            for n in range(data004.counts[i]):
                code += 'def test_p{}_{}(): pytest.xfail("AAAA")\n'.format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "0 Passed" in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "{} Expected failures".format(cTests) in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=True)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=False)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004E__statistics_consistency__xpassed(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = "import pytest\n"
            for n in range(data004.counts[i]):
                code += "@pytest.mark.xfail\n"
                code += "def test_p{}_{}(): assert True\n".format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "0 Passed" in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "{} Unexpected passes".format(cTests) in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=True)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=False)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004F__statistics_consistency__rerun(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = "import pytest\n"
            for n in range(data004.counts[i]):
                code += "g_calls_{} = 0\n".format(n)
                code += "@pytest.mark.flaky(reruns=3, reruns_delay=1)\n"
                code += "def test_p{0}_{1}(): global g_calls_{1}; g_calls_{1}+=1; assert g_calls_{1}>1\n".format(
                    i, n
                )
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "{} Passed".format(cTests) in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "0 Errors" in content
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "{} Reruns".format(cTests) in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=False)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=True)
        html_checker.check_filter__rerun(disabled=False)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_004G__statistics_consistency__error(data004: tagData004):
    assert type(data004) is tagData004

    ws = E2EWorkspace(prefix="e2e_stats_")
    try:
        cTests = 0
        for i in range(len(data004.counts)):
            cTests += data004.counts[i]
            code = """import pytest
@pytest.fixture
def boom(): raise Exception("BOOM")\n
"""
            for n in range(data004.counts[i]):
                code += "def test_p{0}_{1}(boom): pass\n".format(i, n)
                continue

            ws.generate_report("run_{}".format(i), code)
            continue

        assert cTests > 1

        output_html = ws.root / "stats_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # --- Check Summary Line ---
        assert "{} tests took".format(cTests) in content

        # --- Check Visual Counters (Filters) ---
        # Verified results from our 2 runs
        assert "0 Failed" in content
        assert "0 Passed" in content
        assert "0 Skipped" in content

        # Categories that should remain zero
        # We check the exact strings expected in the HTML
        assert "{} Errors".format(cTests) in content  # three errorS!
        assert "0 Expected failures" in content  # for xfailed
        assert "0 Unexpected passes" in content  # for xpassed
        assert "0 Reruns" in content  # for rerun

        # If your version of pytest-html has 'Retried'
        if "Retried" in content:
            assert "0 Retried" in content

        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=True)
        html_checker.check_filter__skipped(disabled=True)
        html_checker.check_filter__xfailed(disabled=True)
        html_checker.check_filter__xpassed(disabled=True)
        html_checker.check_filter__error(disabled=False)
        html_checker.check_filter__rerun(disabled=True)
        html_checker.check_filter__retried(disabled=True)

    finally:
        pass

    ws.cleanup()
    return


# ------------------------------------------------------------------------
def test_e2e_005__statistics_consistency__error():
    # Author: Mark G <mark@google.com>

    ws = E2EWorkspace(prefix="e2e_error_")
    try:
        # One OK test, One with an error in setup
        code = """
import pytest
@pytest.fixture
def boom(): raise Exception("BOOM")

def test_pass(): assert True
def test_error(boom): pass
"""
        ws.generate_report("run_err", code)

        output_html = ws.root / "error_check.html"
        result = ws.run_merger(["-i", str(ws.reports_dir), "-o", str(output_html)])

        assert result.returncode == 0
        assert output_html.exists()
        content = output_html.read_text()

        html_checker = HTML_CHECKER(content)

        # Check our money
        assert "2 tests took" in content
        assert "0 Failed" in content
        assert "1 Passed" in content
        assert "1 Error" in content  # one erroR!

        # Check a button
        html_checker.check_filter__failed(disabled=True)
        html_checker.check_filter__passed(disabled=False)
        html_checker.check_filter__error(disabled=False)

    finally:
        pass

    ws.cleanup()
    return


# //////////////////////////////////////////////////////////////////////////////
