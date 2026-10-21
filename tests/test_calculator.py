from calculator import CalculationError, evaluate_expr, integrate_expr
from sympy import simplify, sympify, symbols
import pytest

general_inputs = ["sin", "cosxx", "+1-", "x.y", "2+", "x + a", 
                 "1=1", "afdfa", "1/0", "sqrt(-1)", "", " ", "y"]

@pytest.mark.parametrize("text", general_inputs)
def test_invalid_evaluate_input(text):
    with pytest.raises(CalculationError):
        evaluate_expr(text)

@pytest.mark.parametrize("text", general_inputs)
def test_invalid_integration_input(text):
    with pytest.raises(CalculationError):
        integrate_expr(text)

@pytest.mark.parametrize("text, expected", [("2 + 3", 5), ("1 - 0 + 9", 10), ("9^2 + 3", 84), ("1+5 - 3*4", -6)])
def test_integer_results(text, expected):
    assert evaluate_expr(text) == expected

@pytest.mark.parametrize("text, expected", [("2 * pi", 6.2832), ("pi + e", 5.8598), ("1/5 + 3/4", 0.9500)])
def test_decimal_results(text, expected):
    assert float(evaluate_expr(text)) == pytest.approx(expected, abs = 1e-4)

x = symbols('x', real = True)
@pytest.mark.parametrize("text, expected", [("x^2", "x**3/3"), ("sin(x) + cos(x)", "sin(x) - cos(x)"), 
                                            ("sqrt(x) - 1/x", "2*x**(3/2)/3 - log(x)")])
def test_integral_results(text, expected):
    """expected var converted to expression, then subtracted by what
    is calcualted; should give zero if equal"""

    result = integrate_expr(text)
    assert simplify(result - sympify(expected, locals = {'x' : x})) == 0  # does not include C