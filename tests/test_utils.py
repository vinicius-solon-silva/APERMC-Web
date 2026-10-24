"""Unit tests for the pure utility functions in utils.py."""

from io import StringIO
from urllib.parse import urlencode

import pandas as pd
import pytest
from utils import (
    MUNICIPAL_COORDINATES,
    format_percent,
    format_tonnes,
    parse_brazilian_number,
    sheet_url,
    tidy_columns,
    YEARS,
)


class TestSheetUrl:
    def test_builds_url_with_sheet_name(self):
        # urlencode() produces standard percent-encoding (spaces → +)
        url = sheet_url("Dados IBGE 2022")
        assert "tqx" in url and "sheet" in url
        assert urlencode({"sheet": "Dados IBGE 2022"}) in url

    def test_url_contains_sheet_name(self):
        url = sheet_url("Emissões Anuais e Totais")
        assert "sheet" in url
        assert urlencode({"sheet": "Emissões Anuais e Totais"}) in url

    def test_url_returns_str(self):
        assert isinstance(sheet_url("Foo"), str)


class TestParseBrazilianNumber:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("1.234,56", 1234.56),
            ("1.234", 1234.0),
            ("1234,56", 1234.56),
            ("1.234.567,89", 1234567.89),
            ("  987,65  ", 987.65),
            ("", float("nan")),
            ("   ", float("nan")),
            (None, float("nan")),
            ("abc", float("nan")),
            ("", float("nan")),
        ],
    )
    def test_parses_brazilian_format(self, value, expected):
        result = parse_brazilian_number(value)
        if pd.isna(expected):
            assert pd.isna(result), f"expected NaN for {value!r}, got {result}"
        else:
            assert result == expected, f"expected {expected} for {value!r}, got {result}"


class TestTidyColumns:
    def test_drops_unnamed_columns(self):
        df = pd.DataFrame(
            {
                "A": [1, 2, 3],
                "Unnamed: 0": ["x", "y", "z"],
                "Unnamed: 1": ["p", "q", "r"],
            }
        )
        result = tidy_columns(df)
        assert "Unnamed" not in result.columns
        assert list(result.columns) == ["A"]

    def test_drops_all_nan_columns(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [float("nan")] * 3})
        result = tidy_columns(df)
        assert "B" not in result.columns
        assert list(result.columns) == ["A"]

    def test_drops_all_nan_rows(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
        df.loc[1, ["A", "B"]] = float("nan")
        result = tidy_columns(df)
        assert len(result) == 2

    def test_preserves_non_nan_columns(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
        result = tidy_columns(df)
        pd.testing.assert_frame_equal(result, df)


class TestFormatTonnes:
    def test_formats_whole_number(self):
        assert format_tonnes(1000.0) == "1.000"

    def test_formats_decimal(self):
        # Python's :.0f rounds .56 up to 1235
        assert format_tonnes(1234.56) == "1.235"

    def test_formats_large_number(self):
        assert format_tonnes(1234567.89) == "1.234.568"

    def test_formats_zero(self):
        assert format_tonnes(0.0) == "0"

    def test_returns_str(self):
        assert isinstance(format_tonnes(1.5), str)


class TestFormatPercent:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0.0, "0,0%"),
            (0.5, "0,5%"),
            (0.123, "0,1%"),
            (-10.5, "-10,5%"),
        ],
    )
    def test_formats_percent(self, value, expected):
        assert format_percent(value) == expected

    def test_returns_str(self):
        assert isinstance(format_percent(0.5), str)


class TestYEARS:
    def test_years_range(self):
        assert YEARS == list(range(2010, 2025))


class TestMunicipalCoordinates:
    def test_campinas_coords(self):
        assert MUNICIPAL_COORDINATES["Campinas"] == (-22.9056391, -47.059564)

    def test_has_expected_number_of_municipalities(self):
        assert len(MUNICIPAL_COORDINATES) == 20
