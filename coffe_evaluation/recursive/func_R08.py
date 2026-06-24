# COFFE Recursive Example 8
# Source: COFFE function-level benchmark

def solution(n):
    if n == 1 or n == 2:
        return 1
    else:
        return solution(solution(n - 1)) + solution(n - solution(n - 1))
