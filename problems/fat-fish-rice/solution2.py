"""Independent solution: floor((10a + b) / 19) in Python."""
import sys

data = sys.stdin.read().split()
if len(data) >= 2:
    a, b = int(data[0]), int(data[1])
    print((10 * a + b) // 19)
