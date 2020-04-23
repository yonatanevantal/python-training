"""Calculator module.

This module allows evaluation of strings which represent mathematical
expressions. The supported operators are declared in operators dictionary.
"""
import re
import math
import operator
from sys import maxsize
from collections import namedtuple

ANY_NUMBER = r"-?\d+(?:\.\d+)?"

# higher precedence means the operator is stronger (will be done first)
Operator = namedtuple("Operator", ["operation", "precedence", "regex"])

OPERATORS = {
    '+': Operator(precedence=1, operation=operator.add,
                  regex=fr"({ANY_NUMBER})\+({ANY_NUMBER})"),
    '-': Operator(precedence=1, operation=operator.sub,
                  regex=fr"({ANY_NUMBER})-({ANY_NUMBER})"),

    '*': Operator(precedence=2, operation=operator.mul,
                  regex=fr"({ANY_NUMBER})\*({ANY_NUMBER})"),
    '/': Operator(precedence=2, operation=operator.truediv,
                  regex=fr"({ANY_NUMBER})/({ANY_NUMBER})"),

    '^': Operator(precedence=3, operation=math.pow,
                  regex=fr"({ANY_NUMBER})\^({ANY_NUMBER})"),
    '%': Operator(precedence=4, operation=math.fmod,
                  regex=fr"({ANY_NUMBER})%({ANY_NUMBER})"),

    '@': Operator(precedence=5, operation=lambda x, y: (x + y) / 2.0,
                  regex=fr"({ANY_NUMBER})@({ANY_NUMBER})"),
    '$': Operator(precedence=5, operation=max,
                  regex=fr"({ANY_NUMBER})\$({ANY_NUMBER})"),
    '&': Operator(precedence=5, operation=min,
                  regex=fr"({ANY_NUMBER})&({ANY_NUMBER})"),

    '~': Operator(precedence=6, operation=operator.neg,
                  regex=fr"~({ANY_NUMBER})"),
    '!': Operator(precedence=7, operation=math.factorial,
                  regex=fr"({ANY_NUMBER})!"),

    '(': Operator(precedence=maxsize, operation=lambda expr: evaluate(expr),
                  regex=r"\(([^()]*)\)")
}


def evaluate(expression: str) -> float:
    """Calculate the value of a mathematical expression.

    Args:
        expression: the entire mathematical expression to calculate.

    Returns:
         The calculated result of the given expression.
    """
    expression = expression.replace(" ", "")
    operators_by_precedence = sorted(OPERATORS.values(),
                                     key=operator.attrgetter("precedence"),
                                     reverse=True)

    for operator_info in operators_by_precedence:
        operator_regex = operator_info.regex

        search_result = re.search(operator_regex, expression)

        if search_result is None:
            continue

        operands = search_result.groups()

        if operator_info.operation is not OPERATORS["("].operation:
            operands = [float(op) for op in operands]

        operation_result = operator_info.operation(*operands)

        old_expression = search_result.group()
        expression = expression.replace(old_expression, str(operation_result))

        return evaluate(expression)

    return float(expression)


def main():
    print("Welcome! Enter expressions to evaluate ('quit' to exit) >>> ")

    for expression in iter(input, "quit"):
        print(evaluate(expression))
        print("Enter expression to evaluate ('quit' to exit) >>> ")


if __name__ == '__main__':
    main()
