# evaluate_tool.py - evaluation script for the recommendation tool used in this dissertation.
# This script runs the recommendation tool on a sample of 30 Python functions
# taken from the COFFE code efficiency benchmark to evaluate the tool's accuracy.
# The sample consists of 11 recursive and 19 iterative functions.

import os
import ast
from recommendation_tool import analyse_function, recommend

# The 11 recursive functions are stored in the recursive folder
# and the 19 iterative functions are stored in the iterative folder.
# Both folders are inside the coffe_evaluation folder in the project directory.
RECURSIVE_DIR = "coffe_evaluation/recursive"
ITERATIVE_DIR = "coffe_evaluation/iterative"


# This function evaluates the recommendation tool on a single Python file.
# It reads the source code of the file and parses it with the ast module.
# The function definition named solution is then identified as solution is
# the naming convention used by COFFE for reference solutions.
# The recommendation tool's analyse_function and recommend are then called on the identified function.
def evaluate_file(filepath, expected):
    with open(filepath) as f:
        source = f.read()

    tree = ast.parse(source)

    # Find the function named solution which is COFFE's naming convention.
    solution_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'solution':
            solution_func = node
            break

    # Fallback: if no function named solution is found,
    # use the first function definition in the file.
    if solution_func is None:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                solution_func = node
                break

    if solution_func is None:
        return None

    # Call the two functions exported by the recommendation tool.
    # The first classifies the function and the second generates the
    # recommendation message based on the experimental findings.
    analysis = analyse_function(solution_func, source)
    recommendation = recommend(analysis)

    # Convert the analysis result into a single classification label
    # for reporting purposes
    if not analysis["is_recursive"]:
        classification = "Iterative"
    elif analysis["is_memoized"]:
        classification = "Memoised"
    elif analysis["is_tail_recursive"]:
        classification = "Tail Recursive"
    else:
        classification = "Plain Recursive"

    # Check whether the tool's classification matches the expected classification.
    correct = False
    if expected == "Recursive" and classification in ["Plain Recursive", "Tail Recursive", "Memoised"]:
        correct = True
    elif expected == "Iterative" and classification == "Iterative":
        correct = True

    return {
        "file": os.path.basename(filepath),
        "expected": expected,
        "classification": classification,
        "recommendation": recommendation,
        "correct": correct
    }


print("=" * 80)
print("EVALUATION OF RECOMMENDATION TOOL ON COFFE BENCHMARK")
print("=" * 80)

results = []

# Evaluate every Python file in the recursive folder.
# The expected classification for these files is Recursive.
print("\n=== RECURSIVE TEST FILES ===\n")
for filename in sorted(os.listdir(RECURSIVE_DIR)):
    if filename.endswith(".py"):
        result = evaluate_file(os.path.join(RECURSIVE_DIR, filename), "Recursive")
        if result:
            results.append(result)
            mark = "PASS" if result["correct"] else "FAIL"
            print(f"[{mark}] {result['file']}")
            print(f"  Classification: {result['classification']}")
            print(f"  Recommendation: {result['recommendation']}")
            print()

# Evaluate every Python file in the iterative folder.
# The expected classification for these files is Iterative.
print("\n=== ITERATIVE TEST FILES ===\n")
for filename in sorted(os.listdir(ITERATIVE_DIR)):
    if filename.endswith(".py"):
        result = evaluate_file(os.path.join(ITERATIVE_DIR, filename), "Iterative")
        if result:
            results.append(result)
            mark = "PASS" if result["correct"] else "FAIL"
            print(f"[{mark}] {result['file']}")
            print(f"  Classification: {result['classification']}")
            print(f"  Recommendation: {result['recommendation']}")
            print()

# Compute the overall accuracy and the breakdown across the recursive
# and iterative categories
total = len(results)
correct = sum(1 for r in results if r["correct"])
rec_total = sum(1 for r in results if r["expected"] == "Recursive")
rec_correct = sum(1 for r in results if r["expected"] == "Recursive" and r["correct"])
iter_total = sum(1 for r in results if r["expected"] == "Iterative")
iter_correct = sum(1 for r in results if r["expected"] == "Iterative" and r["correct"])

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total functions tested: {total}")
print(f"Correctly classified: {correct}")
print(f"Overall accuracy: {correct/total*100:.1f}%")
print(f"\nRecursive: {rec_correct}/{rec_total} ({rec_correct/rec_total*100:.1f}%)")
print(f"Iterative: {iter_correct}/{iter_total} ({iter_correct/iter_total*100:.1f}%)")