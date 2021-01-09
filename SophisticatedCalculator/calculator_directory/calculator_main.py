# Imports:
import re
import calculator_directory.calculations as calculate
import calculator_directory.equation_validation as is_valid
import calculator_directory.calculator_operators as operators
import sys


# Checking that the equation can be calculated and if it can be calculated,
# then calling the matching functions from calculations and printing the
# result to the user:
def calculate_equation(equation):
    # Converting the string to a list that contains operators (as chars),
    # parentheses and numbers:
    equation_list = calculate.string_to_list(equation)

    # Setting the operators in the list by converting the operators from
    # a string to their matching value from the dictionary):
    equation_list = calculate.set_operators_in_list(equation_list)

    # Checking if the equation can be calculated:
    if is_valid.check_equation_validity(equation_list):
        # Calculating and printing the value:
        value = calculate.solve_equation(equation_list)
        if value is not False:
            print(calculate.solve_equation(equation_list))

    # The equation can't be calculated - letting the user know:
    else:
        print("The calculator doesn't know how to"
              " calculate the equation you entered.")


# Printing some details regarding the program to the user which will help
# him understand how to use it better. Also Using ', '.join to print the
# operators lists values in a way which will be easy for the user to see:
def print_opening_message():
    print('Welcome to the 🅂🄾🄿🄷🄸🅂🅃🄸🄲🄰🅃🄴🄳 🄲🄰🄻🄲🅄🄻🄰🅃🄾🅁!')
    print('Enter any equation and the calculator will solve it for you.\n'
          'The calculator knows how to handle integers, operators and '
          'parentheses from the type ().')
    print('\n ---- Program Information ----')
    print('(*) Enter a regular equation if you would like the calculator to '
          'solve it for you.\n'
          '(*) Press h+enter to see what every operator does.\n'
          '(*) Press x+enter to exit the program.')
    print('\n ---- Operators Information ----')
    print('(*) The following operators can be used in the format {num '
          'operator '
          'num}: ' +
          ', '.join([val[0] for val in operators.operator_tuple_dict.keys() if
                     val[2] == 'num op num']))
    print('(*) The following operator(s) can be used in the format {num '
          'operator}: ' +
          ', '.join([val[0] for val in operators.operator_tuple_dict.keys() if
                     val[2] == 'num op']))
    print('(*) The following operator(s) can be used in the format {operator '
          'num}: ' +
          ', '.join([val[0] for val in operators.operator_tuple_dict.keys() if
                     val[2] == 'op num']))
    print('\nYou can now enter any equation and the sophisticated calculator '
          'will solve it for you!')


# The program's main function - using an endless loop to continuously
# ask the user to input equations and then print the equations sum/an error
# message in return to the user's input:
def main():
    # Printing the opening message of the program:
    print_opening_message()
    while True:
        # Asking the user to input an equation to calculate:
        equation = input("Enter an equation: ")
        # Removing unwanted white spaces, new lines and tabs from the
        # input:
        equation = re.sub(' +|[\n\t]', '', equation)

        # Ending the program's run:
        if equation == "x":
            sys.exit()
        # Printing the information regarding every operator:
        elif equation == "h":
            for item in operators.operator_information_dict:
                print(str(operators.operator_information_dict.get(item)))
            print('')
        # Checking if the equation we received is valid and calculating it:
        else:
            # Checking the validity of the equation's string:
            if is_valid.check_string_validity(equation):
                # Calling the calculate_equation function which checks if the
                # equation can be calculated and prints the result of the
                # calculation:
                calculate_equation(equation)

            # The equation that the user inputted isn't valid and therefore
            # can't be calculated:
            else:
                print("The equation you entered isn't valid,"
                      " please check it and try again.")


# Calling the main function of this program:
main()
