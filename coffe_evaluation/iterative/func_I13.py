# COFFE Iterative Example 13
# Source: COFFE function-level benchmark

def solution(S, step):
    return [S[i::step] for i in range(step)]
