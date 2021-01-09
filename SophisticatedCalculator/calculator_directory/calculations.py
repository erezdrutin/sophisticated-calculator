# Imports:
import calculator_directory.calculator_operators as calc
import re
import numbers


# Fixing an "end case" error that occur because of the regex we're using.
# The regex we're using isn't capable of handling a case on which we receive
# an equation such as 4!-3 correctly because it treats the 3 as a -3. This
# function is used to separate num op operators from the minus operator,
# which will then allow us to correctly calculate the equation's sum:
def separate_num_op_format(result_list):
    operators_and_parentheses = [val[0] for val in
                                 calc.operator_tuple_dict.keys() if
                                 val[2] == 'num op']
    operators_and_parentheses.append(')')
    for index, value in enumerate(result_list):
        # Checking that the current value we're standing on is an operator
        # and it's format of input is num op, which is the case that is
        # causing errors to our regex:
        if index < len(result_list) - 1 and \
                result_list[index] in operators_and_parentheses:
            if isinstance(result_list[index + 1], numbers.Number):
                # if the value is negative then:
                if result_list[index + 1] < 0:
                    # Setting the value to positive and then adding the '-'
                    # sign before:
                    result_list[index + 1] = -result_list[index + 1]
                    result_list.insert(index + 1, '-')  # Adding the '-'
    return result_list


# Creating a list which contains the values from the equation string. The
# list's cells will contain parentheses, operators and values:
def string_to_list(equation_string):
    # Removing any unwanted white spaces, tabs, or new lines from the
    # equation string:
    equation_string = re.sub(r"[\n\t\s]*", "", equation_string)

    # Creating a list based on the equation string. The list will contain
    # values, operators and parentheses:
    result_list = re.findall(r'\b-\b|-?\d+|\D', equation_string)

    # Converting all the values in a list to floats from strings, and leaving
    # the values that can't be converted to a float
    for i in range(0, len(result_list)):
        # Trying to set each value to a number. If it's unsuccessful,
        # then leaving it unchanged (because it's either an operator or a
        # parentheses):
        try:
            result_list[i] = float(result_list[i])
        except ValueError as e:
            result_list[i] = result_list[i]

    result_list = separate_num_op_format(result_list)
    # Returning the list we received from the equation string:
    return result_list


# Updating the result_list to contain the operators inside it, which will
# later allow us to run through the list without having to call outside
# functions each time to get a matching tuple from the dictionary for each
# operator:
def set_operators_in_list(equation_list):
    # Getting the full list of operators as tuples (Key, Power Rank):
    operators_list = calc.operator_tuple_dict.keys()

    # Updating the operators list to contain the tuples of those that appear
    # in the equation_list:
    operators_list = [value for value in operators_list if
                      value[0] in equation_list]

    # Updating equation_list to contain tuples of operators instead of
    # characters of operators:
    for index, value in enumerate(equation_list):
        for y in operators_list:
            if value == y[0]:
                equation_list[index] = y

    # Returning the updated list:
    return equation_list


# Returning a list of operators in the form of (Key Tuple, Lambda Function)
# that also appear in a list. The list will contain the dictionary items
# that match those operators:
def get_operators_from_list(equation_list):
    # Creating an empty operators list:
    operators_list = []

    # Updating operators_list to contains values from the dictionary (Key
    # Tuple, Lambda Function):
    for val in equation_list:
        if val in calc.operator_tuple_dict.keys():
            operators_list.append((val, calc.operator_tuple_dict.get(val)))

    # Returning the operators list:
    return operators_list


# Returning the operator with the highest power rank, or the first instance
# of it (if an operator exists twice, the first instance of it will be
# returned):
def get_strongest_operator_by_power_rank(operators_list):
    try:
        max_operator = operators_list[
            0]  # Setting the max_operator to the first operator.
        # item = an operator instance from the dictionary (tuple, function):
        for item in operators_list:
            if item[0][1] > max_operator[0][1]:
                max_operator = item  # updating max_operator
        return max_operator
    except IndexError:
        return False


# Returns the indexes of uninterrupted parentheses in the equation
# by using a for loop to go through the entire equation_list while at each
# time looking for an opening parentheses and a closing parentheses
# that aren't "interrupted" by another opening parentheses:
def get_indexes_of_parentheses(equation_list):
    # Defining 2 variables to store the start & end indexes of the parentheses:
    start_index = 0
    end_index = 0

    # Running through the entire list, when in the end we will get the
    # indexes of uninterrupted parentheses from the RIGHT side of the equation.
    for i in range(0, len(equation_list)):
        if equation_list[i] == '(':
            start_index = i
            i = i + 1
            while equation_list[i] != ')':
                # Going towards the next index as long as we don't get
                # another opening parentheses:
                if equation_list[i] != '(':
                    i = i + 1
                    end_index = i
                # We got another opening parentheses, therefore updating
                # the starting index of the parentheses and continuing
                # to run through the list:
                else:
                    start_index = i  # Updating the start index.
                    i = i + 1

    # Returning a tuple that contains the index of the
    # beginning of the parentheses and the end of them:
    return start_index, end_index


# Removes values in range of indexes from a list. The function uses a for
# loop to go through all the values in the received range of values and
# deletes those value from the received list:
def remove_values_in_range_from_list(equation_list, parentheses_indexes):
    # Deleting the value at the "same" index every time because
    # at each deletion the entire list goes 'back a position:
    for i in range(parentheses_indexes[0], parentheses_indexes[1]):
        del equation_list[parentheses_indexes[0]]

    # Returning the updated equation_list:
    return equation_list


# Calculating the sum of a simple expression - an expression without any
# parentheses. This is a recursive function that at each run finds the
# operator with the highest power rank and calculates it's operation,
# then stores it in the expression list and replaces the operator and
# the operand(s) by the value of the operation. Once the expression is
# solved, the expression_list will only have 1 value - the sum of the
# expression, and the function will return it.
def get_value_of_expression(expression_list):
    # Getting the operator with the highest power rank in the expression_list,
    # defining an error flag which will help us determine whether there was
    # an error during the run of this function, storing the index of
    # the operator with the highest power rank and defining a variable to
    # store the sum of the current operation:
    operators_list = get_operators_from_list(expression_list)
    temp_operator = get_strongest_operator_by_power_rank(operators_list)
    temp_operator_index = 0
    sum_of_operation = 0
    # If temp_operator's value is False then there was an error attempting
    # to retrieve it therefore setting the error flag to true:
    if temp_operator is False:
        error_flag = True
        print("Some operators/numbers are missing therefore the equation "
              "can't be calculated")
    else:
        error_flag = False
        temp_operator_index = expression_list.index(temp_operator[0])

    # If the operator's format is 'num op num' then trying to
    # calculate the value of the operation by getting the values
    # from both of the operator's sides and performing the operation:
    if error_flag is False and temp_operator[0][2] == 'num op num':
        # Trying to perform the operation:
        try:
            sum_of_operation = temp_operator[1](
                expression_list[temp_operator_index - 1],
                expression_list[temp_operator_index + 1])
        # Letting the user know that there was an error relating
        # to performing the operation on zero:
        except ZeroDivisionError:
            error_flag = True
            print("Can't perform " + temp_operator[0][0] + " on 0.")
        # Letting the user know that the values received to perform
        # the operation on is too big for the operation to be performed:
        except OverflowError:
            error_flag = True
            print("There value received is too big for " + temp_operator[0][
                0] + " operation.")
        # Letting the user know that there was an error with the operator
        # due to the received numbers to perform the operation on:
        except ValueError:
            error_flag = True
            print("Couldn't perform the " + temp_operator[0][0] +
                  " operation on the received values.")
        # Letting the user know that an error occurred due to
        # the use of the operator and then letting the user know
        # what the error is:
        except Exception as e:
            error_flag = True
            print("There was an error with the " + temp_operator[0][0] +
                  " operator.")
            print('Calculation Error:', e)

        # Trying to update the expression_list:
        try:
            # updating the list to contain the value of the operation we
            # just performed:
            expression_list[temp_operator_index - 1] = sum_of_operation
            # Deleting the operator from the list:
            del expression_list[temp_operator_index]
            # Deleting the 2nd number from the expression list (all the indexes
            # moved by 1 after the previous delete):
            del expression_list[temp_operator_index]
        # Letting the user know that an unexpected error occurred during the
        # attempt to update the list:
        except Exception as e:
            if error_flag is False:
                error_flag = True
                print('Calculation Error:', e)

    # If the operator's format is 'num op' then trying to calculate
    # the value of the operation by getting the value from it's left:
    elif error_flag is False and temp_operator[0][2] == 'num op':
        # Trying to perform the operation:
        try:
            sum_of_operation = temp_operator[1](
                expression_list[temp_operator_index - 1])
        # Letting the user know that he can't perform factorial on negative
        # numbers (if a factorial caused the error) or that there was an error
        # with another operator from the format 'num op':
        except ValueError:
            error_flag = True
            if temp_operator[0][0] == '!':
                print("Can't do factorial for negative/rational numbers.")
            else:
                print("There was an error with the " + temp_operator[0][
                    0] + " sign.")
        # Letting the user know that the value received to perform
        # the operation on is too big for the operation to be performed:
        except OverflowError:
            error_flag = True
            print("There value received is too big for " + temp_operator[0][
                0] + " operation.")
        # Letting the user know that an error occurred due to
        # the use of the operator and then letting the user know
        # what the error is:
        except Exception as e:
            error_flag = True
            print("There was an error with the " + temp_operator[0][
                0] + " sign.")
            print('Calculation Error:', e)

        # Trying to update the expression_list:
        try:
            # updating the list to contain the value of the operation we
            # just performed:
            expression_list[temp_operator_index - 1] = sum_of_operation
            # Deleting the operator from the list:
            del expression_list[temp_operator_index]
        # Letting the user know that an unexpected error occurred during the
        # attempt to update the list:
        except Exception as e:
            if error_flag is False:
                error_flag = True
                print('Calculation Error:', e)

    # If the operator's format is 'op num' then trying to calculate
    # the value of the operation by getting the value from it's right:
    elif error_flag is False and temp_operator[0][2] == 'op num':
        # Trying to perform the operation:
        try:
            sum_of_operation = temp_operator[1](
                expression_list[temp_operator_index + 1])
        # Letting the user know that an error occurred due to
        # the use of the operator and then letting the user know
        # what the error is:
        except Exception as e:
            error_flag = True
            print("There was an error with the " + temp_operator[0][0] +
                  " sign.")
            print('Calculation Error:', e)

        # Trying to update the expression_list:
        try:
            # updating the list to contain the value of the operation we
            # just performed:
            expression_list[temp_operator_index] = sum_of_operation
            # Deleting the number that came after the operator from the list:
            del expression_list[temp_operator_index + 1]
        # Letting the user know that an unexpected error occurred during the
        # attempt to update the list:
        except Exception as e:
            if error_flag is False:
                error_flag = True
                print('Calculation Error:', e)

    # Checking that we didn't get an error performing the operation in the
    # current run of the recursion. If we did get an error then returning a
    # list with 2 False, in order to stop the run of this recursion and the
    # outside recursion that are attempting to solve the equation together.
    # If the length of the expression list when we get here is 1 then the
    # program finished solving the expression, therefore returning it's
    # value. Else, calling this function again after calling another
    # function to "fix" minuses locations on this equation:
    if error_flag is False:
        if len(expression_list) == 1:
            return sum_of_operation
        # Else - calling the function again:
        else:
            # Checking if after the update of the equation, it's length is 1:
            if len(expression_list) == 1:
                return sum_of_operation
            # Else - calling the function again:
            else:
                return get_value_of_expression(expression_list)
    # There was an error during the attempt to calculate the value
    else:
        return [False, False]


# Calculating the sum of an equation by going through the entire equation list
# and each time calling the get_value_of_expression function with an
# expression to calculate from the equation_list, and then replaces that
# part of the list with the value of the expression:
def solve_equation(equation_list):
    if len(equation_list) == 1:
        # Returning the float value of 0 if the value is either -0.0 / 0.0:
        if equation_list[0] == 0:
            return float(0)
        # Returning the value regularly:
        else:
            return equation_list[0]  # Returning the sum of the calculation.

    # temporary value containing the value of the current calculation:
    val = 0
    # Else - getting the next () to calculate and calculating:
    if '(' and ')' in equation_list:
        parentheses_indexes = get_indexes_of_parentheses(equation_list)
        parentheses_list = []  # Creating an empty list for the values
        # inside the parentheses.
        for i in range(0, len(equation_list)):
            # Only taking the values inside the ()
            if parentheses_indexes[0] < i < parentheses_indexes[1]:
                parentheses_list.append(equation_list[i])

        # Removing the values inside the parentheses from the list:
        equation_list = remove_values_in_range_from_list(equation_list,
                                                         parentheses_indexes)

        # If the len of the parentheses is still bigger than 1,
        if len(parentheses_list) > 1:
            equation_list[parentheses_indexes[0]] = get_value_of_expression(
                parentheses_list)
        else:
            equation_list[parentheses_indexes[0]] = parentheses_list[0]

        # Updating val's value to the value of the expression:
        val = equation_list[parentheses_indexes[0]]

    else:
        val = get_value_of_expression(equation_list)

    # Since False is defined as 0 in Python, and we need to use False in
    # order to break the recursion on which we get the value for an
    # expression, we return a list of 2 False in case there was an error
    if not isinstance(val, numbers.Number) and val.count(False) > 1:
        return False
    else:
        return solve_equation(equation_list)
