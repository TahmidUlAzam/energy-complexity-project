# COFFE Recursive Example 6
# Source: COFFE function-level benchmark

def solution(n):
    if n == 0:
        return 2
    if n == 1:
        return 1
    return solution(n - 1) + solution(n - 2)
