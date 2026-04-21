import time
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt


# --- Part A: Algorithm Implementation ---

def bubble_sort(arr):
    # O(n^2)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(arr):
    # O(n^2)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def quick_sort(arr):
    # O(nlogn) worst O(n^2)
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# מיפוי מספרים לאלגוריתמים לפי דרישות המטלה [cite: 71-76]
ALGO_MAP = {
    1: ("Bubble Sort", bubble_sort),
    2: ("Selection Sort", selection_sort),
    5: ("Quick Sort", quick_sort)
}


# --- Utility Functions ---

def generate_array(size, exp_type):
    """מייצר מערך לפי סוג הניסוי (אקראי או כמעט ממוין) [cite: 26, 54]"""
    if exp_type == 0:  # Random Arrays [cite: 23]
        return [random.randint(0, 1000) for _ in range(size)]

    # Nearly Sorted [cite: 54]
    arr = sorted([random.randint(0, 1000) for _ in range(size)])
    noise_percent = 0.05 if exp_type == 1 else 0.20  # 5% or 20% [cite: 68-69]
    num_swaps = int(size * noise_percent)

    for _ in range(num_swaps):
        idx1, idx2 = random.sample(range(size), 2)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


# --- Core Experiment Logic ---

def run_experiment(algo_ids, sizes, exp_type, repetitions):
    results = {algo_id: {"means": [], "stds": []} for algo_id in algo_ids}

    for size in sizes:
        for algo_id in algo_ids:
            times = []
            algo_name, algo_func = ALGO_MAP[algo_id]

            for _ in range(repetitions):
                test_arr = generate_array(size, exp_type)

                start_time = time.time()
                algo_func(test_arr.copy())
                end_time = time.time()

                times.append(end_time - start_time)

            # חישוב ממוצע וסטיית תקן [cite: 32-33]
            results[algo_id]["means"].append(np.mean(times))
            results[algo_id]["stds"].append(np.std(times))

    return results


def plot_results(results, sizes, filename, title):
    plt.figure(figsize=(10, 6))
    for algo_id, data in results.items():
        name = ALGO_MAP[algo_id][0]
        means = np.array(data["means"])
        stds = np.array(data["stds"])

        plt.plot(sizes, means, label=name, marker='o')
        # יצירת האזור המוצל עבור סטיית התקן
        plt.fill_between(sizes, means - stds, means + stds, alpha=0.2)

    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(filename)
    print(f"Saved plot to {filename}")


# --- Part D: CLI Interface ---

def main():
    parser = argparse.ArgumentParser(description="Sorting Algorithms Experiment")
    parser.add_argument("-a", "--algorithms", nargs="+", type=int, required=True,
                        help="IDs of algorithms to compare")  # [cite: 65]
    parser.add_argument("-s", "--sizes", nargs="+", type=int, required=True, help="Array sizes")  # [cite: 66]
    parser.add_argument("-e", "--experiment", type=int, choices=[0, 1, 2], default=0,
                        help="0: Random, 1: 5% noise, 2: 20% noise")  # [cite: 67]
    parser.add_argument("-r", "--repetitions", type=int, default=10,
                        help="Number of repetitions per size")  # [cite: 70]

    args = parser.parse_args()

    # ניסוי 1: מערכים אקראיים (result1.png) [cite: 34]
    print("Running Experiment 1 (Random)...")
    res1 = run_experiment(args.algorithms, args.sizes, 0, args.repetitions)
    plot_results(res1, args.sizes, "result1.png", "Runtime Comparison (Random Arrays)")

    # ניסוי 2: מערכים עם רעש (result2.png) [cite: 58]
    if args.experiment > 0:
        noise_label = "5%" if args.experiment == 1 else "20%"
        print(f"Running Experiment 2 ({noise_label} noise)...")
        res2 = run_experiment(args.algorithms, args.sizes, args.experiment, args.repetitions)
        plot_results(res2, args.sizes, "result2.png", f"Runtime Comparison (Nearly Sorted, noise={noise_label})")


if __name__ == "__main__":
    main()