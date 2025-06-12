import os
import time
import psutil
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict, Any
import importlib.util
import sys

# Import all algorithms
def import_module_from_file(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import all algorithm modules
current_dir = os.path.dirname(os.path.abspath(__file__))
algorithms_dir = current_dir  # Assuming the algorithms are in the same directory
img_subdir = os.path.join(current_dir, "imgs/")
os.mkdir(img_subdir)

# Import all algorithm modules
aho_corasick = import_module_from_file(os.path.join(algorithms_dir, "aho_corasick_algorithm.py"), "aho_corasick_algorithm")
boyer_moore = import_module_from_file(os.path.join(algorithms_dir, "boyer_moore_algorithm.py"), "boyer_moore_algorithm")
kmp = import_module_from_file(os.path.join(algorithms_dir, "kmp_algorithm.py"), "kmp_algorithm")
naive = import_module_from_file(os.path.join(algorithms_dir, "naive_pattern_matching.py"), "naive_pattern_matching")
rabin_karp = import_module_from_file(os.path.join(algorithms_dir, "rabin_karp_algorithm.py"), "rabin_karp_algorithm")
shift_or_mod = import_module_from_file(os.path.join(algorithms_dir, "shift_or_algorithm.py"), "shift_or_algorithm")
# suffix_table = import_module_from_file(os.path.join(algorithms_dir, "suffix_table.py"), "suffix_table")
ukkonen = import_module_from_file(os.path.join(algorithms_dir, "ukkonen.py"), "ukkonen")
z_algorithm = import_module_from_file(os.path.join(algorithms_dir, "z_algorithm.py"), "z_algorithm")

class CharacterComparisonCounter:
    """Helper class to count character comparisons"""
    
    def __init__(self):
        self.comparisons = 0
    
    def compare(self, char1, char2):
        self.comparisons += 1
        return char1 == char2
    
    def reset(self):
        self.comparisons = 0
    
    def get_count(self):
        return self.comparisons

def memory_usage():
    """Get current memory usage in KB"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / 1024  # Convert to KB

def compare_pattern_matching_algorithms(text: str, pattern: str, test_name: str = "Default") -> Dict[str, Dict[str, Any]]:
    """
    Compare the performance of different pattern matching algorithms.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        test_name: Name of the test for reporting
    
    Returns:
        A dictionary containing the results of each algorithm:
        - Execution time in milliseconds
        - Memory usage in kilobytes
        - Number of character comparisons made (where applicable)
        - Positions where the pattern was found
    """
    results = {}
    comparison_counter = CharacterComparisonCounter()
    
    # Store baseline memory
    baseline_memory = memory_usage()
    
    # Naive Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = naive.naive_pattern_match(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Naive"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text) * len(pattern),  # Worst case for naive algorithm
            "positions": positions
        }
    except Exception as e:
        results["Naive"] = {"error": str(e)}
    
    # KMP Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = kmp.kmp_pattern_match(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["KMP"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text) + len(pattern),  # Approximate for KMP
            "positions": positions
        }
    except Exception as e:
        results["KMP"] = {"error": str(e)}
    
    # Boyer-Moore Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = boyer_moore.boyer_moore_pattern_match(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Boyer-Moore"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text) // len(pattern) * len(pattern),  # Approximation
            "positions": positions
        }
    except Exception as e:
        results["Boyer-Moore"] = {"error": str(e)}
    
    # Rabin-Karp Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = rabin_karp.rabin_karp_pattern_match(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Rabin-Karp"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text),  # Best case for Rabin-Karp
            "positions": positions
        }
    except Exception as e:
        results["Rabin-Karp"] = {"error": str(e)}
    
    # Shift-Or Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = shift_or_mod.shift_or(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Shift-Or"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text),  # Shift-Or makes len(text) operations
            "positions": positions
        }
    except Exception as e:
        results["Shift-Or"] = {"error": str(e)}
    
    # Z Algorithm Pattern Matching
    try:
        start_time = time.time()
        start_memory = memory_usage()
        positions = z_algorithm.z_pattern_match(text, pattern)
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Z Algorithm"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory, 
            "comparisons": 2 * len(text),  # Approximation
            "positions": positions
        }
    except Exception as e:
        results["Z Algorithm"] = {"error": str(e)}
    
    # Aho-Corasick Algorithm
    try:
        start_time = time.time()
        start_memory = memory_usage()
        ac = aho_corasick.AhoCorasick([pattern])
        # Build the trie and failure links
        ac_results = ac.search(text)
        positions = [pos for pos, pat in ac_results]
        end_time = time.time()
        end_memory = memory_usage()
        
        results["Aho-Corasick"] = {
            "execution_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": end_memory - baseline_memory,
            "comparisons": len(text),  # Approximate
            "positions": positions
        }
    except Exception as e:
        results["Aho-Corasick"] = {"error": str(e)}
    
    # Suffix Tree (not fully implemented)
    try:
        results["Suffix Tree"] = {
            "execution_time_ms": 0,
            "memory_usage_kb": 0,
            "comparisons": 0,
            "positions": [],
            "comment": "Not implemented yet. Will build the tree and find patterns when implemented."
        }
    except Exception as e:
        results["Suffix Tree"] = {"error": str(e)}
    
    # Add test metadata
    for algo in results:
        if "error" not in results[algo]:
            results[algo]["test_name"] = test_name
    
    return results

def generate_test_cases():
    """Generate various test cases for benchmarking"""
    test_cases = []
    
    # Real data (simulate books/articles)
    # In production, you would load real text files here
    real_data_text = "This is a simulation of real text from books or articles. " * 1000
    real_data_pattern = "real text"
    test_cases.append(("Real Data", real_data_text, real_data_pattern))
    
    # Randomly generated texts
    random_text = ''.join(random.choice('ACGT') for _ in range(10000))
    random_pattern = ''.join(random.choice('ACGT') for _ in range(5))
    test_cases.append(("Random Text", random_text, random_pattern))
    
    # Recurring patterns
    recurring_text = "ABCABCABCABCABCABCABCABCABCABC" * 100
    recurring_pattern = "ABCABC"
    test_cases.append(("Recurring Patterns", recurring_text, recurring_pattern))
    
    # Worst-case scenarios for specific algorithms
    
    # Naive worst case: pattern matches at every position
    naive_worst_text = "A" * 1000
    naive_worst_pattern = "A" * 5
    test_cases.append(("Naive Worst Case", naive_worst_text, naive_worst_pattern))
    
    # KMP/Z-Algorithm worst case: pattern almost matches but fails at the last character
    kmp_worst_text = ("A" * 99 + "B") * 100
    kmp_worst_pattern = "A" * 100
    test_cases.append(("KMP/Z Worst Case", kmp_worst_text, kmp_worst_pattern))
    
    # Boyer-Moore worst case: pattern always shifts by 1
    bm_worst_text = "ABCDEFGABCDEFGABCDEFG" * 100
    bm_worst_pattern = "ABCDEFGA"
    test_cases.append(("Boyer-Moore Worst Case", bm_worst_text, bm_worst_pattern))
    
    # Rabin-Karp worst case: many hash collisions
    rk_worst_text = "".join(random.choice("AB") for _ in range(1000))
    rk_worst_pattern = "AB" * 5
    test_cases.append(("Rabin-Karp Worst Case", rk_worst_text, rk_worst_pattern))
    
    return test_cases

def visualize_results(all_results):
    """Visualize the benchmark results"""
    # Prepare data for visualization
    tests = list(all_results.keys())
    algorithms = list(all_results[tests[0]].keys())
    
    # Create figure for execution time
    plt.figure(figsize=(14, 8))
    bar_width = 0.8 / len(algorithms)
    x = np.arange(len(tests))
    
    for i, algo in enumerate(algorithms):
        times = []
        for test in tests:
            if "execution_time_ms" in all_results[test][algo]:
                times.append(all_results[test][algo]["execution_time_ms"])
            else:
                times.append(0)
        
        plt.bar(x + i * bar_width, times, width=bar_width, label=algo)
    
    plt.xlabel('Test Cases')
    plt.ylabel('Execution Time (ms)')
    plt.title('Execution Time Comparison')
    plt.xticks(x + bar_width * (len(algorithms) / 2 - 0.5), tests, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(img_subdir + 'execution_time_comparison.png')
    
    # Create figure for memory usage
    plt.figure(figsize=(14, 8))
    
    for i, algo in enumerate(algorithms):
        memory = []
        for test in tests:
            if "memory_usage_kb" in all_results[test][algo]:
                memory.append(all_results[test][algo]["memory_usage_kb"])
            else:
                memory.append(0)
        
        plt.bar(x + i * bar_width, memory, width=bar_width, label=algo)
    
    plt.xlabel('Test Cases')
    plt.ylabel('Memory Usage (KB)')
    plt.title('Memory Usage Comparison')
    plt.xticks(x + bar_width * (len(algorithms) / 2 - 0.5), tests, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(img_subdir + 'memory_usage_comparison.png')
    
    # Create figure for character comparisons
    plt.figure(figsize=(14, 8))
    
    for i, algo in enumerate(algorithms):
        comparisons = []
        for test in tests:
            if "comparisons" in all_results[test][algo]:
                comparisons.append(all_results[test][algo]["comparisons"])
            else:
                comparisons.append(0)
        
        plt.bar(x + i * bar_width, comparisons, width=bar_width, label=algo)
    
    plt.xlabel('Test Cases')
    plt.ylabel('Character Comparisons')
    plt.yscale('log')  # Log scale for better visualization
    plt.title('Character Comparisons Comparison')
    plt.xticks(x + bar_width * (len(algorithms) / 2 - 0.5), tests, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(img_subdir + 'char_comparison_comparison.png')

def run_benchmark():
    """Run the full benchmark suite"""
    test_cases = generate_test_cases()
    all_results = {}
    
    for test_name, text, pattern in test_cases:
        print(f"Running test: {test_name}")
        results = compare_pattern_matching_algorithms(text, pattern, test_name)
        all_results[test_name] = results
        
        # Print summary for this test
        print(f"\n--- Results for {test_name} ---")
        print(f"Text length: {len(text)}, Pattern length: {len(pattern)}")
        for algo, data in results.items():
            if "error" in data:
                print(f"{algo}: Error - {data['error']}")
            else:
                print(f"{algo}:")
                print(f"  Execution time: {data['execution_time_ms']:.2f} ms")
                print(f"  Memory usage: {data['memory_usage_kb']:.2f} KB")
                print(f"  Positions found: {len(data['positions'])}")
        print("----------------------------\n")
    
    # Visualize results
    visualize_results(all_results)
    
    return all_results

def compare_suffix_based_algorithms():
    """
    Compare algorithms based on suffix structures.
    This is a placeholder for future implementation.
    """
    print("Suffix-based algorithm comparison is not fully implemented yet.")
    print("When implemented, it will compare:")
    print("- Suffix Tree (Ukkonen's algorithm)")
    print("- Longest Common Substring")
    print("- Longest Palindromic Substring")
    
    # Placeholder for Suffix Tree implementation
    text = "BANANA$"
    pattern = "ANA"
    
    print("\nSuffix Tree Structure Example (when implemented):")
    print("For text:", text)
    print("- Will build tree using Ukkonen's algorithm")
    print("- Will find pattern:", pattern)
    print("- Will identify longest common substring")
    print("- Will identify longest palindromic substring")

if __name__ == "__main__":
    print("Pattern Matching Algorithms Benchmark")
    print("====================================")
    
    # Run the standard pattern matching benchmarks
    results = run_benchmark()
    
    # Compare suffix-based algorithms separately
    print("\nSuffix-based Algorithm Comparison")
    print("================================")
    compare_suffix_based_algorithms()
    
    print("\nBenchmark completed successfully!")
    print("Results visualizations have been saved as PNG files.")
