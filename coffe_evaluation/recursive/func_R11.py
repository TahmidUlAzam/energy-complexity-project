# COFFE Recursive Example 11
# Source: COFFE function-level benchmark

def solution(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    return solution(n - 1) + solution(n - 2)
