# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:21:55 2017

11-aug


@author: Kun
"""


import api
import numpy as np
import random
import time
import copy
import primal
import dual


from update_spanning_tree3 import update_spanning_tree3

#size of the problem
n = 12

#size of the bucket
vio_set_lim = n**2

#makes the set of Vertices
V = api.makeVset(n)

#assigning pointers for R and N
R= V[0]
N = V[1]

#creating distiance dicitonary
dist_dic = {}
#dis = 1
#randomly generating distances between 10 and 100 for each entry in the distance matrix
for v in V[1]:
    dist_dic[v] = random.randint(10, 100)#dis#dist_dic[v] + dis/100.00
#    dis+=1
    
#adding noise to the distance matrix
#dis = 1

#for v in V[1]:
#    dist_dic[v] = dist_dic[v] + dis/100.00
#    dis+=1    

#the set of non basic edges with flow = 1
exceptset = set()


#make E_B creates basis and returns 3 things
E_T, E_X, P = api.makeE_B(n,N)
E_T = list(E_T)
E_X = list(E_X)
E_B = [E_T, E_X]
#the code below is wrong
#manually makes the initial M_Rinverse
MR_inv = api.test_MR_inv(E_B,V)
#
#keep intial E_B for testing purposhes
#initial_E_B = copy.deepcopy(E_B)
#the following lists are used for logging
#historyE_B = []
#historyV = []
logg = []
#his_fbar_T = []
#his_fbar_X = []
#costlog = []
#initialising
e_prime = None
notopt = True
set0 = set()
set1 = set()
set2 = set()
pivotset = set()
#number of simplex iterations
num_iter = 0
#time keeping
start = time.time()

#starting simplex phase 2
while notopt:
    
    num_iter +=1
    #create cost dictionary
    c_T = dict.fromkeys(E_T, 0)

    for e in E_T:
        if e[1] is None:
            c_T[e] = dist_dic[e[0]]
        else:
            c_T[e] = 0
    
    c_X = dict.fromkeys(E_X, 0)
    for e in E_X:
        if e[1] is None:
            c_X[e] = dist_dic[e[0]]
        else:
            c_X[e] = 0
    
    
    c_bar = [c_T,c_X]

    #running dual to find potentail 
    pi_R, pi_N, c_X = dual.dual(V, E_B, MR_inv, c_bar)
    pi_R.update(pi_N)
    pi_dl = pi_R
    for v in pi_dl:
        if np.isclose(0, pi_dl[v]):
            pi_dl[v] = 0
        else:
            pi_dl[v] = np.round(pi_dl[v], 10)
    violate = {}
    setcounter = 0
#==============================================================================
#     LAST THING TO IMPLEMENT IS THE BUCKETING THE VIOLATE EDGES
#==============================================================================
    #looping through the non basic hyperarcs    
    #xijks
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if setcounter==vio_set_lim:
                        break
                    else:                    
                        if i<j and j<k:
        #                        E.add(((i,j),k))
                            e = ((i,j),k)                        
                            if e not in E_B[0] and e not in E_B[1]:
                                c_e = 0
                                temp = pi_dl[(e[0][0],e[1])] + pi_dl[(e[0][1],e[1])] + pi_dl[e[1]]      
                                reduced_cost_e = c_e  + temp - pi_dl[e[0]]
                                if np.isclose(0, reduced_cost_e):
                                    reduced_cost_e = 0
                                else:
                                    reduced_cost_e = np.round(reduced_cost_e, 10)
                
                                if e in exceptset and reduced_cost_e > 0:
                                    violate[e] = reduced_cost_e
                                    setcounter+=1
                                elif e not in exceptset and reduced_cost_e < 0:
                                    violate[e] = reduced_cost_e
                                    setcounter+=1
                            else:
                                continue
    #uij
    for j in range(2,n+1):
        for i in range(1, n):
            if i<j:
                if setcounter==vio_set_lim:
                    break
                else:     
                    e = ((i, j), None)
                    if e not in E_B[0] and e not in E_B[1]:
                        c_e = dist_dic[e[0]]
                        reduced_cost_e = c_e - pi_dl[e[0]]
                        if np.isclose(0, reduced_cost_e):
                            reduced_cost_e = 0
                        else:
                            reduced_cost_e = np.round(reduced_cost_e, 10)
                        if e in exceptset and reduced_cost_e > 0:
                            violate[e] = reduced_cost_e
                            setcounter+=1
                        elif e not in exceptset and reduced_cost_e < 0:
                            violate[e] = reduced_cost_e
                            setcounter+=1
                    else:
                        continue
      
 


   
    len_violate = len(violate)
#    print len_violate
#==============================================================================
#     gotta fix this shit, not all v in R should be -1 only 4,5,6..etc
#==============================================================================
    #create demand vector
    b_R = dict.fromkeys(V[0], 0)
    b_N = dict.fromkeys(V[1], 0)
    starting_b = [(1,2),(1,3),(2,3)]
    starting_r = range(4,n+1)
    for v in starting_b:
        if v in N:      
            b_N[v] = 1
        if v in R:
            b_R[v]= 1

    for v in starting_r:
        if v in N:      
            b_N[v] = -1
        if v in R:
            b_R[v]= -1
    
    b_bar = [b_R, b_N]
    #create primal
    f_T, f_X = primal.Primal(V, E_B, MR_inv, b_bar)
    for e in f_T:
        if np.isclose(0, f_T[e]):
            f_T[e] = 0
        else:
            f_T[e] = np.round(f_T[e], 10)
    for e in f_X:
        if np.isclose(0, f_X[e]):
            f_X[e] = 0
        else:
            f_X[e] = np.round(f_X[e], 10)
            
#    tempcost = api.calcCost(f_T,dist_dic)
#    costlog.append(tempcost)

    #terminate as optimality condition met
    if len_violate ==0:        
        print "Terminate algorithm", "n is ", n
        calccost = api.calcCost(f_T,dist_dic)        
        print "cost is  ", calccost
        notopt = False
        end = time.time()
        print "time taken ", end-start
        print "num iterations", num_iter
        break
#        return len_violate, E_B, E_B_pre, e_star, e_prime
    
    else:
        #find entering e
        minRC = float('inf')    
        for e in violate:
            if violate[e] < minRC:
                minRC = violate[e]
                e_prime = e

           
    
        if e_prime[1] is None:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            if e_prime[0] in R:      
                temp_R[e_prime[0]] = -1         
            else:
                temp_N[e_prime[0]] = -1  
            temp_bar = [temp_R, temp_N]
        
        elif e_prime[1] is not None:
            if e_prime[0] is not None:
                ij = e_prime[0]
                k = e_prime[1]
                ik = (e_prime[0][0],e_prime[1])
                jk = (e_prime[0][1],e_prime[1])     
                temp_R = dict.fromkeys(V[0], 0)      
                temp_N = dict.fromkeys(V[1], 0)
                vset = [ij, ik, jk, k]            
                for v in vset:
                    if v in V[0]:
                        if v ==ij:
                            temp_R[v] = -1
                        else:
                            temp_R[v] = 1
                    if v in V[1]:
                        if v == ij:
                            temp_N[v] = -1
                        else:
                            temp_N[v] = 1
                
                temp_bar = [temp_R, temp_N]
        #running primal again but with demand vector induced by eprime
        fbar_T, fbar_X = primal.Primal(V, E_B, MR_inv, temp_bar)  
        for e in fbar_T:
            if np.isclose(0,fbar_T[e]):
                fbar_T[e] = 0
            else:
                fbar_T[e] = np.round(fbar_T[e], 10)
        for e in fbar_X:
            if np.isclose(0,fbar_X[e]):
                fbar_X[e] = 0
            else:
                fbar_X[e] = np.round(fbar_X[e], 10)
        
        fbar_lp = api.lp_find_flow(E_B, V, e_prime, n)
        fbar_pri = copy.deepcopy(fbar_T)
        fbar_pri.update(fbar_X)
        #creates the s set
        s = {}
        
        if e_prime not in exceptset:                
            for e in E_B[0]:
                if fbar_T[e] > 0:
                    s[e] = ((1-f_T[e])/fbar_T[e])
                elif fbar_T[e] < 0:
                    s[e] = f_T[e]/(-fbar_T[e])
                else:
                    s[e] = 0
            for e in E_B[1]:
                if fbar_X[e] > 0:
                    s[e] = ((1-f_X[e])/fbar_X[e])
                elif fbar_X[e] < 0:
                    s[e] = f_X[e]/(-fbar_X[e])
                else:
                    s[e] = 0
            
            s[e_prime] = 1
        else:
            #if f(e_prime) =1
            for e in E_B[0]:
                if fbar_T[e] > 0:
                    s[e] = ((-f_T[e])/fbar_T[e])
                elif fbar_T[e] < 0:
                    s[e] = f_T[e]/(-fbar_T[e])
                else:
                    s[e] = 0
            for e in E_B[1]:
                if fbar_X[e] > 0:
                    s[e] = ((1-f_X[e])/fbar_X[e])
                elif fbar_X[e] < 0:
                    s[e] = f_X[e]/(-fbar_X[e])
                else:
                    s[e] = 0
            
            s[e_prime] = 0
            

            
            
        argmin = {}
        for e in s:
            if e in E_B[0] and fbar_T[e] !=0:
                argmin[e] = s[e]
            elif e in E_B[1] and fbar_X[e] !=0:
                argmin[e] = s[e]
                

        e_star = None
        #selects leaving edge e
        if len(argmin) == 0:
            e_star = e_prime
        
        else:
            if e_star is None:
            
                argminvalue = min(argmin.values())
                if argminvalue >1:
                    e_star = e_prime
                else:
                    keys_to_remove = [key for key, value in argmin.iteritems()
                              if value > argminvalue]
                    for key in keys_to_remove:
                        del argmin[key]
                    
                    e_star = random.choice(argmin.keys())

        set0 = set1
        set1 = set2
        set2 = pivotset
        pivotset = set((e_prime, e_star))
        #checks for cycling
        if set0 == set1 and set1 == set2 and set2 == pivotset:
            print "cycling - terminate"
            calccost = api.calcCost(f_T,dist_dic)        
            print "cost is  ", calccost
            notopt = False
            end = time.time()
            print "time taken ", end-start
            print "num iterations", num_iter
            break
        
#==============================================================================
#         HERE SHOULD BE WHERE THE CHNAGE BASIS HAPPENS
#       NEED TO TRY KEEP THE BASIS AS A SPANNING TREE OTHERWISE
#       THE FLOW AND PRIMAL ALGORITHM WILL NOT WORK        
#==============================================================================

        if e_prime == e_star:
        #basis not changed
            if e_prime in exceptset:
                exceptset.remove(e_prime)
            elif e_prime not in exceptset:
                exceptset.add(e_prime)
                
#            gotta change f_T
            f_prime = {}
            for e in E_B[0]:
                if e == e_prime:
                    f_prime[e] = f_T[e]+s[e_star]
                else:
                    f_prime[e] = f_T[e]+fbar_T[e]*s[e_star]
                    
            f_T = f_prime
            logg.append("in "+str(e_prime)+"  out "+str(e_star))
            
           
        else:

            if e_star in E_T:
                if f_T[e_star] == 1:
                    exceptset.add(e_star)
            else:
                if f_X[e_star] == 1:
                    exceptset.add(e_star)
            if e_prime in exceptset:
                exceptset.remove(e_prime)
                
            E_B, V, MR_inv = update_spanning_tree3(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X)            
            MR_inv = api.test_MR_inv(E_B,V)        
            E_T = E_B[0]
            E_X = E_B[1]
            R = V[0]
            N = V[1]
            logg.append("in "+str(e_prime)+"  out "+str(e_star))
#            print " "
