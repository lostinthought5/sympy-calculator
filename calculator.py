from sympy import sin, cos, tan, log, pi, sympify, integrate, E, sqrt, symbols, I, Integral
from sympy.core.numbers import ComplexInfinity, NaN
from sympy.core.sympify import SympifyError

class CalculationError(Exception):
	pass

operations: dict[str, object] = {
	'pi' : pi,
	'e' : E,
	'sin' : sin,
	'cos' : cos,
	'tan' : tan,
	'log' : log,
	'sqrt' : sqrt,
}

option_types: dict[str, str] = {
	'e' : "(Standard Expressions)",
	'i' : "(Integration)",
	'h' : "(History)",
}

def _parser():
	pass

def evaluate_expr(text: str):
	# the documentation says sympify uses eval(); avoid in production
	expression: object = sympify(text, locals = operations, evaluate = False)

	if expression.is_Number:
		raise CalculationError("Single numbers are not allowed, please try again!")
	
	if expression.free_symbols: # this checks for non-numerical characters
		raise CalculationError("Variables are not allowed in standard expressions, please try again!")

	answer: object = sympify(text, locals = operations) # evaluates for the actual answer

	if isinstance(answer, (ComplexInfinity, NaN)): # checks whether var corresponds to classes representing infinity
		raise CalculationError("Your expression is undefined, please try again!")

	if answer.is_real is False:
		raise CalculationError("Complex numbers are not allowed, please try again!")
	elif answer.is_real is None: # .is_real is None when sympy can't determine
		raise SympifyError("")

	return answer


def integrate_expr(text: str):
	allowed = operations.copy()

	x = symbols('x', real = True) # must clarify x is real, otherwise .is_real logic works differently
	allowed['x'] = x

	expression = sympify(text, locals = allowed)

	if expression.free_symbols - {x}: 
		raise CalculationError("Only syntax in terms of functions of x is accepted, please try again!")

	if isinstance(expression, (ComplexInfinity, NaN)):
		raise CalculationError("Your expression is undefined, please try again!")

	answer = integrate(expression, x)

	if isinstance(answer, Integral): # will be invalix syntax
		raise SympifyError("")
	
	if answer.has(I): # checks for imaginary numbers
		raise CalculationError("Complex numbers are not allowed, please try again!")

	return answer