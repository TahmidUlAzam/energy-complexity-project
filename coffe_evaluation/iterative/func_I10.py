# COFFE Iterative Example 10
# Source: COFFE function-level benchmark

def solution(list, element):
    list = [v for elt in list for v in (element, elt)]
    return list
