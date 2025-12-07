"""
Advent of Code Helper Library
Provides utilities for running solutions with timing and validation
"""

import time
from typing import Callable, Any, Optional

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def format_time(seconds: float) -> str:
    """Format time in appropriate units"""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f}µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.3f}s"


def run_solution(
    solver: Callable[[list[str]], Any],
    input_file: str,
    part: int,
    expected: Optional[Any] = None,
    label: str = ""
) -> Any:
    """
    Run a solution function with timing and optional validation
    
    Args:
        solver: Function that takes lines as input and returns the answer
        input_file: Path to input file
        part: Part number (1 or 2)
        expected: Expected answer for validation (optional)
        label: Label for this run (e.g., "TEST" or "REAL")
    
    Returns:
        The result from the solver function
    """
    # Read input
    with open(input_file) as f:
        lines = f.read().splitlines()
    
    # Time the solution
    start = time.perf_counter()
    result = solver(lines)
    elapsed = time.perf_counter() - start
    
    # Format output
    time_str = format_time(elapsed)
    
    if expected is not None:
        is_correct = result == expected
        color = Colors.GREEN if is_correct else Colors.RED
        status = f"{color}{'✓' if is_correct else '✗'}{Colors.RESET}"
        print(f"Part {part}: {result} {status} (expected: {expected}) [{time_str}]")
    else:
        print(f"Part {part}: {result} [{time_str}]")
    
    return result


def run_day(
    day: int,
    part1_solver: Callable[[list[str]], Any],
    part2_solver: Callable[[list[str]], Any],
    test_part1: Optional[Any] = None,
    test_part2: Optional[Any] = None,
    base_path: str = "."
):
    """
    Run both parts on test and real input with timing and validation
    
    Args:
        day: Day number
        part1_solver: Function for part 1
        part2_solver: Function for part 2
        test_part1: Expected answer for test input part 1
        test_part2: Expected answer for test input part 2
        base_path: Base path for input files (default: current directory)
    """
    day_path = f"{base_path}/day_{day}"
    
    # Test input
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}DAY {day} - TEST INPUT{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.RESET}")
    
    run_solution(part1_solver, f"{day_path}/test_input.txt", 1, test_part1)
    run_solution(part2_solver, f"{day_path}/test_input.txt", 2, test_part2)
    
    # Real input
    print(f"\n{Colors.YELLOW}{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}DAY {day} - REAL INPUT{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{'='*50}{Colors.RESET}")
    
    run_solution(part1_solver, f"{day_path}/input.txt", 1)
    run_solution(part2_solver, f"{day_path}/input.txt", 2)
    print()


# Alternative: Simple runner for single parts
class AOCRunner:
    """Object-oriented interface for running solutions"""
    
    def __init__(self, day: int, base_path: str = "."):
        self.day = day
        self.base_path = base_path
        self.day_path = f"{base_path}/day_{day}"
    
    def test(self, part: int, solver: Callable, expected: Any):
        """Run on test input with expected answer"""
        print(f"{Colors.CYAN}[TEST - Part {part}]{Colors.RESET}")
        return run_solution(solver, f"{self.day_path}/test_input.txt", part, expected)
    
    def solve(self, part: int, solver: Callable):
        """Run on real input"""
        print(f"{Colors.YELLOW}[REAL - Part {part}]{Colors.RESET}")
        return run_solution(solver, f"{self.day_path}/input.txt", part)