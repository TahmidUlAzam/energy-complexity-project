# analyze.py - data analysis script for this dissertation.
# Reads the CodeCarbon emissions CSV produced by run_all_experiments.py,
# computes summary statistics per configuration and plots the energy
# consumption figures shown in Chapter 5.
import pandas as pd
import matplotlib.pyplot as plt


# Step 1: Load the data
# emissions_final.csv has no header row (CodeCarbon overwrote emissions.csv at some point).
# We grab the header from the backup file, which has the same column order, then apply it.
header_row = pd.read_csv("emissions_FINAL_30trials_backup.csv", nrows=0).columns.tolist()
df = pd.read_csv("emissions_final.csv", header=None, names=header_row)
print(f"Loaded {len(df)} rows from emissions_final.csv")


#  Step 2: Parse project_name into algorithm, variant, n, trial
# Format: "{Algorithm}_{Variant}_n{Size}_trial{TrialNumber}"
# Single-word variants (Iterative, Memoized, Recursive) → 4 parts when split on "_"
# Two-word variants (Tail_Recursive, Unoptimized_Recursive) → 5 parts
split_cols = df["project_name"].str.split("_", expand=True)
two_word = split_cols[4].notna()

df["algorithm"] = split_cols[0]
df["variant"] = split_cols[1].where(~two_word, split_cols[1] + "_" + split_cols[2])
n_col = split_cols[2].where(~two_word, split_cols[3])
trial_col = split_cols[3].where(~two_word, split_cols[4])
df["n"] = n_col.str.replace("n", "").astype(int)
df["trial"] = trial_col.str.replace("trial", "").astype(int)

print(f"Algorithms found: {sorted(df['algorithm'].unique())}")
print(f"Variants found: {sorted(df['variant'].unique())}")



#  Step 3: Compute summary statistics (mean + std per configuration)
summary = df.groupby(["algorithm", "variant", "n"]).agg(
    mean_energy=("energy_consumed", "mean"),
    std_energy=("energy_consumed", "std"),
    mean_duration=("duration", "mean"),
    std_duration=("duration", "std"),
    trials=("energy_consumed", "count")
).reset_index()

print(f"\nSummary table: {len(summary)} configurations")
summary.to_csv("summary_statistics.csv", index=False)
print("✓ Saved summary_statistics.csv")


# Step 4: Plot mean energy consumption with error bars across input sizes
# for all variants of one algorithm.
# Used to generate Figures 5.1, 5.2, 5.3 in the dissertation.
def plot_algorithm(algorithm_name, log_scale=True, save_path=None):
    variant_labels = {
        "Iterative": "Iterative",
        "Memoized": "Memoised Recursive",
        "Tail_Recursive": "Tail Recursive",
        "Unoptimized_Recursive": "Unoptimised Recursive",
        "Recursive": "Recursive"
    }
    algo_labels = {
        "Fib": "Fibonacci Algorithm",
        "Factorial": "Factorial Algorithm",
        "Hanoi": "Towers of Hanoi Algorithm"
    }

    fig, ax = plt.subplots(figsize=(9, 6))
    algo_data = summary[summary["algorithm"] == algorithm_name]

    for variant in algo_data["variant"].unique():
        variant_data = algo_data[algo_data["variant"] == variant].sort_values("n")
        label = variant_labels.get(variant, variant)
        ax.errorbar(
            variant_data["n"],
            variant_data["mean_energy"],
            yerr=variant_data["std_energy"],
            label=label,
            marker="o",
            capsize=4
        )

    actual_sizes = sorted(algo_data["n"].unique())
    ax.set_xticks(actual_sizes)
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Mean Energy Consumed (kWh)", fontsize=12)
    ax.set_title(f"Energy Consumption: {algo_labels.get(algorithm_name, algorithm_name)}", fontsize=13)

    if log_scale:
        ax.set_yscale("log")

    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"✓ Plot saved to {save_path}")

    plt.show()


#  Step 5: Generate the three dissertation plots 
plot_algorithm("Fib", save_path="plot_fibonacci.png")
plot_algorithm("Factorial", save_path="plot_factorial.png")
plot_algorithm("Hanoi", save_path="plot_hanoi.png")