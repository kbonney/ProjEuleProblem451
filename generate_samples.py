from sympy.ntheory import factorint
import sys
import json

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python generate_samples.py 1000
#to generate up to modulo 1000

def generate_samples(max_n):
    #x is our modulus
    for x in range(3, max_n):
        self_squares = []
        #factoring to find invertible numbers
        primes = factorint(x)

        #checking all the numbers where gcd(x,y)=1
        for y in range(1, x):
            #checks that no prime divisors of our modulus (x) divide our number y
            #then checks if y is its own inverse
            if all(y%p != 0 for p in primes.keys()) and (y*y)%x == 1:
                self_squares.append(y)
        print("n: {} self squares: {}".format(x, self_squares))

#code for taking command-line arguments
max_n = 5
if len(sys.argv) > 1:
    max_n = int(sys.argv[1])


print(json.dumps(generate_samples(max_n)
,indent=1))
