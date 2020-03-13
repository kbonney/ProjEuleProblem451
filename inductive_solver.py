from sympy import sieve
import sympy as sp
import sys
import json
import multiprocessing
import time
import matplotlib.pyplot as plt
from math import sqrt
from bisect import insort

####
#Overview
####
#The goal here is to leverage previous solutions when finding the next solution
#It uses the theory of finite abelian groups
#Which is basically just fancy chinese remainder theorem

def inductive_solver(max_n):

    #prime sieve for breaking apart solutions
    print("Calculating all necessary primes...")
    primes = [i for i in sieve.primerange(2,int(sqrt(max_n))+1)]
    print("Solving...")

    #dictionary for holding previous solution sets
    solutions = dict([(2, [1]),(3, [1,2])])

    #value for holding our sum solution
    #mod 3 is already included
    sum_sol = 1
    
    #iterating through all possible modulo
    for x in range(4, max_n+1):

        #finding the smallest prime divisor
        smallest_prime = x

        upper_bound = int(sqrt(x))+1
        for cur_prime in primes:
            if cur_prime > upper_bound:
                break
            if x%cur_prime == 0:
                smallest_prime = cur_prime
                break
            
        smallest_prime_power = smallest_prime
        while (x/smallest_prime_power)%smallest_prime == 0:
            smallest_prime_power *= smallest_prime

        #handling edge cases where we have a prime power or a power of 2
        if smallest_prime_power == x:
            if smallest_prime != 2:
                solutions.update([(x,[1,x-1])])
                sum_sol += 1
                continue
            else:
                max_val = 1
                cur_solutions = [1,x-1]
                for cur_val in range(int(sqrt(x)),int((x/2))+1):
                    if (cur_val**2)%x == 1:
                        if (-cur_val)%x > max_val:
                            max_val = (-cur_val)%x
                        cur_solutions.append(cur_val)
                        cur_solutions.append((-cur_val)%x)
                sum_sol += max_val
                solutions.update([(x, cur_solutions)])
                continue
                        
        k = x/smallest_prime_power

        
        #once we've found the smallest prime divisor power, our desired number satisfies a^2 = 1 mod lp^k
        #where lp^k = n
        #thus it satisfies a^2=1 mod p^k
        #and it satifies a^2=1 mod l
        #so our solution must be modularly equivalent to solutions mod p^k and solutions mod l

        #now we're just leveraging chinese remainder theorem
        #using an algorithm to find all solutions for each pair of solutions
        
        cur_sols = []
        #smaller_val = min(smallest_prime_power, k)
        #other_val = max(smallest_prime_power, k)
        max_val = 1
        gcd = sp.gcdex(smallest_prime_power,k)
        for a in solutions[smallest_prime_power]:
            for b in solutions[k]:
                next_sol = ((gcd[0]*smallest_prime_power*(b)) + (gcd[1]*k*(a)))%x
                cur_sols.append(next_sol)
                if next_sol > max_val and next_sol < x-1:
                    max_val = next_sol
        #print(cur_sols)
                        
        sum_sol += max_val
        #saving our solutions
        solutions.update([(x, cur_sols)])
    return solutions, sum_sol

n_sols = 1000
if len(sys.argv) > 1:
    n_sols = int(sys.argv[1])
solutions, sum_sol = inductive_solver(n_sols)
#for solution in solutions.iteritems():
#    print("n: {} self squares: {}".format(solution[0], solution[1]))

print("Sum of involutions: {}".format(sum_sol))
