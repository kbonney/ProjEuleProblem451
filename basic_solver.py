from sympy.ntheory import factorint
import sys

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python generate_samples.py 1000
#to generate up to modulo 1000

def generate_solns(max_n):
    
    #added fillers so solns[n] gives soln mod n
    solns = [0, 0, 1]

    #x is our modulus
    for x in range(2, max_n):

        #factoring to find invertible numbers
        primes = factorint(x)
        
        #checking all the numbers where gcd(x,y)=1
        #does not check n-1 aka y=1 (trivial case)
        for y in range(2, x):
            #start at the largest value less than x-1 since we're looking for max
            cur_val = x-y
            #checks that no prime divisors of our modulus (x) divide our number y
            #then checks if y is its own inverse
            if all(cur_val%p != 0 for p in primes.keys()) and (y*y)%x == 1:
                solns.append(cur_val)
                break

    return solns
#code for taking command-line arguments
max_n = 5
if len(sys.argv) > 1:
    max_n = int(sys.argv[1])

solns = generate_solns(max_n)
print(solns)
print("Sum: {}".format(sum(solns)))
