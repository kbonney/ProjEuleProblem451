from sympy.ntheory import factorint
import sys
import json
import multiprocessing
import time
import matplotlib.pyplot as plt
from math import sqrt

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python count_samples.py 1000
#to count up to modulo 1000

def factor_check(n):
    #factoring to find invertible numbers
    primes = factorint(n)
    prime_len = len(primes)
    if prime_len == 1 and 2 not in primes:
        return primes, True
    #if divisible by 2 exactly once
    elif prime_len == 2 and 2 in primes and ((n/2)%2 ==  1):
        return primes, True
    return primes, False
    
def count_solns(max_n, interval = 1, offset = 0, do_percent = 0, target_int = None):

    ###
    #We're setting up a loop here through every value of n up to the desired threshold
    ###
    sol_sum = 0
    percent = 0
    
    #handling base cases, n < 8
    #offset counting for each process
    start_val = 0
    while(start_val*interval + offset < 8):
        if start_val*interval + offset > 2:
            sol_sum += 1
        start_val+=1
        
    #x is our n value
    x = start_val*interval + offset

    ##
    #Beginning the loop through n values
    ##

    
    #looping through all values of n
    while x < max_n + 1:
        
        #tracking the current percentage
        if do_percent == 1:
            new_percent = (x*100)/max_n
            if new_percent > percent:
                percent = new_percent
                print("{}%".format(percent))

        ##
        #Checking edge cases and easy solutions
        ##
        
        #grab the prime factors and handle the cases where we know the involution is 1
        #using theory of prime order groups, prime power groups, prime power *2 groups
        primes, inverse_is_one = factor_check(x)
        if inverse_is_one:
            sol_sum += 1
            x += interval
            continue

        #using the totient to find more cases where the involution is 1 (totient must be divisible by 4)
        totient = 1
        prime_prod = 1
        for prime in primes.keys():
            prime_prod *= prime
        for prime in primes.keys():
            totient *= prime_prod-prime
        if totient%4 != 0:
            sol_sum += 1
            x += interval
            continue

        ###
        #Now we're preparing for the down-and dirty checking for each member of the group
        ###
        
        #if x is even we don't have to check even #s
        skip_evens = 1-(x%2)

        #flag to remember if we found the solution
        solved = False

        #proven bounds on the possible values of the largest self-inverse
        #these bounds are emperically exact
        lower_bound = int(x/2)-1
        upper_bound = x-int(sqrt(x))

        #used to aid in skipping #s
        if skip_evens and upper_bound%2 == 0:
            upper_bound += 1

        #checking if the values in our range are self-square
        #search from largest to smallest
        #terminate as soon as one is found
        for y in range(upper_bound, lower_bound, (-1 -skip_evens)):
            if (y*y)%x == 1:
                sol_sum += y
                solved = True
                break
        #if we didn't find a solution, then the solution is 1
        if not solved:
            sol_sum += 1
        x += interval

    ##
    #Now we're cleaning up and sending the results back
    ##

    if target_int == None:
        return D
    else:
        target_int.value += sol_sum
        
##
#This is the interface where we handle the user commnds
##

max_n = 5

#We expect a two arguments: max_n and #processes 
if len(sys.argv) == 3:
    do_percent = 1
    max_n = int(sys.argv[1])
    processes = int(sys.argv[2])

    ##
    #Beginning the multiprocessing
    ##
    
    manager = multiprocessing.Manager()
    #the process manager holds a shared variable that is our solns
    sols = manager.Value('i', 0)
    jobs = []

    #setting up each process with their own values of n
    #each of the k processes only looks at values of n where n+cur=0(mod k), 0<cur<k

    #first process prints percent and must be initialized separately
    cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': 0, 'do_percent': do_percent, 'target_int': sols})
    cur_process.start()
    jobs.append(cur_process)

    #initialize the rest of the processes in a loop
    for cur in range(1, processes):
        cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': cur, 'do_percent': 0, 'target_int': sols})
        cur_process.start()
        jobs.append(cur_process)

    #wait for our processes to terminate
    for cur_process in jobs:
        cur_process.join()

    #and finally, we have our solution!
    print("sum: {}".format(sols.value))
