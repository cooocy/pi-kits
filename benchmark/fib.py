#! /usr/bin/python
import sys
import time


def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


no = int(sys.argv[1])
begin = time.time()
number = fib(no)
end = time.time()
print(f'fib({no}): {number}, const: {end - begin}s')
