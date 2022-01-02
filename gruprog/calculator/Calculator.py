# package calculator

from math import nan
from enum import Enum

# A calculator for rather simple arithmetic expressions.
# Your task is to implement the missing functions so the
# expressions evaluate correctly. Your program should be
# able to correctly handle precedence (including parentheses)
# and associativity - see helper functions.
# The easiest way to evaluate infix expressions is to transform
# them into postfix expressions, using a stack structure.
# For example, the expression 2*(3+4)^5 is first transformed
# to [ 3 -> 4 -> + -> 5 -> ^ -> 2 -> * ] and then evaluated
# left to right. This is known as Reverse Polish Notation,
# see: https://en.wikipedia.org/wiki/Reverse_Polish_notation
#
# NOTE:
# - You do not need to implement negative numbers
#
# To run the program, run either CalculatorREPL or CalculatorGUI

MISSING_OPERAND:  str = "Missing or bad operand"
DIV_BY_ZERO:      str = "Division with 0"
MISSING_OPERATOR: str = "Missing operator or parenthesis"
OP_NOT_FOUND:     str = "Operator not found"
OPERATORS:        str = "+-*/^"
INVALID_CHAR:     str = "Invalid character"


def infix_to_postfix(tokens: list):
    output = []
    operator_stack = []
    for token in tokens:
        if isinstance(token, float):
            output.append(token)

        elif token in OPERATORS:
            output, operator_stack = infix_to_postfix_operator(output, operator_stack, token)

        elif token == "(":
            operator_stack.append(token)

        elif token == ")":
            output, operator_stack = infix_to_postfix_right_parentheses(output, operator_stack)

    output = infix_to_postfix_add_remaining_ops(output, operator_stack)
    return output

def infix_to_postfix_operator(output: list, operator_stack: list, o1: str):
    precedence_o1 = get_precedence(o1)
    for o2 in operator_stack[::-1]:
        precedence_o2 = get_precedence(o2)
        if o2 != "(" and (precedence_o2 > precedence_o1 or (precedence_o2 == precedence_o1 and get_associativity(o1) == Assoc.LEFT)):
            output.append(operator_stack.pop())
        else:
            break
    operator_stack.append(o1)

    return output, operator_stack

def infix_to_postfix_right_parentheses(output: list, operator_stack: list):
    i = len(operator_stack) - 1
    while i > 0 and operator_stack[i] != "(":
        output.append(operator_stack.pop())
        i -= 1
    if i >= 0 and operator_stack[i] == "(":
        operator_stack.pop()
    else:
        raise ValueError(MISSING_OPERATOR)
    return output, operator_stack

def infix_to_postfix_add_remaining_ops(output: list, operator_stack: list):
    while len(operator_stack) > 0:
        op = operator_stack.pop()
        if op == "(":
            raise ValueError(MISSING_OPERATOR)
        else:
            output.append(op)
    return output

# -----  Evaluate RPN expression -------------------
def eval_postfix(postfix_tokens: list):
    stack = []
    for token in postfix_tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            try:
                d1 = stack.pop()
                d2 = stack.pop()
            except IndexError as _:
                raise ValueError(MISSING_OPERAND)
            res = apply_operator(token, d1, d2)
            stack.append(res)
    return stack[0]


# Method used in REPL
def eval_expr(expr: str):
    if len(expr) == 0:
        return nan
    expr = refactor_expr(expr)
    try:
        tokens = tokenize(expr)
        postfix_tokens = infix_to_postfix(tokens)
        res = eval_postfix(postfix_tokens)
        return res
    except ValueError as ve:
        return ve
    except OverflowError as oe:
        return f"OverflowError {oe}"


def apply_operator(op: str, d1: float, d2: float):
    op_switcher = {
        "+": addition,
        "-": subtraction,
        "*": multiplication,
        "/": division,
        "^": exponent
    }
    op_func = op_switcher.get(op, ValueError(OP_NOT_FOUND))

    if callable(op_func):
        return op_func(d1, d2)
    else:
        return op_func

def addition(d1: float, d2: float):
    return d1 + d2

def subtraction(d1: float, d2: float):
    return d2 - d1

def multiplication(d1: float, d2: float):
    return d1 * d2

def division(d1: float, d2: float):
    if d1 == 0:
        raise ValueError(DIV_BY_ZERO)
    return d2 / d1

def exponent(d1: float, d2: float):
    return d2 ** d1


def get_precedence(op: str):
    op_switcher = {
        "+": 2,
        "-": 2,
        "*": 3,
        "/": 3,
        "^": 4
    }
    return op_switcher.get(op, ValueError(OP_NOT_FOUND))


class Assoc(Enum):
    LEFT = 1
    RIGHT = 2


def get_associativity(op: str):
    if op in "+-*/":
        return Assoc.LEFT
    elif op in "^":
        return Assoc.RIGHT
    else:
        return ValueError(OP_NOT_FOUND)


# ---------- Tokenize -----------------------
def tokenize(expr: str):
    tokens = []
    cur_num = ""
    for i, char in enumerate(expr):
        if char.isnumeric() or char == ".":
            cur_num += char
        elif char in OPERATORS:
            tokens, cur_num = tokenize_operator(tokens, cur_num, char, i)
        elif char in "()":
            tokens, cur_num = tokenize_parenthesis(tokens, cur_num, char)
        else:
            raise ValueError(INVALID_CHAR)
    if cur_num:
        tokens.append(float(cur_num))
    return tokens

def tokenize_operator(tokens: list, cur_num: str, char: str, i: int):
    if cur_num:
        tokens.append(float(cur_num))
        cur_num = ""
    tokens.append(char)
    return tokens, cur_num

def tokenize_parenthesis(tokens: list, cur_num: str, char: str):
    if cur_num:
        tokens.append(float(cur_num))
        cur_num = ""
        if char == "(":
            tokens.append("*")
    tokens.append(char)
    return tokens, cur_num

def refactor_expr(expr: str):
    expr = expr.replace(" ", "")
    expr = expr.replace("−", "-")
    expr = expr.replace("×", "*")
    expr = expr.replace("x", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace(",", ".")
    return expr
