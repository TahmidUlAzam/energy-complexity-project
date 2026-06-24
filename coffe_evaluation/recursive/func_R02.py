# COFFE Recursive Example 2
# Source: COFFE function-level benchmark

def solution(n):
    if n < 1:
        return 0
    else:
        return n + solution(n - 2)
