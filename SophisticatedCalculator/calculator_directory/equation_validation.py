# Imports:
import calculator_directory.calculator_operators as calc
import numbers


# Checking the operators "order" in the string. Preventing the user from
# inputting equations such as '5----5' or '5**5' while allowing the user to
# input equations such as '5--5' / '5*5' since those are valid and solvable:
def check_operator_count(equation_string):
    counter = 0
    flag = True
    operators_list = [val[0] for val in calc.operator_tuple_dict.keys() if
                      val[2] == 'num op num']
    for index, value in enumerate(equation_string):
        if value in operators_list:
            # if it's mid run then:
            if index > 0 and counter > 0:
                # if we have a match - ruling out the expression
                if equation_string[index - 1] in operators_list and value != \
                        '-':
                    flag = False
                # if we have a match between '+'/'-' we need at least 3 to
                # rule out the expression:
                if equation_string[index] == '-':
                    # We will only get here when the counter is already 2
                    # and should be updated to 3, therefore we set the
                    # statement to counter >= 2:
                    if counter >= 2:
                        flag = False
                    else:
                        counter = counter + 1
                else:
                    if counter >= 2:
                        flag = False
            # index is either 0 or the current value isn't the same as the
            # previous then counter is set to 1 again:
            else:
                counter = 1
        else:
            counter = 0

    return flag


# Using the list data structure as a stack to store parentheses and pop them
# accordingly. Whenever we see an opening parentheses - '(', the value will
# be added to the stack, and whenever we see a closing parentheses - ')',
# we will pop the stack. If we receive an error in the attempt to pop the
# stack, then there aren't enough opening parentheses therefore we will
# return False. Also, if the stack isn't empty at the end - returning False,
# because there are too many opening parentheses and not enough closing
# parentheses.
def check_balanced_parentheses(equation_string):
    # Variable Definition - Empty "stack" list:
    stack = []

    # Going through the entire string and when we see a parentheses, either
    # adding it to the "stack" or popping the "stack":
    for parentheses in equation_string:
        if parentheses == '(':
            stack.append(parentheses)
        elif parentheses == ')':
            try:
                stack.pop()
            # Returning False because there aren't enough opening parentheses:
            except IndexError:
                return False

    # Output will be False if there are too many opening parentheses,
    # or True if the length is 0 which means that all the opening
    # parentheses have a matching closing parentheses in the string:
    return len(stack) == 0


# Returning True if the equation_list received is valid, or False if it isn't.
# Checking all the end cases related to operators being close to parentheses:
def check_operators_close_to_parentheses_validity(equation_list):
    # Variables Definition - defining a "flag" which will help us determine
    # at the end whether the equation_list is valid or not and 2 lists
    # containing: 1. ops_list_without_num_op - All the operators except
    # operators with the format 'num op'. 2. ops_list_without_op_num - All
    # the operators except operators with the format 'op num'.
    flag = True
    ops_list_without_num_op = [val for val in calc.operator_tuple_dict.keys()
                               if val[2] != 'num op']
    ops_list_without_op_num = [val for val in calc.operator_tuple_dict.keys()
                               if val[2] != 'op num']

    # Going through the entire list - each time storing the index and value
    # of the current position in the list:
    for index, value in enumerate(equation_list):
        # Checking cases related to the opening parentheses:
        if value == '(':
            # Before parentheses we expect to receive an operator which is
            # from the type 'op num' or 'num op num':
            if index > 0 and equation_list[
                index - 1] not in ops_list_without_num_op and \
                    equation_list[index - 1] != '(':
                flag = False

            # The inside of the parentheses must start with either an
            # operator from the type 'op num' or with a number:
            elif equation_list[index + 1] != '(' and equation_list[
                index + 1] in ops_list_without_op_num and \
                    not isinstance(equation_list[index + 1], numbers.Number):
                flag = False

        # Checking cases related to the closing parentheses:
        elif value == ')':
            # After parentheses we expect to ALWAYS receive an operator with
            # the format 'num op num' / 'num op' or a closing parentheses:
            if index < len(equation_list) - 1 and equation_list[
                index + 1] != ')' and \
                    equation_list[index + 1] not in ops_list_without_op_num:
                flag = False

            # Before the end of the parentheses we expect to receive
            # an operator from the type 'num op' or a number:
            elif equation_list[index - 1] in ops_list_without_num_op and \
                    equation_list[index - 1] != '(' and \
                    not isinstance(equation_list[index - 1], numbers.Number):
                flag = False

    # Returning the flag which should be True if the equation is valid
    # or False if the equation isn't valid:
    return flag


# Checking end cases for each of the different types of operators
# and returns whether the equations are valid or not:
def check_operators_validity(equation_list):
    flag = True
    num_op_num = [val for val in calc.operator_tuple_dict.keys() if
                  val[2] == 'num op num']
    num_op = [val for val in calc.operator_tuple_dict.keys() if
              val[2] == 'num op']
    op_num = [val for val in calc.operator_tuple_dict.keys() if
              val[2] == 'op num']

    # Saving the minus operator:
    minus_operator = \
        [val for val in calc.operator_tuple_dict.keys() if val[0] == '-'][0]

    for index, value in enumerate(equation_list):
        # Checking num_op_num operators:
        if value in num_op_num:
            if 0 < index < len(equation_list) - 1:
                # We expect to receive a number/num_op/) before a num_op_num
                # operator and to receive a number/)/op_num after a num_op_num:
                if not (isinstance(equation_list[index - 1], numbers.Number) or
                        equation_list[index - 1] == ')' or
                        equation_list[index - 1] in num_op) or not \
                        (equation_list[index + 1] == '(' or isinstance(
                            equation_list[index + 1], numbers.Number) or
                         equation_list[index + 1] in op_num):
                    flag = False
            elif 0 < index:
                # We can't have a num_op_num at the end of the list:
                if index == len(equation_list) - 1:
                    flag = False
                # We expect to receive a )/number/num_op before a num_op_num
                # operator:
                elif not (isinstance(equation_list[index - 1],
                          numbers.Number) or equation_list[index - 1] == ')' or
                          equation_list[index - 1] in num_op):
                    flag = False
            elif index < len(equation_list) - 1:
                # We can't have a num_op_num at the beginning of the list:
                if index == 0:
                    flag = False
                # We expect to receive a (/number/op_num operator after a
                # num_op_num operator:
                elif not (equation_list[index + 1] == '(' or
                          isinstance(equation_list[index + 1],
                          numbers.Number) or
                          equation_list[index + 1] in op_num):
                    flag = False

        # Checking num_op operators:
        if value in num_op:
            if 0 < index < len(equation_list) - 1:
                # We expect to receive a number/)/num_op before a num_op
                # operator and a )/number/num_op/num_op_num after it:
                if not (isinstance(equation_list[index - 1], numbers.Number) or
                        equation_list[index - 1] == ')' or
                        equation_list[index - 1] in num_op) or not \
                        (equation_list[index + 1] == ')' or
                         isinstance(equation_list[index + 1],
                         numbers.Number) or
                         equation_list[index + 1] in num_op or
                         equation_list[index+1] in num_op_num):
                    flag = False
            elif 0 < index:
                # We expect to receive a number/)/num_op before a num_op
                # operator:
                if not (isinstance(equation_list[index - 1], numbers.Number) or
                        equation_list[index - 1] == ')' or
                        equation_list[index - 1] in num_op):
                    flag = False

            elif index < len(equation_list) - 1:
                # We can't have a num_op_num at the beginning of the list:
                if index == 0:
                    flag = False
                # We expect to receive a )/number/num_op/num_op_num operator
                # after an op_num operator:
                if not (equation_list[index + 1] == '(' or
                        isinstance(equation_list[index + 1], numbers.Number) or
                        equation_list[index + 1] in num_op or
                        equation_list[index + 1] in num_op_num):
                    flag = False

        # If the value is in the op_num operators:
        if value in op_num:
            if 0 < index < len(equation_list) - 1:
                # We expect to receive num_op_num operator/( before an op_num
                # operator and to receive a number/( after it:
                if not (isinstance(equation_list[index + 1], numbers.Number) or
                        equation_list[index + 1] == '(') or not \
                        (equation_list[index - 1] in num_op_num or
                         equation_list[index-1] == '('):
                    flag = False
            elif 0 < index:
                # We can't have a op_num at the end of the list:
                if index == len(equation_list) - 1:
                    flag = False
                # We expect to receive a num_op_num operator before an
                # op_num operator:
                if not (equation_list[index - 1] in num_op_num or
                        equation_list[index-1] == '('):
                    flag = False
            elif index < len(equation_list) - 1:
                # We expect to receive a number/( after an op_num operator:
                if not (isinstance(equation_list[index + 1], numbers.Number) or
                        equation_list[index + 1] == '('):
                    flag = False
    return flag


# Returns whether a string input is valid or not. Only allowing the user to
# input numbers, operators and parentheses, which have to start by either a
# minus sign, a parentheses or a number [An equation can start with
# -(op_num/number) OR '(' OR number]. Also, only entering an operator as an
# equation isn't valid - therefore blocking it:
def check_string_input(equation_string):
    # First - creating an operators list that contains each of the values:
    operators_list = [val[0] for val in calc.operator_tuple_dict.keys()]
    operators_list_not_op_num = [val[0] for val in
                                 calc.operator_tuple_dict.keys() if
                                 val[2] != 'op num']
    parentheses_list = ['(', ')']

    # Creating a list with the available options for the first index in the
    # equation:
    opening_list = [val[0] for val in calc.operator_tuple_dict.keys() if
                    val[2] == 'op num']
    opening_list.append('-')
    opening_list.append('(')

    # A valid equation must begin with a minus, a parentheses or a number:
    if equation_string[0] in opening_list or equation_string[0].isdigit():
        # If there are more than 2 items in the equation, and the first in
        # them is a minus, we need to check that there isn't an operator
        # with the format 'num op num' or 'num op' after it:
        if len(equation_string) > 1 and equation_string[0] == '-':
            if equation_string[1] in operators_list_not_op_num:
                return False

        # Disabling the user's option to input an operator as an equation:
        if any(val in operators_list for val in equation_string):
            if len([val for val in equation_string if val.isdigit()]) == 0:
                return False

        # Returning whether all the values in the string are valid or not:
        return all(
            [c.isdigit() or c in operators_list or c in parentheses_list for c
             in equation_string])
    # Returning False if the equation didn't begin with a proper value:
    else:
        return False


# Checking whether there are duplicates of parentheses in the
# equation_string or not. If there aren't then returning True, if there are
# then returning False. For example: ((5+4)) -> False, ((5+4)+3) -> True:
def check_parentheses_validity(equation_string):
    # Creating a stack of characters:
    stack = []

    # Going through the equation:
    for val in equation_string:
        # If the current character is a closing parenthesis:
        if val == ')':
            # Popping a character from the stack:
            top = stack.pop()

            # Storing the amount of values in the parentheses. If the count
            # will be less than/equal to 1 then there are unnecessary
            # parentheses:
            values_in_parentheses = 0
            while top != '(':
                values_in_parentheses += 1
                top = stack.pop()

            if values_in_parentheses < 1:
                return False

        # Pushing an opening parentheses '(', operators and operands to stack:
        else:
            stack.append(val)

    # No duplicates were found:
    return True


# Returns whether the string is valid. This means that the string starts
# with -number/(/number, it has balanced parentheses (all of it's opening
# parentheses have a matching closing parentheses) and the string doesn't
# contain operators which are being used in a wrong way (for example,
# number~ won't be valid because we expect to get a number after the ~). In
# addition, an empty string isn't valid as is a string that contains
# unnecessary parentheses (For example: ((5+5)) isn't valid):
def check_string_validity(equation_string):
    return len(equation_string) > 0 and check_string_input(equation_string) \
           and check_balanced_parentheses(equation_string) and \
           check_operator_count(equation_string) and \
           check_parentheses_validity(equation_string)


# Returns whether the received equation string which was transferred to a list
# is solvable (True) or not (False):
def check_equation_validity(equation_list):
    return check_operators_validity(equation_list) and \
           check_operators_close_to_parentheses_validity(equation_list)
