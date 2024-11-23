#! /usr/bin/python
import sys
import time


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def nth_prime(n):
    count = 0
    num = 2
    while True:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 1


no = sys.argv[1]
begin = time.time()
number = nth_prime(int(no))
end = time.time()
print(f'nth_prime({no}): {number}, const: {end - begin}s')
