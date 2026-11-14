"""Tests for temp_convert (run: python -m pytest test_temp_convert.py -q)."""

import io

import pytest

from temp_convert import c_to_f, f_to_c, format_result, main, parse_finite


def run(argv, stdin_text=""):
    out, err = io.StringIO(), io.StringIO()
    code = main(argv, stdin=io.StringIO(stdin_text), stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


# --- business logic layer ---------------------------------------------------

def test_logic_conversions():
    assert c_to_f(100) == 212
    assert f_to_c(212) == 100
    assert c_to_f(-40) == -40


def test_logic_parse_finite():
    assert parse_finite(" 12.5 ") == 12.5
    for bad in ["abc", "", "nan", "inf", "-inf", "infinity", "1e999", "1_0", "١٠٠"]:
        with pytest.raises(ValueError):
            parse_finite(bad)


# --- CLI layer ---------------------------------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [("100", "212.00"), ("0", "32.00"), ("-40", "-40.00")],
)
def test_c_to_f_one_shot(value, expected):
    code, out, err = run(["--c-to-f", value])
    assert (code, out, err) == (0, expected + "\n", "")


@pytest.mark.parametrize(
    "value,expected",
    [("212", "100.00"), ("32", "0.00"), ("-40", "-40.00")],
)
def test_f_to_c_one_shot(value, expected):
    code, out, err = run(["--f-to-c", value])
    assert (code, out, err) == (0, expected + "\n", "")


def test_interactive_converts():
    code, out, err = run([], "100 C\n100 c\n100C\n212 F\n  212f  \nq\n")
    assert code == 0
    assert err == ""
    assert out.count("212.00 F") == 3
    assert out.count("100.00 C") == 2


@pytest.mark.parametrize(
    "stdin_text,expected",
    [
        ("q\n100 C\n", 0),
        ("Q\n100 C\n", 0),
        ("\n100 C\n", 0),
        ("100 C\nq\n", 1),
        ("100 C\n", 1),
        ("q\n", 0),
        ("Q\n", 0),
        ("\n", 0),
        ("", 0),
    ],
)
def test_interactive_exit_forms(stdin_text, expected):
    code, out, err = run([], stdin_text)
    assert code == 0
    assert "Traceback" not in err
    assert out.count("212.00 F") == expected


def test_c_to_f_exponent_form():
    assert run(["--c-to-f=-1e2"]) == (0, "-148.00\n", "")


def test_interactive_bad_input_reprompts():
    code, out, err = run([], "abc\n100 K\n1e308 C\n١٠٠ C\n100 C\nq\n")
    assert code == 0
    assert len(err.strip().splitlines()) == 4
    # session continued after the errors and still converted
    assert "212.00 F" in out
    assert "1.8e+308" not in out and "inf" not in out


@pytest.mark.parametrize(
    "flag,value",
    [
        (flag, value)
        for flag in ("--c-to-f", "--f-to-c")
        for value in ("abc", "nan", "inf", "1e999", "1_0", "١٠٠")
    ]
    # 1e308 C overflows to infinity in Fahrenheit; 1e308 F stays finite in Celsius
    + [("--c-to-f", "1e308")],
)
def test_bad_value_one_shot(flag, value):
    code, out, err = run([flag, value])
    assert code != 0
    assert err.strip() != ""
    assert out == ""


@pytest.mark.parametrize(
    "argv",
    [["--c-to-f", "1", "--f-to-c", "1"], ["--bogus"], ["100"], ["--c-to-f"]],
)
def test_bad_invocation(argv):
    code, out, err = run(argv)
    assert code != 0
    assert err.strip() != ""
    assert out == ""


@pytest.mark.parametrize(
    "argv,expected",
    [(["--c-to-f", "-17.7777778"], "0.00"), (["--f-to-c", "32"], "0.00")],
)
def test_negative_zero_normalised(argv, expected):
    code, out, err = run(argv)
    assert (code, out) == (0, expected + "\n")
    assert format_result(-0.001) == "0.00"
    assert format_result(-0.0) == "0.00"
    assert format_result(-0.5) == "-0.50"


def test_help_text():
    code, out, err = run(["--help"])
    assert code == 0
    assert "--c-to-f" in out and "--f-to-c" in out
    assert "interactive" in out.lower()
    assert "--c-to-f 100" in out and "--f-to-c 212" in out
