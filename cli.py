"""
This file is used to handle all printing and user inputs. It calls
functions from calculator.py to retrieve answers, and also lets the
user know if there was a problem with their input. 
"""

from calculator import CalculationError, evaluate_expr, integrate_expr
from collections.abc import Callable

class Session():
    def __init__(self):
        self.history: list[str] = []
        self.current_option: str | None = None
        self.active = True

        self.option_types: dict[str, str] = {
            'e' : "(Standard Expressions)",
            'i' : "(Integration)",
            'h' : "(History)",
        }

        self.accepted_inputs: dict[str, Callable] = {
            'e' : lambda: self.solution_handler('e'),
            'i' : lambda: self.solution_handler('i'),
            'h' : self.history_handler,
            'q' : self.quit,
        }

    def start(self): # this begins the session
        print('Hello and welcome. This calculator may be used for basic math, trigonometry, and basic integrals!\n')
        
        user_input = ""
        while self.active:
            if not self.current_option:
                print("(Menu) - What kind of calculation/option is needed?")
                user_input = input("Standard Expressions (e) | Integration (i) | " 
                                    "History (h) | Exit (q) | ").strip().lower()  # corrects input

                if not (user_input in self.accepted_inputs):
                    print("Please enter a valid option!\n")
                    continue

                print()

                func = self.accepted_inputs[user_input]
                if user_input == 'q':
                    func()
                    continue

                self.current_option = self.option_types[user_input]

            self.accepted_inputs[user_input]()

    def quit(self):
        print("Thank you for using me! Good bye!\n")
        self.active = False

    def withdraw(self):
        print()  # terminal spacing
        self.current_option = None

    def solution_handler(self, input_type: str):  # input_type = e or i
        solution_methods: dict[str, Callable] = {
            'e' : evaluate_expr,
            'i' : integrate_expr,
        }

        user_problem: str = input(f"{self.current_option} - Please enter your problem | Go Back (b): ").strip().lower()
        print()
        
        try:
            if user_problem == 'b': 
                self.withdraw()
                return

            func = solution_methods[input_type]
            answer = func(user_problem)

        except CalculationError as error:
            print(f"{error}\n")

        else:
            final_output = f"{answer:.4f}" if input_type == 'e' else f"{answer} + C"

            print(f"Solution: {final_output}\n")
            self.history.append(f"Input = {user_problem} - Solution = {final_output}")

    def history_handler(self):
        if not self.history:
            print("There are no recorded problem entries yet!\n")
            self.withdraw()
            return

        array_types : dict[str, list[str]] = {
            'e' : self.history, 
            'l' : self.history[::-1],
        }

        # can just print History here
        print("(History) - Would you like to:")
        user_input = input("Display Earliest Entries (e) | Latest Entries (l) "
                            "| Go Back (b): ").strip().lower()
        print()

        if user_input == 'b':
            self.withdraw()
            return
        elif user_input not in array_types:
            print("Please input a valid history option!")
            return

        print("History:")

        for entry in array_types[user_input]:
            print(entry)

        print()

if __name__ == '__main__':
    session = Session()
    session.start()