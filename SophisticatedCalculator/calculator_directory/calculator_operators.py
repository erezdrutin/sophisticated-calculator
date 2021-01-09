# Imports:
import math

# Working with tuples as dictionary keys and with lambda functions as values:
operator_tuple_dict = {
    # Key - Tuple, Value - Lambda Function:
    # Tuple Contains: Operator sign, Operator power rank, Format of input.
    # Value Contains: a matching lambda function to the operator.
    ('+', 1, 'num op num'): lambda a, b: a + b,
    ('-', 1, 'num op num'): lambda a, b: a - b,
    ('*', 2, 'num op num'): lambda a, b: a * b,
    ('/', 2, 'num op num'): lambda a, b: a / b,
    ('^', 3, 'num op num'): lambda a, b: math.pow(a, b),
    ('~', 6, 'op num'): lambda a: -a,
    ('%', 4, 'num op num'): lambda a, b: a % b,
    ('!', 6, 'num op'): lambda a: math.factorial(a),
    ('@', 5, 'num op num'): lambda a, b: (a + b) / 2,
    ('$', 5, 'num op num'): lambda a, b: max(a, b),
    ('&', 5, 'num op num'): lambda a, b: min(a, b)
}

# Setting information for each of the operators that the calculator knows
# how to handle. When the user will ask for "help" (information regarding
# the operators), this dictionary values will be presented to him:
operator_information_dict = {
    '+': '+ => Format: a + b => Adds b to a.',
    '-': '- => Format: a - b => Subtracts b from a.',
    '*': '* => Format: a * b => Multiplies a by b.',
    '/': '/ => Format: a / b => Divides a by b.',
    '^': '^ => Format: a ^ b => Powers a to the pow of b.',
    '~': '~ => Format: -a => Negates a.',
    '%': '% => Format: a % b => Leftovers from the divide of a by b.',
    '!': '! => Format: a! => Multiplies a by all of the values before a:'
         ' (1*2*...*a).',
    '@': '@ => Format: (a+b)/2 => Averages a and b.',
    '$': '$ => Format: max(a, b) => Max value between a and b.',
    '&': '& => Format: min(a, b) => Min value between a and b.'
}
