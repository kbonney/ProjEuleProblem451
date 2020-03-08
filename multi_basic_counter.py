from sympy.ntheory import factorint
from sympy.ntheory import primefactors, isprime
import sys
import json
import multiprocessing
import time
from math import sqrt

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python count_samples.py 1000
#to count up to modulo 1000

def count_solns(max_n, interval = 1, offset = 0, do_percent = 0, target_int = None):
    
    sol_sum = 0
    percent = 0
    
    #handling cases less than interval (tricky since we are avoiding 0,1,2)
    start_val = 0
    while(start_val*interval + offset < 3):
        start_val+=1

    #x is our modulus
    #only looking at offset values    
    x = start_val*interval + offset
    while x < max_n + 1:
        if do_percent == 1:
            new_percent = (x*100)/max_n
            if new_percent > percent:
                percent = new_percent
                print("{}%".format(percent))
        '''
        #factoring to find invertible numbers
        primes = primefactors(x)
        prime_len = len(primes)
        if prime_len == 1 and 2 not in primes:
            sol_sum += 1
            x += interval
            continue
        #if divisible by 2 exactly once
        elif prime_len == 2 and 2 in primes and ((x/2)%2 ==  1):
            sol_sum += 1
            x += interval
            continue
        '''
        '''
        if isprime(x):
            sol_sum += 1
            x += interval
            continue
        '''
        #checking all the numbers where gcd(x,y)=1
        #does not check n-1 aka y=1 (trivial case)
        solved = False
        lower_bound = int(x/2)-1
        upper_bound = x-int(sqrt(x))
        for y in range(upper_bound, lower_bound, -1):
            #start at the largest value less than x-1 since we're looking for max
            #checks that no prime divisors of our modulus (x) divide our number y
            #then checks if y is its own inverse
            #all(X%p != 0 for p in primes) and
            if (y*y)%x == 1:
                sol_sum += y
                solved = True
                break
        if not solved:
            sol_sum += 1
        x += interval

            
    if target_int == None:
        return D
    else:
        target_int.value += sol_sum
    
start = time.time()

#code for taking command-line arguments
max_n = 5
if len(sys.argv) == 2:
    max_n = int(sys.argv[1])
    sols = count_solns(max_n)
    print("sum: {}".format(sols))

#if we got a number of processes as well as a max n
#then we must multiprocess
elif len(sys.argv) == 3:
    
    max_n = int(sys.argv[1])
    processes = int(sys.argv[2])

    #multiprocessing a solution
    #each of the k processes only looks at values of n where n=cur(mod k), 0<cur<k
    manager = multiprocessing.Manager()
    #the process manager holds a shared variable that is our solns
    sols = manager.Value('i', 0)
    jobs = []

    #setting up each process with the right values of n
    #first process prints percent
    cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': 0, 'do_percent': 1, 'target_int': sols})
    cur_process.start()
    jobs.append(cur_process)

    for cur in range(1, processes):
        cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': cur, 'do_percent': 0, 'target_int': sols})
        cur_process.start()
        jobs.append(cur_process)
        
    for cur_process in jobs:
        cur_process.join()

    print("sum: {}".format(sols.value))

    
end = time.time()
print("Time elapsed: {}".format(end-start))
