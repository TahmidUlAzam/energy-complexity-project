# COFFE Iterative Example 14
# Source: COFFE function-level benchmark

def solution(list, element):
    solution = all((v == element for v in list))
    return solution
