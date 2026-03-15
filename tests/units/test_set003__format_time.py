# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pytest_html_report_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet003__format_time:
    @dataclasses.dataclass
    class tagData003:
        sign: str
        duration: float
        result: str

    sm_Data003Ok: typing.List[tagData003] = [
        # 1. Milliseconds (less than 1s)
        tagData003("zero", 0.0, "0 ms"),
        tagData003("ms_small", 0.005, "5 ms"),
        tagData003("ms_large", 0.999, "999 ms"),
        # 2. Boundary case
        tagData003("exactly_one_sec", 1.0, "00:00:01"),
        # 3. Seconds
        tagData003("seconds", 59.0, "00:00:59"),
        # 4. Minutes
        tagData003("one_minute", 60.0, "00:01:00"),
        tagData003("minutes_seconds", 61.5, "00:01:01"),  # .5 is dropped due to int()
        # 5. Hours
        tagData003("one_hour", 3600.0, "01:00:00"),
        tagData003("full_time", 3661.0, "01:01:01"),
        # 6. Large values
        tagData003("many_hours", 360000.0, "100:00:00"),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data003Ok, ids=[x.sign for x in sm_Data003Ok])
    def data003ok(self, request: pytest.FixtureRequest) -> tagData003:
        return request.param

    # --------------------------------------------------------------------
    def test_003_ok(self, data003ok: tagData003):
        assert type(data003ok) is __class__.tagData003
        r = prog.PytestHTMLReportMerger._format_time(data003ok.duration)
        assert r == data003ok.result
        return


# //////////////////////////////////////////////////////////////////////////////
