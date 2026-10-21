"""
This file handles the math logic. It takes user input and raises
errors to cli.py if needed, otherwise it returns the corresponding 
answer to cli.py
"""

from sympy import sympify, integrate, E, symbols, I, Integral, Expr
from sympy.core.numbers import ComplexInfinity, NaN
from sympy.core.sympify import SympifyError
from re import match

class CalculationError(Exception):
    """This is used to fetch errors in the cli.py file"""

name_overrides: dict[str, object] = { # this is to attribute the correct sympy object
    'e' : E,
}

def _parse(text: str, names: dict, evaluate: bool = True):
    # this is to simplify syntax error catches
    try:
        # the documentation says sympify uses eval(); avoid in production
        result = sympify(text, locals = names, evaluate = evaluate)
        
    except (SympifyError, AttributeError, TypeError) as error: # all occur from improper syntax
        raise CalculationError("Invalid syntax, please try again!") from error
        
    if not isinstance(result, Expr):  # this happens when a math function alone is inputted
        raise CalculationError("No arguments given, please try again!")
    return result

def is_valid_input(text: str) -> bool:
    new_input = text.replace(" ", "").strip()  # removes all spacing whether visible or not
        
    # using regex here; only permitted characters
    return match(r'^[0-9x\+\-\*\/\^\(\)\.a-zA-Z]+$', new_input) is not None

def evaluate_expr(text: str) -> Expr:
    """Evaluates a numeric expression typed by the user. It raises
    CalculationError if the text has invalid characters, syntax,
    contains variables, is undefined, or gives a complex result.
    """

    if not is_valid_input(text):
        raise CalculationError("Invalid characters detected; only numbers, operators, letters, and parenthesis permitted!")

    expression = _parse(text, name_overrides, evaluate = False)   

    if expression.is_Number:
        raise CalculationError("Single numbers are not allowed, please try again!")
    
    if expression.free_symbols:  # this checks for non-numerical characters
        raise CalculationError("Variables are not allowed in standard expressions, please try again!")

    answer = _parse(text, name_overrides)  # evaluates for the actual answer

    if isinstance(answer, (ComplexInfinity, NaN)):  # inputs like 1/0, 0/0, log(0)...
        raise CalculationError("Your expression is undefined, please try again!")

    if answer.is_real is False:
        raise CalculationError("Complex numbers are not allowed, please try again!")
    elif answer.is_real is None:  # .is_real is None when sympy can't determine
        raise CalculationError("Invalid syntax, please try again!")

    return answer

def integrate_expr(text: str) -> Expr:
    """
    Integrates an expression typed by the user. It raises
    CalculationError if the text has invalid characters, syntax,
    contains variables other than x, is undefined, or gives 
    a complex result.
    """

    if not is_valid_input(text):
            raise CalculationError("Invalid characters detected; only numbers, operators, letters, and parenthesis permitted!")

    allowed = name_overrides.copy()

    x = symbols('x', real = True)
    allowed['x'] = x

    expression = _parse(text, allowed)

    if expression.free_symbols - {x}: 
        raise CalculationError("Only syntax in terms of functions of x is accepted, please try again!")

    if isinstance(expression, (ComplexInfinity, NaN)):
        raise CalculationError("Your expression is undefined, please try again!")

    answer = integrate(expression, x)

    if isinstance(answer, Integral):  # will be invalid syntax
        raise CalculationError("Invalid syntax, please try again!")
    
    if answer.has(I):  # checks for imaginary numbers
        raise CalculationError("Complex numbers are not allowed, please try again!")

    return answer