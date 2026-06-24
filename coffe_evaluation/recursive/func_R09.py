# COFFE Recursive Example 9
# Source: COFFE function-level benchmark

def solution(data_list):
    total = 0
    for element in data_list:
        if type(element) == type([]):
            total = total + solution(element)
        else:
            total = total + element
    return total
