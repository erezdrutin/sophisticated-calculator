# Imports:
import math
import pytest
import calculator_directory.equation_validation as equation_validation
import calculator_directory.calculations as calculations
import calculator_directory.calculator_operators as calculator_operators

""" ******** Defining Parameters For The Tests Outputs ********
-------------------------------------------------------------------------------
When running the tests, we would like to see relevant outputs to what we're
testing. For example, when we're testing whether we're receiving a correct
answer from a calculation of an equation, we would like to see what was the
equation and what was the expected answer: 3+4 = 7. Defining the following
params will allow us to get the output in the desired format.
-------------------------------------------------------------------------------
"""


# Defining how we want the equation validity tests (both the string and
# equation list tests) to look like when we run them:
def validity_param(eq, expected):
    # Printing valid for valid equations and invalid for invalid equations:
    output = 'Valid' if expected else 'Invalid'
    return pytest.param(eq, expected, id=f'{eq}: {output}')


# Defining how we want the equation calculation tests (both the simple
# equations and the complicated equations) to look like when we run them:
def eq_param(eq, expected):
    # Printing them in the format: 4+5 = 9:
    return pytest.param(eq, expected, id=f'{eq} = {expected}')


# Defining how we want the end cases calculations tests to look like when we
# run them:
def end_case_param(eq, expected):
    # Printing the results in the format: ~4 returns False:
    return pytest.param(eq, expected, id=f'{eq} returns {expected}')


# Defining how we want the num_op_num operators tests to look like when we
# run them:
def num_op_num_param(numbers, operator, expected):
    # Printing them in the format 4+5 = 9:
    return pytest.param(numbers, operator, expected,
                        id=f'{numbers[0]}{operator}{numbers[1]} = '
                        f'{expected}')


# Defining how we want the num_op operators tests to look like when we
# run them:
def num_op_param(numbers, operator, expected):
    # Printing them in the format 3! = 6:
    return pytest.param(numbers, operator, expected,
                        id=f'{numbers[0]}{operator} = {expected}')


# Defining how we want the op_num operators tests to look like when we
# run them:
def op_num_param(numbers, operator, expected):
    # Printing them in the format ~3 = -3:
    return pytest.param(numbers, operator, expected,
                        id=f'{operator}{numbers[0]} = {expected}')


""" ******** Calculator Operators Tests ********
-------------------------------------------------------------------------------
Checking each of the calculator operators to determine whether it works
properly or not. These tests will be purely to assert whether we defined the
operators in the calculator_operators module correctly and we receive
results that are matching our expectations.

**** Important Note: ****
Python 3 ints doesn't have a maximum or a minimum, since the int type is
"unbounded", therefore there is no point in attempting to test our
calculator with such values since.
-------------------------------------------------------------------------------
"""


# Testing each of the calculator's operators:
@pytest.mark.parametrize('numbers, operator, expected',
                         [
                             num_op_num_param([4, 1], '+', 5),
                             num_op_num_param([8, 5], '-', 3),
                             num_op_num_param([6, 7], '*', 42),
                             num_op_num_param([35, 5], '/', 7),
                             num_op_num_param([2, 5], '^', 32),
                             op_num_param([40], '~', -40),
                             num_op_num_param([38, 14], '%', 10),
                             num_op_param([0], '!', 1),
                             num_op_num_param([10, 20], '@', 15),
                             num_op_num_param([42, 400], '$', 400),
                             num_op_num_param([57, 40], '&', 40),
                         ])
def test_calculator_operators(numbers, operator, expected):
    # Arrange:
    op = [val for val in calculator_operators.operator_tuple_dict if
          val[0][0] == operator][0]

    # Act:
    if op[2] == 'num op num':
        result = calculator_operators.operator_tuple_dict.get(op)(numbers[0],
                                                                  numbers[1])
    else:
        result = calculator_operators.operator_tuple_dict.get(op)(numbers[0])

    # Assert:
    assert result == expected


""" ******** Equation Validity Tests ********
-------------------------------------------------------------------------------
The code contains 2 different validity checks on which we call different
functions to test different cases in order to verify that the equation we
receive is indeed valid and can be calculated.

The validity checks functions:
1.  A string validity check that checks whether the length of the received
    equation's length is at least 1 char, that the equation starts with a
    start with -(op_num/number) OR ( OR number, that the parentheses in the
    string are balanced (every opening parentheses has a matching closing
    parentheses) and that there isn't a repetition of an operator multiple
    times in a row.

2.  An equation validity check, that comes after the string validity check,
    on which we check whether the received equation is valid and can be
    calculated or not. The function checks whether each operator is in a
    valid position or not. For example, we can't have 40~3 or !(30).
-------------------------------------------------------------------------------
"""


# Sending the parameters to the function that we want to test. In this case,
# we want to test how the test_string_validity function acts in comparison
# to how we expect it to act - "Arrange":
@pytest.mark.parametrize('equation, expected',
                         [validity_param('4-*3', False),
                          validity_param('!+43', False),
                          validity_param('7&@3', False),
                          validity_param('3$%7', False),
                          validity_param('~30&4.5', False),
                          validity_param('', False),
                          validity_param('wertfyguhijk1243ty+*&%d', False),
                          validity_param('     ', False),
                          validity_param('    ', False),
                          validity_param('   \n ', False),
                          validity_param('', False),
                          validity_param('+', False),
                          validity_param('+4', False),
                          validity_param('5+4', True),
                          validity_param('7^4-1', True),
                          validity_param('~-4!', True),
                          validity_param('193%10@8', True),
                          validity_param('0!@2', True),
                          validity_param('14$3&2', True),
                          validity_param('2!%4', True),
                          validity_param('4+2%1', True)
                          ])
# Testing whether the function acts how we expect it to act based on the
# parameters it receives or not:
def test_check_string_validity(equation, expected):
    # Act:
    result = equation_validation.check_string_validity(equation)
    # Assert:
    assert expected == result


# Sending the parameters to the function that we want to test. In this case,
# we want to test how the check_equation_validity function acts in comparison
# to how we expect it to act:
@pytest.mark.parametrize('equation, expected',
                         [validity_param('6&!3', False),
                          validity_param('3(50+2)', False),
                          validity_param('~!17', False),
                          validity_param('(-)2', False),
                          validity_param('(4+)5', False),
                          validity_param('(13%)8', False),
                          validity_param('~~5', False),
                          validity_param('14--(40+5)', False),
                          validity_param('-~-(-5)', False),
                          validity_param('4--5', True),
                          validity_param('~(17%3)+6', True),
                          validity_param('49&20@1', True),
                          validity_param('302$~4', True),
                          validity_param('14%-4', True),
                          validity_param('(0!*4)^3', True)
                          ])
# Testing whether the function acts how we expect it to act based on the
# parameters it receives or not:
def test_check_equation_validity(equation, expected):
    # Arrange:
    equation_list = calculations.string_to_list(equation)
    equation_list = calculations.set_operators_in_list(equation_list)
    # Act:
    result = equation_validation.check_equation_validity(equation_list)
    # Assert:
    assert result == expected


""" ******** Equation Calculation Tests ********
-------------------------------------------------------------------------------
The code contains 2 functions for calculating the sum of an equation:
1.  A function that calculates the sum of an expression without parentheses.
2.  A function that goes through the entire equation and each time sends an
    expression (without parentheses) to the first function and then updates
    the itself with the value of the expression (until the equation only
    contains 1 value which will be the sum of the equation).
-------------------------------------------------------------------------------
"""


# Sending the parameters to the function that we want to test. In this case,
# we want to test how the get_value_of_expression function acts in comparison
# to how we expect it to act:
@pytest.mark.parametrize('equation, expected',
                         [eq_param('~2', -2),
                          eq_param('4!', 24),
                          eq_param('4*5+3', 23),
                          eq_param('400+30', 430),
                          eq_param('-5+5', 0),
                          eq_param('20/4-3', 2),
                          eq_param('30%10', 0),
                          eq_param('-2^2', 4),
                          eq_param('2&40', 2),
                          eq_param('2@10', 6),
                          eq_param('2$30', 30),
                          eq_param('~4@30', 13),
                          eq_param('2*3&4', 6),
                          eq_param('2^3$8', 256),
                          eq_param('350+~30', 320),
                          eq_param('0!*4^2', 16),
                          eq_param('2^3!/5', 12.8),
                          eq_param('30&3!', 6),
                          eq_param('~-4!', 24),
                          eq_param('3!%4$3', 2),
                          eq_param('4^3+32%4-4', 60)
                          ])
# Testing how the function handles expressions without parentheses:
def test_check_simple_equations_calculation(equation, expected):
    # Arrange - Converting the equation string to a list:
    equation_list = calculations.string_to_list(equation)
    equation_list = calculations.set_operators_in_list(equation_list)
    # Act - Storing the result of the calculation.
    result = calculations.get_value_of_expression(equation_list)
    # Assert - Asserting whether result matches our expectations:
    assert result == expected


# Sending the parameters to the function that we want to test. In this case,
# we want to test how the solve_equation function acts in comparison
# to how we expect it to act:
@pytest.mark.parametrize('equation, expected',
                         [eq_param('25-~35^3+(6*((4-9)%31)&63*10^-1)',
                                   42915.6),
                          eq_param('~(-3^2+(72-5!)$100/(7-15))', 3.5),
                          eq_param('4!%10+((30@60$40)^3)*4', 364504),
                          eq_param('((40&13+~(40$20)/4)!)%10', 6),
                          eq_param('(((4$3!)%4^~-3)-4&3+2@8)/6',
                                   1.6666666666666667),
                          eq_param('4958&312%5+6^7/2+(((40@4)$4^2)%10)',
                                   139974),
                          eq_param('931%4*7-((4$3^2)&1)+3!/2', 23),
                          eq_param('4!/8+~((4^-2)*(37$20))@40', 21.84375),
                          eq_param('93%3-~(((30&4)@24)/6+4)',
                                   6.333333333333334),
                          eq_param('~6-((100@500*2^-3)/8)*(2$99)', -470.0625),
                          eq_param('(3-~(4&3)^2+3*7%2)$8@5!+8&2', 66),
                          eq_param('(300$(350&320)*8^(4/2))-65@55', 20420),
                          eq_param('((3^-4)$80*9+(42%30)/15&8)@100', 410.75),
                          eq_param('7-~(38*8+6!/8%3)@(250$300)-((7^2)&32)',
                                   157),
                          eq_param('(((34%7)^~2)*15/3)@(175@(30&25))',
                                   3605 / 72),
                          eq_param('(14^(1/2)*42&3)+(99$38-44$15)%8@4',
                                   math.sqrt(14) * 3 + 1),
                          eq_param('(14&(3!+2%3)+8^2)@100-((14$2/7)*5)', 76),
                          eq_param('(((3!!/100-5^4)@300*10@50)$3)%15', 3),
                          eq_param('(((8*(301%9))$65)^2+96/32*6)@4000',
                                   4121.5),
                          eq_param('~(((((14&-4*8)%3)^2)$(0!+2)!!)@81*~3/6)',
                                   200.25),
                          eq_param('(((((3-~-4)&10)^3$2+5)@3000)%15)!', 2),
                          eq_param('(((~-6!*(1/2))+(17^3)%3)$(200@300&100))*5',
                                   1810),
                          eq_param('~(~(~(-4*5)+8%3)^4)@((1449/18)$40)',
                                   -117087.75),
                          eq_param('((30^(4%3+0!))$((14@86)/10+45&93))@150',
                                   525),
                          eq_param('(((13^97$2%6)*1400@600)/20)+~(6!)',
                                   -70)
                          ])
# Testing how the function handles complicated calculations that contain
# many numbers, parentheses and operators:
def test_complicated_equations_calculation(equation, expected):
    # Arrange - Converting the equation string to a list:
    equation_list = calculations.string_to_list(equation)
    equation_list = calculations.set_operators_in_list(equation_list)
    # Act - Storing the result of the calculation.
    result = calculations.solve_equation(equation_list)
    # Assert - Asserting whether result matches our expectations:
    assert result == expected


# Sending the parameters to the function that we want to test. In this case,
# we want to test how the solve_equation function acts in comparison
# to how we expect it to act:
@pytest.mark.parametrize('equation, expected',
                         [end_case_param('~4!', False),
                          end_case_param('(4+1/2)!', False),
                          end_case_param('4!!!!', False),
                          end_case_param('40/0', False),
                          end_case_param('14%0', False),
                          end_case_param('1400^230', False),
                          end_case_param('-5^(-4/3)', False)
                          ])
# Testing end cases of the solve_equation function on which we expect the
# function to return False because it couldn't solve the equation:
def test_end_cases_results(equation, expected):
    # Arrange - Converting the equation string to a list:
    equation_list = calculations.string_to_list(equation)
    equation_list = calculations.set_operators_in_list(equation_list)
    # Act - Storing the result of the calculation.
    result = calculations.solve_equation(equation_list)
    # Assert - Asserting whether result matches our expectations:
    assert result == expected
