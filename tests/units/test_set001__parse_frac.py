# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pytest_html_report_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet001__parse_frac:
    @dataclasses.dataclass
    class tagData001Ok:
        sign: str
        text: str
        result: float

    sm_Data001Ok: typing.List[tagData001Ok] = [
        tagData001Ok(
            sign="empty",
            text="",
            result=0,
        ),
        tagData001Ok(
            sign="1",
            text="1",
            result=0.1,
        ),
        tagData001Ok(
            sign="123",
            text="123",
            result=0.123,
        ),
        tagData001Ok(
            sign="1234",
            text="1234",
            result=0.1234,
        ),
        tagData001Ok(
            sign="12345",
            text="12345",
            result=0.12345,
        ),
        tagData001Ok(
            sign="12345",
            text="12345",
            result=0.12345,
        ),
        tagData001Ok(
            sign="123456",
            text="123456",
            result=0.123456,
        ),
        tagData001Ok(
            sign="1234561",
            text="1234561",
            result=0.123456,
        ),
        tagData001Ok(
            sign="1234562",
            text="1234562",
            result=0.123456,
        ),
        tagData001Ok(
            sign="1234563",
            text="1234563",
            result=0.123456,
        ),
        tagData001Ok(
            sign="1234564",
            text="1234564",
            result=0.123456,
        ),
        tagData001Ok(
            sign="1234565",
            text="1234565",
            result=0.123457,
        ),
        tagData001Ok(
            sign="1234566",
            text="1234566",
            result=0.123457,
        ),
        tagData001Ok(
            sign="1234567",
            text="1234567",
            result=0.123457,
        ),
        tagData001Ok(
            sign="1234568",
            text="1234568",
            result=0.123457,
        ),
        tagData001Ok(
            sign="1234569",
            text="1234569",
            result=0.123457,
        ),
        tagData001Ok(
            sign="999999",
            text="999999",
            result=0.999999,
        ),
        tagData001Ok(
            sign="9999994",
            text="9999994",
            result=0.999999,
        ),
        tagData001Ok(
            sign="9999995",
            text="9999995",
            result=1.0,
        ),
        # Leading zeros (ensure they aren't lost by int conversion)
        tagData001Ok(
            sign="leading_zero",
            text="05",
            result=0.05,
        ),
        tagData001Ok(
            sign="many_leading_zeros",
            text="000005",
            result=0.000005,
        ),
        # Leading zeros with rounding
        tagData001Ok(
            sign="leading_zeros_round_up",
            text="0000059",
            result=0.000006,
        ),
        tagData001Ok(
            sign="leading_zeros_round_down",
            text="0000054",
            result=0.000005,
        ),
        # Zeros only
        tagData001Ok(
            sign="zeros_short",
            text="000",
            result=0.0,
        ),
        tagData001Ok(
            sign="zeros_long_with_tail",
            text="0000009",
            result=0.000001,  # Rounding up from 7th zero
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data001Ok, ids=[x.sign for x in sm_Data001Ok])
    def data001ok(self, request: pytest.FixtureRequest) -> tagData001Ok:
        return request.param

    # --------------------------------------------------------------------
    def test_001_ok(self, data001ok: tagData001Ok):
        assert type(data001ok) is __class__.tagData001Ok
        r = prog.PytestHTMLReportMerger._parse_frac(data001ok.text)
        assert r == data001ok.result
        return


# //////////////////////////////////////////////////////////////////////////////
