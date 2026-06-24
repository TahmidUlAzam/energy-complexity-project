# COFFE Iterative Example 9
# Source: COFFE function-level benchmark

def solution(dict, n):
    result = {key: value for (key, value) in dict.items() if value >= n}
    return result
