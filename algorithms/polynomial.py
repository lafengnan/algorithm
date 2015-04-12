# For polynomial-evaluations
# One polynomial is a sum of more than 1 X**n itmes:
# P(X) = A0 + A1X + A2X**2 + ... + AX**n

from sort import timeit

@timeit
def horner(x, factors):
    """
    Horner's rule:
        P(X) = A0 + X(A1 + X(A2 + ... + X(An-1 + XAn)...))
    """
    r = 0
    i = len(factors) - 1

    while i >= 0:
        r = factors[i] + r*x
        i -= 1

    return r

@timeit
def naive(x, factors):
    r = 0
    i = 0

    while i < len(factors):
        r += factors[i] * x**i
        i += 1

    return r
