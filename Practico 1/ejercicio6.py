from sympy.ntheory.factor_ import primefactors
from sympy import mod_inverse

n = 1255
e = 3

p, q = primefactors(n)
d = mod_inverse(e, (p - 1) * (q - 1))

print("The private key is", d)