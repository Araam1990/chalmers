from functools import cache

@cache
def fib(n):
    return n if n <= 1 else fib(n - 2) + fib(n - 1)

print(fib(68))