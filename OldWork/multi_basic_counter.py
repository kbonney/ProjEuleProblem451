from sympy.ntheory import factorint, totient
from sympy.ntheory import primefactors, isprime
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
    
def count_solns(max_n, interval = 1, offset = 0, do_percent = 0, target_int = None, graph_name = ""):
    n_vals = []
    times = []
    sol_sum = 0
    percent = 0
    
    #handling base cases
    start_val = 0
    while(start_val*interval + offset < 8):
        if start_val*interval + offset > 2:
            sol_sum += 1
        start_val+=1


    start = time.time()
    #x is our modulus
    #only looking at offset values    
    x = start_val*interval + offset
    while x < max_n + 1:
        if do_percent == 1:
            new_percent = (x*100)/max_n
            if new_percent > percent:
                percent = new_percent
                print("{}%".format(percent))
                n_vals.append(x)
                times.append(time.time()-start)

                
        primes, inverse_is_one = factor_check(x)
        if inverse_is_one:
            sol_sum += 1
            x += interval
            continue

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

        #if x is even we don't have to check even #s
        skip_evens = 1-(x%2)
        
        #do not check n-1 aka y=1 (trivial case)
        solved = False

        #proven bounds on the possible values of the largest self-inverse
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
        if not solved:
            sol_sum += 1
        x += interval

            
    if target_int == None:
        return D
    else:
        target_int.value += sol_sum
        
    if do_percent == 1:
        print("Time taken: {}".format(time.time()-start))
        plt.plot(n_vals, times)
        plt.title(graph_name)
        plt.show()

    

#code for taking command-line arguments
max_n = 5
if len(sys.argv) == 2:
    max_n = int(sys.argv[1])
    sols = count_solns(max_n)
    print("sum: {}".format(sols))

#if we got a number of processes as well as a max n
#then we must multiprocess
elif len(sys.argv) >= 3:
    do_percent = 0
    if len(sys.argv) == 4:
        graph_name = sys.argv[3]
        do_percent = 1
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
    cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': 0, 'do_percent': do_percent, 'target_int': sols, 'graph_name':graph_name})
    cur_process.start()
    jobs.append(cur_process)

    for cur in range(1, processes):
        cur_process = multiprocessing.Process(target=count_solns, args=[max_n], kwargs={'interval': processes, 'offset': cur, 'do_percent': 0, 'target_int': sols})
        cur_process.start()
        jobs.append(cur_process)
        
    for cur_process in jobs:
        cur_process.join()

    print("sum: {}".format(sols.value))

    
#print("Time elapsed: {}".format(end_time-start))
