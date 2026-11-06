from math import factorial
from decimal import Decimal, getcontext
# Using the Chudnovsky algorithm for figuring out π (pi)
getcontext().prec=1000

pi_input = input("Enter the number of decimal places for π you'd want: ")
n = int(pi_input)

def returnPi(n):
    numerator= Decimal(0)
    pi = Decimal(0)
    denominator= Decimal(0)

    for k in range(n):
        numerator = ((-1)**k)*(factorial(6*k))*(13591409+545140134*k)
        denominator = factorial(3*k)*(factorial(k)**3)*(640320**(3*k))
        pi += Decimal(numerator)/Decimal(denominator)
    pi = pi * Decimal(12) / Decimal(640320 ** Decimal(1.5))
    pi = 1/pi
    return round(pi,n)

print(returnPi(n))