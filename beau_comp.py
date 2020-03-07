from sympy.ntheory import factorint
import sys

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

def generate_samples(max_n):
    for x in range(3, max_n):
        self_squares = []
        primes = factorint(x)
        for y in range(1, x):
            if y not in primes.keys() and (y*y)%x == 1:
                self_squares.append(y)
        print("n: {} self squares: {}".format(x, self_squares))

max_n = 5
if len(sys.argv) > 1:
    max_n = int(sys.argv[1])

generate_samples(max_n)
