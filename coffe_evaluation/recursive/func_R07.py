# COFFE Recursive Example 7
# Source: COFFE function-level benchmark

def solution(n):
    if n == 0 or n == 1:
        return 1
    return 2 * solution(n - 1) + solution(n - 2)
