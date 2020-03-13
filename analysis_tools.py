import sympy as sp
from sympy.ntheory import factorint
from sympy.ntheory import primefactors
from sympy.ntheory import isprime
import sys
import json
import multiprocessing
import time
from math import sqrt
import matplotlib.pyplot as plt

#####
#Contains functions for:
#Generating sample modulo and their involutions
#Looking at the totients/factorizations of n-values and their solutions
#Graphing n-values vs solutions 
#####

#this prints out all self-squares of the moduli up to max_n
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

#code which looks at the totient of the n value and its solutions
#one bound we have discovered but not proven is that the totient of n must be divisible by 4
def totient_comparisons(max_n):
    #x is our modulus
        false_pos = 0
        false_neg = 0
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


                #if we have some interesting solutions, verify the relationship between
                #totient(n)%4 and the existence of solutions (it's necessary, not sufficient)
                if (len(self_squares) > 2) != (sp.totient(x)%4==0):
                        if len(self_squares) > 2:
                                false_neg += 1
                        else:
                                false_pos += 1
                if len(self_squares) > 2:
                        print("Solution totient: {}".format(sp.factorint(sp.totient(max(self_squares)))))
                        #looking at the factorizations of solutions
                        print("N totient: {}".format(sp.factorint(sp.totient(x))))
        print("False positive solns: {} False negative solns: {}".format(false_pos, false_neg))

#code which looks at the factorization of the n value and its solutions
def factorization_comparisons(max_n):
    #x is our modulus
        for x in range(3, max_n):
                self_squares = []
                #factoring to find invertible numbers
                primes = factorint(x)
                
                #checking all the numbers where gcd(x,y)=1
                for y in range(1, x-1):
                        #checks that no prime divisors of our modulus (x) divide our number y
                        #then checks if y is its own inverse
                        if all(y%p != 0 for p in primes.keys()) and (y*y)%x == 1:
                                self_squares.append(y)    


                #if we have some interesting solutions, verify the relationship between
                #totient(n)%4 and the existence of solutions (it's necessary, not sufficient)
                if (len(self_squares) > 2):
                        print("N value: {}".format(x))
                        print("Solution factorization: {}".format(sp.factorint(max(self_squares))))
                        #looking at the factorizations of solutions
                        print("N factorization: {}".format(sp.factorint(x)))
        
#simply counts every n which has a totient divisible by 4 up to some max n
def count_totients_div_4(max_n):
        count = 0
        for x in range(2,max_n):
                if sp.totient(x)%4 == 0:
                        count +=1
        print("Totients divis by 4 up to {}: {}".format(max_n, count))

#calculates and graphs solutions up to some max_n
#also plots the theoretical bounds of .5n and n-sqrt(n)
def approx_bounds(max_n):

        #values we will be plotting 
        n_vals = []
        #these are solution values
        a_vals = []
        
        #x is our modulus
        for x in range(3, max_n):

                #the value of the solution initialized to 1
                self_square = 1
                
                #factoring to find invertible numbers
                primes = factorint(x)

                #we catch one simple edge case here to speed things up
                if len(primes) == 1:
                        n_vals.append(x)
                        a_vals.append(1)
                        continue

                #we only check the theoretical bounds because I have seen that they check out
                for y in range(x-2, int(.5*x)-1, -1):
                        #checks that no prime divisors of our modulus (x) divide our number y
                        #then checks if y is its own inverse
                        if all(y%p != 0 for p in primes.keys()) and (y*y)%x == 1:
                                self_square = y
                                break

                n_vals.append(x)
                a_vals.append(self_square)
        lower_bound = [.5*n for n in n_vals]
        upper_bound = [n-sqrt(n) for n in n_vals]
        plt.scatter(n_vals, a_vals)
        plt.plot(n_vals, lower_bound)
        plt.plot(n_vals, upper_bound)
        plt.show()
        
#totient_comparisons(100)
#count_totients_div_4(100)
approx_bounds(100000)
#factorization_comparisons(100)
