from math import factorial
from decimal import Decimal, getcontext

# Uses the summation of the series 1/n! to calculate e

n = int(input("Enter number of decimal places for e: "))
getcontext().prec = n + 100 # Extra precision for calculation

def euler_number(n):
    e = Decimal(0)
    for k in range(n + 100):  # Add some extra terms for accuracy
        e += Decimal(1) / Decimal(factorial(k))
    quantizer = Decimal('1.' + '0' * n) # Quantizer for rounding to the nth decimal place
    return e.quantize(quantizer)

result = euler_number(n)
print(result)