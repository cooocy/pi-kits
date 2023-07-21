#! /usr/bin/python
import sys
import time

def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)

n = int(sys.argv[1])
begin = time.time()
fib_n = fib(n)
end = time.time()
print('fib(%s): %s, time(s): %s' % (n, fib_n, end - begin))
