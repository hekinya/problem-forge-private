import sys

tokens = sys.stdin.read().split()
for word in tokens[1:]:
    print('YES' if word in 'Yes' * 18 else 'NO')
