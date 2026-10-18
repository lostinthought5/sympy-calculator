from calculator import CalculationError, evaluate_expr, integrate_expr, option_types, SympifyError
from re import match

class Session():
    def __init__(self):
        self.history: list = []
        self.active: bool = True
        self.current_option: str = None

        self.accepted_inputs: dict[str, Callable] = {
	        'e' : lambda: self.solution_handler('e'),
	        'i' : lambda: self.solution_handler('i'),
	        'h' : self.history_handler,
	        'q' : self.quit,
        }

    def start(self):
        print('Hello and welcome. This calculator may be used for basic math, trigonometry, and basic integrals!\n')
        
        user_input: str = "" # done to update the var rather than define per iteration
        while self.active:
            if not self.current_option:
                print("(Menu) - What kind of calculation/option is needed?")
                user_input = input("Standard Expressions - (e) | Integration (i) | " 
                                    "History (h) | Exit (q) | ").strip().lower() # corrects input

                if not (user_input in self.accepted_inputs):
                    print("Please enter a valid option!\n")
                    continue

                print()

                func = self.accepted_inputs[user_input]
                if user_input == 'q':
                    func()
                    continue

                self.current_option = option_types[user_input]

            self.accepted_inputs[user_input]()

    def quit(self):
        print("Thank you for using me! Good bye!\n")
        self.active = False

    def withdraw(self):
        print() # terminal spacing
        self.current_option = None

    def is_valid_input(self, user_input: str) -> bool:
        new_input = user_input.replace(" ", "").strip() # this removes all spacing whether visible or not
        
        # using regex here; only permitted characters
        return match(r'^[0-9x\+\-\*\/\^\(\)\.a-zA-Z]+$', new_input)

    def solution_handler(self, input_type: str): # input_type = e or i
        solution_methods: dict[str, Callable] = {
            'e' : evaluate_expr,
            'i' : integrate_expr,
        }

        user_problem: str = input(f"{self.current_option} - Please enter your problem | Go Back (b): ").strip().lower()
        print()
        
        if not (self.is_valid_input(user_problem)):
            print("Invalid characters detected; only numbers, operators, letters, and parenthesis permitted!\n")
            return
        
        try:
            if user_problem == 'b': 
                self.withdraw()
                return

            func = solution_methods[input_type]
            answer = func(user_problem)

        except SympifyError:
            print("Invalid syntax detected; make sure your problem follows standard formatting!\n")

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

        array_types : dict[str, list] = {
            'e' : self.history, 
            'l' : reversed(self.history),
        }

        # can just print History here since it is guaranteed to be that option
        print("(History) - Would you like to:")
        user_input = input("Display Earliest Entries (e) | Latest Entries (l) "
                            "| Go Back (b): ").strip().lower()
        print()

        if user_input == 'b':
            self.withdraw()
            return
        elif not user_input in array_types:
            print("Please input a valid history option!")
            return

        print("History:")

        for entry in array_types[user_input]:
            print(entry)

        print()

if __name__ == '__main__':
    session = Session()
    session.start()