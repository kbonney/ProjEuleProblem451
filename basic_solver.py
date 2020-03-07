from sympy.ntheory import factorint
import sys
import json
import time

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python generate_samples.py 1000
#to generate up to modulo 1000

def generate_solns(max_n):
    
    #added fillers so solns[n] gives soln mod n
    D = dict()

    #x is our modulus
    for x in range(3, max_n+1):

        #factoring to find invertible numbers
        primes = factorint(x)
        
        #checking all the numbers where gcd(x,y)=1
        #does not check n-1 aka y=1 (trivial case)
        for y in range(2, x):
            #start at the largest value less than x-1 since we're looking for max
            X = x-y
            #checks that no prime divisors of our modulus (x) divide our number y
            #then checks if y is its own inverse
            if all(X%p != 0 for p in primes.keys()) and (X*X)%x == 1:
                D[x]=X
                break

    return D


start = time.time()

#code for taking command-line arguments
max_n = 5
if len(sys.argv) > 1:
    max_n = int(sys.argv[1])

sols = generate_solns(max_n)
print(json.dumps(sols,indent=1))
print("Sum: {}".format(sum(sols.values())))

end = time.time()
print("Time elapsed: {}".format(end-start))
