# COFFE Recursive Example 10
# Source: COFFE function-level benchmark

def solution(x, y):
    if y < 0:
        return -solution(x, -y)
    elif y == 0:
        return 0
    elif y == 1:
        return x
    else:
        return x + solution(x, y - 1)
