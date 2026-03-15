# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pytest_html_report_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet002__parse_duration_to_seconds:
    @dataclasses.dataclass
    class tagData002:
        sign: str
        value: typing.Any
        result: float

    # Positive test cases
    sm_Data002Ok: typing.List[tagData002] = [
        # Numeric inputs
        tagData002(sign="int_seconds", value=10, result=10.0),
        tagData002(sign="float_seconds", value=123.456, result=123.456),
        # Milliseconds format
        tagData002(sign="ms_int", value="303 ms", result=0.303),
        tagData002(sign="ms_float", value="12.5 ms", result=0.0125),
        tagData002(sign="ms_zero", value="0 ms", result=0.0),
        # Plain numeric strings
        tagData002(sign="str_int", value="5", result=5.0),
        tagData002(sign="str_float", value="1.5", result=1.5),
        # HH:MM:SS format
        tagData002(sign="hms_simple", value="00:00:03", result=3.0),
        tagData002(sign="hms_full", value="01:02:03", result=3723.0),
        # HH:MM:SS with fractional parts
        tagData002(sign="hms_frac_ms", value="00:00:01.5", result=1.5),
        tagData002(sign="hms_frac_micro", value="00:00:01.000001", result=1.000001),
        tagData002(sign="hms_frac_round_up", value="00:00:01.9999999", result=2.0),
        # Mix
        tagData002(sign="tiny1", value="00:00:00.0000001", result=0.0),
        tagData002(sign="tiny2", value="00:00:00.0000002", result=0.0),
        tagData002(sign="tiny3", value="00:00:00.0000003", result=0.0),
        tagData002(sign="tiny4", value="00:00:00.0000004", result=0.0),
        tagData002(sign="tiny5", value="00:00:00.0000005", result=0.000001),
    ]

    # Negative test cases (expecting ValueError)
    sm_Data002Fail: typing.List[tagData002] = [
        tagData002(sign="wrong_string", value="invalid", result=0.0),
        tagData002(sign="wrong_format", value="00-00-03", result=0.0),
        tagData002(sign="empty_str", value="", result=0.0),
        tagData002(sign="none_val", value=None, result=0.0),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data002Ok, ids=[x.sign for x in sm_Data002Ok])
    def data002ok(self, request: pytest.FixtureRequest) -> tagData002:
        return request.param

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data002Fail, ids=[x.sign for x in sm_Data002Fail])
    def data002fail(self, request: pytest.FixtureRequest) -> tagData002:
        return request.param

    # --------------------------------------------------------------------
    def test_002_ok(self, data002ok: tagData002):
        assert type(data002ok) is __class__.tagData002
        r = prog.PytestHTMLReportMerger._parse_duration_to_seconds(data002ok.value)
        # Use approx to handle potential float precision issues
        assert r == pytest.approx(data002ok.result)

    # --------------------------------------------------------------------
    def test_002_fail(self, data002fail: tagData002):
        with pytest.raises(ValueError):
            prog.PytestHTMLReportMerger._parse_duration_to_seconds(data002fail.value)


# //////////////////////////////////////////////////////////////////////////////
