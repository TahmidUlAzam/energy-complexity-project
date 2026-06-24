# run_all_experiments.py - main experiment runner for this dissertation.
# Imports all algorithm variants from factorial.py, fibonacci.py and hanoi.py
# measures energy consumption with CodeCarbon over 30 trials per configuration
from codecarbon import EmissionsTracker
import time

from fibonacci import fib_iterative, fib_memoized, fib_tail_recursive, fib_recursive
from factorial import factorial_iterative, factorial_memoized, factorial_tail_recursive, factorial_recursive
from hanoi import hanoi_recursive, hanoi_iterative


# 30 trials per configuration to average out random noise in the
# software-based energy measurements.
TRIALS = 30


# Runs 30 trials of a single algorithm-variant-input-size configuration.
# Each trial creates its own CodeCarbon tracker with a unique project label
# so the trials can be identified later in the CSV.
# The 'repetitions' argument controls how many times the function is called
#  inside each trial (used to amplify short workloads like Factorial).
# The 'call_func' argument is a wrapper that handles the different argument signatures of
# Fibonacci/Factorial (single n) versus Towers of Hanoi (four arguments).
def run_single_test(algorithm_name, variant_name, func, n, call_func, repetitions=1):
    for trial in range(TRIALS):
        project_label = f"{algorithm_name}_{variant_name}_n{n}_trial{trial}"
        print(f"  Trial {trial + 1}/{TRIALS}: {project_label}")

        tracker = EmissionsTracker(
            project_name=project_label,
            measure_power_secs=1,
            save_to_file=True,
            log_level="error"
        )

        tracker.start()
        for _ in range(repetitions):
            if hasattr(func, "cache_clear"):
                func.cache_clear()
            call_func(func, n)
        tracker.stop()

# Wrapper for Fibonacci and Factorial variants that take a single argument n.
def call_simple(func, n):
    func(n)

# Wrapper for Towers of Hanoi variants that take four arguments.
def call_hanoi(func, n):
    func(n, "A", "C", "B")


# For Fibonacci, n = 10, 15, 20, 25, 30, 35 were chosen to observe the
# exponential growth of the unoptimised recursive variant.
# For Fibonacci, a single call took measurable time already,
# so only a single repetition per trial was required.
print("=== FIBONACCI ===")
fib_variants = [
    ("Iterative", fib_iterative),
    ("Memoized", fib_memoized),
    ("Tail_Recursive", fib_tail_recursive),
    ("Unoptimized_Recursive", fib_recursive),
]
fib_sizes = [10, 15, 20, 25, 30, 35]
for variant_name, func in fib_variants:
    for n in fib_sizes:
        print(f"Fibonacci / {variant_name} / n={n}")
        run_single_test("Fib", variant_name, func, n, call_simple, repetitions=1)


# For Factorial, large inputs like n = 100, 250, 500, 750 and 900 were
# chosen to produce energy consumption that was measurable.
# For Factorial, a single call took microseconds even when input n = 900 and this was not
# reliable for CodeCarbon to measure as it was too short.
# 5,000 repetitions per trial were used to resolve this.
print("\n=== FACTORIAL ===")
fact_variants = [
    ("Iterative", factorial_iterative),
    ("Memoized", factorial_memoized),
    ("Tail_Recursive", factorial_tail_recursive),
    ("Unoptimized_Recursive", factorial_recursive),
]
fact_sizes = [100, 250, 500, 750, 900]
for variant_name, func in fact_variants:
    for n in fact_sizes:
        print(f"Factorial / {variant_name} / n={n}")
        run_single_test("Factorial", variant_name, func, n, call_simple, repetitions=5000)


# For Hanoi, n = 15, 18, 20 and 22 were chosen as the O(2^n) time complexity
# of Towers of Hanoi makes even moderate n values take several seconds per call.
# For Hanoi, a single call took measurable time already,
# so only a single repetition per trial was required.
print("\n=== HANOI ===")
hanoi_variants = [
    ("Recursive", hanoi_recursive),
    ("Iterative", hanoi_iterative),
]
hanoi_sizes = [15, 18, 20, 22]
for variant_name, func in hanoi_variants:
    for n in hanoi_sizes:
        print(f"Hanoi / {variant_name} / n={n}")
        run_single_test("Hanoi", variant_name, func, n, call_hanoi, repetitions=1)

print("\n=== ALL EXPERIMENTS COMPLETE ===")