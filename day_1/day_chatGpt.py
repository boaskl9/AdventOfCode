def count_hits(start, k, direction):
    """
    Count how many t in [1..k] satisfy:
      (start + t) % 100 == 0   for R
      (start - t) % 100 == 0   for L
    """
    if direction == "R":
        # first t such that start + t ≡ 0 (mod 100)
        t0 = (100 - start) % 100
        if t0 == 0:
            t0 = 100
    else:  # direction == "L"
        # first t such that start - t ≡ 0 (mod 100)
        t0 = start % 100
        if t0 == 0:
            t0 = 100

    if t0 > k:
        return 0

    # number of hits = 1 + number of extra full 100-steps
    return 1 + (k - t0) // 100


def solve(rotations):
    pos = 50
    end_zero_count = 0
    pass_zero_count = 0

    for line in rotations:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        k = int(line[1:])
        start = pos

        # count passes *before updating position*
        pass_zero_count += count_hits(start, k, direction)

        # update final position
        if direction == "R":
            pos = (pos + k) % 100
        else:
            pos = (pos - k) % 100

        # Part 1: lands on zero at end
        if pos == 0:
            end_zero_count += 1

    return end_zero_count, pass_zero_count



import time

start = time.perf_counter()

# ---- Run with your input file ----
with open("day_1_input.txt") as f:
    rotations = f.readlines()

p1, p2 = solve(rotations)

print("Day 1 part 1:", p1)
print("Day 1 part 2:", p2)



end = time.perf_counter()

print(f"Execution time: {end - start:.6f} seconds")