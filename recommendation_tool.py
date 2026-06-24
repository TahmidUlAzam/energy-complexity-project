# recommendation_tool.py - rule-based recommendation tool for this dissertation.
# Uses Python's ast module to parse a source file and classify every function
# as iterative, recursive, memoised or tail recursive,
# then prints an evidence-backed recommendation based on the experimental findings.
import ast


# Given a function definition node from the AST,
# determine what type of implementation it is.
def analyse_function(func_node, full_code):
    func_name = func_node.name

    # Check 1: Is it already memoised?
    # Look for @lru_cache or @cache decorator
    is_memoized = False
    for decorator in func_node.decorator_list:
        decorator_str = ast.unparse(decorator)
        if "lru_cache" in decorator_str or "cache" in decorator_str:
            is_memoized = True

    # Check 2: Does it call itself? (i.e. is it recursive?)
    is_recursive = False
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == func_name:
                    is_recursive = True

    # Check 3: Is it tail recursive? 
    # A function is tail recursive if the ONLY recursive call is the final return statement
    is_tail_recursive = False
    if is_recursive:
        # Check if the last return statement is just a recursive call
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return):
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == func_name:
                            is_tail_recursive = True

    return {
        "name": func_name,
        "is_recursive": is_recursive,
        "is_memoized": is_memoized,
        "is_tail_recursive": is_tail_recursive
    }

# Given the analysis of a function, output a recommendation
# based on the experimental findings.
def recommend(analysis):

    name = analysis["name"]

    # Not recursive at all
    if not analysis["is_recursive"]:
        return (f"✓  '{name}': No recursion detected. "
                f"Iterative style confirmed — most energy efficient approach.")

    # Already memoised
    if analysis["is_memoized"]:
        return (f"⚠  '{name}': Memoised recursion detected (@lru_cache). "
                f"Efficient for repeated calls with a warm cache, where memoisation avoids "
                f"recomputation. However, if the cache is cleared between calls or the "
                f"function is called only once, memoisation adds overhead without benefit "
                f"— experimental results show memoised factorial used ~96% more energy "
                f"than iterative at n=900 under cache-clearing conditions. "
                f"Recommendation: keep memoisation for warm-cache workloads (repeated "
                f"lookups); rewrite as iteration for cold-cache or single-call workloads.")

    # Tail recursive
    if analysis["is_tail_recursive"]:
        return (f"⚠  '{name}': Tail recursion detected. "
                f"Python does NOT optimise tail calls — this behaves like unoptimised recursion. "
                f"Experimental results show tail recursive factorial used ~67% more energy "
                f"than iterative at n=900. "
                f"Recommendation: rewrite as a loop for sequential algorithms (factorial, "
                f"summation, etc.). For naturally recursive problems, this advice may not "
                f"apply — verify with measurement before refactoring.")

    # Plain recursion (highest theoretical risk, but context-dependent)
    return (f"✗  '{name}': Unoptimised recursion detected. "
            f"For algorithms with repeated subproblems (e.g. naive Fibonacci), this is "
            f"the highest energy risk pattern — experimental results show unoptimised "
            f"recursive Fibonacci used up to 1,750x more energy than iterative at n=35. "
            f"Recommendation: rewrite as iteration or add @lru_cache, UNLESS the function "
            f"implements a naturally recursive algorithm (e.g. divide-and-conquer, tree "
            f"traversal, Towers of Hanoi). For such problems, iteration can actually use "
            f"MORE energy (Hanoi: iterative used ~2.4x more energy than recursive at n=22). "
            f"Rule-based detection cannot determine algorithmic suitability — verify with "
            f"measurement before refactoring.")


# Main function: reads a Python file, analyses every function in it,
# and prints recommendations.
def analyse_file(filepath):

    print(f"\n=== ENERGY RECOMMENDATION TOOL ===")
    print(f"Analysing: {filepath}\n")

    # Read the file
    with open(filepath, "r") as f:
        source_code = f.read()

    # Parse it into an AST
    tree = ast.parse(source_code)

    # Find all function definitions in the file
    functions_found = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions_found += 1
            analysis = analyse_function(node, source_code)
            recommendation = recommend(analysis)
            print(recommendation)
            print()

    if functions_found == 0:
        print("No functions found in this file.")

    print("=== ANALYSIS COMPLETE ===\n")


# This block runs only when recommendation_tool.py is executed directly.
# It demonstrates the tool by analysing the three algorithm files in this
# dissertation and printing a recommendation for every function it finds.
if __name__ == "__main__":
    analyse_file("fibonacci.py")
    analyse_file("factorial.py")
    analyse_file("hanoi.py")