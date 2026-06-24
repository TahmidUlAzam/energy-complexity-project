# COFFE Iterative Example 19
# Source: COFFE function-level benchmark

def solution(dlist, item):
    pos = 0
    found = False
    while pos < len(dlist) and (not found):
        if dlist[pos] == item:
            found = True
        else:
            pos = pos + 1
    return (found, pos)
