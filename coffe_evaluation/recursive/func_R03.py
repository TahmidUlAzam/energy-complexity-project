# COFFE Recursive Example 3
# Source: COFFE function-level benchmark

def solution(a, b):
    if b == 0:
        return 1
    elif a == 0:
        return 0
    elif b == 1:
        return a
    else:
        return a * solution(a, b - 1)
