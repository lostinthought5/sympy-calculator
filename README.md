# SymPy Calculator

A command-line calculator for arithmetic, trigonometry, and integration, made using [SymPy](https://www.sympy.org/). It evaluates expressions to four decimal places, integrates functions of **x**, and keeps a history of your session. 

## Features

- **Expression evaluation**: arithmetic, pi, e, trigonometric functions, log, sqrt, and other SymPy functions
- **Integral evaluation** with respect to x, shown with a + C for accuracy
- **Session history**: viewable earliest-to-present or present-to-earliest
- **Input validation with clear messages** for invalid characters, improper syntax, variables in a numeric expression, and undefined and complex results
- **Automated tests** with pytest

## Demo
 
```
Hello and welcome. This calculator may be used for basic math, trigonometry, and basic integrals!
 
(Menu) - What kind of calculation/option is needed?
Standard Expressions (e) | Integration (i) | History (h) | Exit (q) | e
 
(Standard Expressions) - Please enter your problem | Go Back (b): 2*pi
 
Solution: 6.2832
 
(Standard Expressions) - Please enter your problem | Go Back (b): 5
 
Single numbers are not allowed, please try again!
 
(Standard Expressions) - Please enter your problem | Go Back (b): b
 
(Menu) - What kind of calculation/option is needed?
Standard Expressions (e) | Integration (i) | History (h) | Exit (q) | i
 
(Integration) - Please enter your problem | Go Back (b): x^2
 
Solution: x**3/3 + C
```

## Getting started
 
**Requirements:** Python 3.10 or newer.
 
```bash
git clone git@github.com:lostinthought5/sympy-calculator.git
cd sympy-calculator
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 cli.py             # windows: python cli.py
```

## Usage
 
At the menu, choose between **e** (standard expressions), **i** (integration), **h** (history), or **q** (quit). Type **b** to go back once in a mode.
 
| Mode | Input | Result |
|------|----------|--------|
| Expression | 2*pi | 6.2832 |
| Expression | (2+3)*4 | 20.0000 |
| Expression | sin(pi/6) | 0.5000 |
| Integration | x^2 | x**3/3 + C |
| Integration | sin(x) + cos(x) | sin(x) - cos(x) + C |
| Integration | 1/x | log(x) + C |
 
**Input Rules**
 
- Use **\*** for multiplication (2*x, not 2x) and **^** or **\*\*** for powers.
- Log is defined to be the natural logarithm.
- Only numbers, operators, parentheses, letters, and . are accepted. Input is case-insensitive.
- Integration accepts functions of **x** only.

## Testing
 
```bash
# from the root directory
python3 -m pytest -v       # windows: python -m pytest -v
```
 
The tests cover the validity of inputted expressions as well as compute integer, decimal, and integral results. Integral results are verified by subtracting the computed result by the expected result to determine
whether it evaluates to zero. This is done to avoid strict output format comparison.  

## Project Structure
 
```
.
├── calculator.py           # math logic; input validation, parsing, evaluation, integration
├── cli.py                  # menus, user input, printing, session history
├── tests/
│   └── test_calculator.py  # pytests
├── requirements.txt
├── .gitignore
└── README.md
```

## Design Notes
 
- The logic and interface are separate, **calculator.py** handles the math logic and input validation without printing or calling the input() function. **cli.py** takes user inputs, calls the needed logic from **calculator.py**, and prints returned results along with other interface features. It's designed this way to test the math logic easily with pytest.

- Expressions are parsed twice, first as an unevaluated expression to parse over what the user actually typed. This is done so that something like **5** is rejected as a single number while **2+3** is allowed. Then, an evaluated expression is parsed through to confirm the proper **SymPy** expression is returned. This helps prevent undefined values like **1/0**, **0/0**, and **log(0)**, and complex values like **sqrt(-1)** from otherwise passing the validation logic.

## Known Limitations
 
- Parsing uses **SymPy**'s **sympify** function, which relies on Python's **eval**. A character whitelist restricts input, but it is not perfect. This project is meant strictly for local use, do not use with untrusted input.

- Since any **SymPy** function name like **exp()** and **atan()** is technicallly accepted and there is no time limit on calculations, some calculations may take an extensive amount of time.

- Complex results are generally rejected, but integrals that are complex only for some values of **x** like **sqrt(-1)** are not detected.

- Implicit multiplication like **2x** and **2pi** is not supported.
## Possible improvements
 
- Implementation of definite integrals and derivatives

- Implementation of algebraic manipulation

- Configurable numerical result precision for decimals

## Built With
 
Python, [SymPy](https://www.sympy.org/), [Pytest](https://pytest.org/)
