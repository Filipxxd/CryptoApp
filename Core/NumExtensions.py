import math
import random


def is_prime(num: int) -> bool:
    if num in [2, 3]:
        return True

    if num % 2 == 0 or num <= 1:
        return False

    r = 0
    d = num - 1

    while d % 2 == 0:
        r += 1
        d //= 2

    x_values = [pow(a, d, num) for a in [random.randint(2, num - 2) for _ in range(5)]]

    if any(x in [1, num - 1] for x in x_values):
        return True

    for _ in range(r - 1):
        x_values = [pow(x, 2, num) for x in x_values]
        if any(x == num - 1 for x in x_values):
            return True

    return False


def get_random_prime(num_length=12) -> int:
    while True:
        current = random.randint(10 ** (num_length - 1), (10 ** num_length) - 1)
        current += 1 if current % 2 == 0 else 0

        if len(str(current)) == num_length and is_prime(current):
            return current


def find_coprime(n: int) -> int:
    for i in range(2, n + 1):
        if math.gcd(n, i) == 1:
            return i

    return n + 1
