from Calculator import *

def tests():
    calculation_tests()
    error_tests()

def calculation_tests():
    print(eval_expr("1+5-3") == 3)
    print(eval_expr("1-5") == -4)

    print(eval_expr("3*3") == 9)
    print(eval_expr("3/3") == 1)

    print(eval_expr("2^2^3") == 256)
    print(eval_expr("3^2^2") == 81)
    
    print(eval_expr("(3+3)*2") == 12)

def error_tests():
    print(str(eval_expr("3/0")) == DIV_BY_ZERO)
    print(str(eval_expr("(3+3")) == MISSING_OPERATOR)
    print(str(eval_expr("3++")) == MISSING_OPERAND)
    print(str(eval_expr("d+a")) == INVALID_CHAR)
    print(str(eval_expr("")) == "nan")

if __name__ == "__main__":
    tests()