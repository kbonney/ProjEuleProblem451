from sympy.ntheory import factorint
import sys
import json
import multiprocessing
import time

#the goal, for all given integers 3<=n<=2*10^7
#is to calculate the largest positive number m<n-1 st m^(-1) (mod n) == m (mod n)

#run as
#python generate_samples.py 1000
#to generate up to modulo 1000

def generate_solns(max_n, interval = 1, offset = 0, target_dict = None):
    
    #added fillers so solns[n] gives soln mod n
    D = dict()

    #handling cases less than interval (tricky since we are avoiding 0,1,2)
    start_val = 0
    while(start_val*interval + offset < 3):
        start_val+=1

    #x is our modulus
    #only looking at offset values    
    x = start_val*interval + offset
    while x < max_n + 1:
        
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
        x += interval

            
    if target_dict == None:
        return D
    else:
        target_dict.update(D)
    
start = time.time()

#code for taking command-line arguments
max_n = 5
if len(sys.argv) == 2:
    max_n = int(sys.argv[1])
    sols = generate_solns(max_n)
    print(json.dumps(sols,indent=1))
    print("sum: {}".format(sum(sols.values())))

#if we got a number of processes as well as a max n
#then we must multiprocess
elif len(sys.argv) == 3:
    
    max_n = int(sys.argv[1])
    processes = int(sys.argv[2])

    #multiprocessing a solution
    #each of the k processes only looks at values of n where n=cur(mod k), 0<cur<k
    manager = multiprocessing.Manager()
    #the process manager holds a shared variable that is our solns
    sols = manager.dict()
    jobs = []

    #setting up each process with the right values to look at
    for cur in range(0, processes):
        cur_process = multiprocessing.Process(target=generate_solns, args=[max_n], kwargs={'interval': processes, 'offset': cur, 'target_dict': sols})
        cur_process.start()
        jobs.append(cur_process)
        
    for cur_process in jobs:
        cur_process.join()

    sols = dict(sols)
    print(json.dumps(sols,indent=1))
    print("sum: {}".format(sum(sols.values())))

    
end = time.time()
print("Time elapsed: {}".format(end-start))
