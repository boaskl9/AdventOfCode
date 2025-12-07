#!/usr/bin/env python3
"""
Run all Advent of Code solutions
"""

import subprocess
import sys
from pathlib import Path

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def run_day(day_num):
    """Run a single day's solution"""
    day_path = Path(f"day_{day_num}")
    script_path = day_path / f"day_{day_num}.py"

    if not script_path.exists():
        print(f"{Colors.RED}Day {day_num} not found at {script_path}{Colors.RESET}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Day {day_num} failed with error code {e.returncode}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Day {day_num} failed: {e}{Colors.RESET}")
        return False

def main():
    """Run all implemented days"""
    # Find all implemented days
    days = []
    for i in range(1, 26):  # Advent of Code has 25 days
        day_path = Path(f"day_{i}")
        script_path = day_path / f"day_{i}.py"
        if script_path.exists():
            days.append(i)

    if not days:
        print(f"{Colors.RED}No days found!{Colors.RESET}")
        return 1

    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}RUNNING ALL ADVENT OF CODE SOLUTIONS{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}Found {len(days)} implemented day(s): {', '.join(map(str, days))}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

    successful = 0
    failed = 0

    for day in days:
        if run_day(day):
            successful += 1
        else:
            failed += 1
        print()  # Extra blank line between days

    # Summary
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}SUMMARY{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}Successful: {successful}{Colors.RESET}")
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*60}{Colors.RESET}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
