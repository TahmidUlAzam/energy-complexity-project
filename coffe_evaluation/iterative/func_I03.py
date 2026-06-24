# COFFE Iterative Example 3
# Source: COFFE function-level benchmark

import re

def solution(text):
    patterns = 'ab{2,3}'
    if re.search(patterns, text):
        return True
    else:
        return False
