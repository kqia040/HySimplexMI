# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 10:23:53 2017

up

@author: Kun
"""




import copy
from update_MR_Inv import update_MR_inv
import api

def update_spanning_tree3(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X):
    #ebar is the cirtical edge
    Case = None
    R = V[0]
    N = V[1]    
#    RR = set(V[0])    
#    if e_star[1] is not None:
#        if e_star[0] is None:
#            e_star_head_tail_set_union = {e_star[1]}
#        else:
#            e_star_head_tail_set_union = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1]), e_star[1]}
#    elif e_star[1] is None:
#        e_star_head_tail_set_union = {e_star[0]}
        
    
    if e_prime[1] is not None:
        if e_prime[0] is None:
            e_prime_head_tail_set_union = {e_prime[1]}
        else:
            e_prime_head_tail_set_union = {e_prime[0], (e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1]), e_prime[1]}
    elif e_prime[1] is None:
        e_prime_head_tail_set_union = {e_prime[0]}        
        
        
        
    #case1
    if e_star in E_B[1]:
        if (not e_prime_head_tail_set_union.issubset(R)):           
            Case = '1a'
#            print '1a'
            newV = copy.deepcopy(V)
            newE_B = copy.deepcopy(E_B)
            newE_B[1][newE_B[1].index(e_star)] = e_prime
            newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
            return newE_B, newV, newMR_inv
        else:
            #this case will never happen
#==============================================================================
#           need to select node in R to remove            
#==============================================================================
#            tempset = copy.deepcopy(e_prime_head_tail_set_union)
            v_remove_from_R = e_prime[0]            
#            for v in R:
#                if v in tempset:
#                    v_remove_from_R = v
#                    break
#            if v_remove_from_R is None:
#                print "errrrrrorrr, at v_remove from R for case 1b" 
            Case = '1b'
#            print '1b'
            newV = copy.deepcopy(V)
            newE_B = copy.deepcopy(E_B)
            newE_B[1].remove(e_star)
            newE_B[0].append(e_prime)
            newV[0].remove(v_remove_from_R)
            newV[1].append(v_remove_from_R)
            newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)            

            
            return newE_B, newV, newMR_inv
        
    elif e_star in E_B[0]:
        #if e is a tree arc
        
        #if e_bar
        #if critical edge exisits        
#        v_list, e_list = api.correct_traverse(E_B, V)
        e_bar = api.e_bar_simple(E_B, e_star)
        
#        if e_bar is not None and fbar_X[e_bar] == 0:
#            e_bar = None
#   
        
#==============================================================================
#         NEED TO CHECK THIS CASE
#==============================================================================
        
        if e_bar is not None:
            #here need to update the E_B
            Case = '2a'
            newV = copy.deepcopy(V)
            intermediateE_B = copy.deepcopy(E_B)
            intermediateE_B[0][intermediateE_B[0].index(e_star)] = e_bar
            intermediateE_B[1][intermediateE_B[1].index(e_bar)] = e_star
            intermediateMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, intermediateE_B, e_star, e_bar, fbar_T, fbar_X)
#            Case = '2a-second-iteration'
#            newE_B = copy.deepcopy(intermediateE_B)
#            newE_B[1][newE_B[1].index(e_star)] = e_prime
#            newMR_inv = update_MR_inv(Case, intermediateMR_inv, V, newV, intermediateE_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    
            if (not e_prime_head_tail_set_union.issubset(R)):           
                Case = '1a'
#                print '2a1a'
                newV = copy.deepcopy(V)
                newE_B = copy.deepcopy(intermediateE_B)
                newE_B[1][newE_B[1].index(e_star)] = e_prime
                newMR_inv = update_MR_inv(Case, intermediateMR_inv, V, newV, intermediateE_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                return newE_B, newV, newMR_inv
            
            else:
                #this case will never happen
    #==============================================================================
    #           need to select node in R to remove            
    #==============================================================================
    #            tempset = copy.deepcopy(e_prime_head_tail_set_union)
                v_remove_from_R = e_prime[0]            
    #            for v in R:
    #                if v in tempset:
    #                    v_remove_from_R = v
    #                    break
    #            if v_remove_from_R is None:
    #                print "errrrrrorrr, at v_remove from R for case 1b" 
                Case = '1b'
#                print '2a1b'
                newV = copy.deepcopy(V)
                newE_B = copy.deepcopy(intermediateE_B)
                newE_B[1].remove(e_star)
                newE_B[0].append(e_prime)
                newV[0].remove(v_remove_from_R)
                newV[1].append(v_remove_from_R)
                newMR_inv = update_MR_inv(Case, intermediateMR_inv, V, newV, intermediateE_B, newE_B, e_prime, e_star, fbar_T, fbar_X)            
    
                
                return newE_B, newV, newMR_inv
#        

        #if tehre is no critical edge!
        else:

#==============================================================================
#             find v_bar            
#==============================================================================
#            len_v_list = len(v_list)            
            v_bar_e_star = None

            if e_star[0] is None:
                v_bar_e_star = e_star[1]
            else:
                v_bar_e_star = e_star[0]
                        
               
            v_bar_e_prime = None
            if e_prime[0] is None:
                v_bar_e_prime = e_prime[1]
            else:
                v_bar_e_prime = e_prime[0]

                
            
            
#            flag = True
#            for e in E_B[0]:
#                if e == e_star:
#                    continue
#                elif e[0] == e_prime[0]:
#                    flag = False
#            
#            if v_bar_e_star == v_bar_e_prime and flag:
            if v_bar_e_star == v_bar_e_prime:
                #eprime replace estar as a tree arc
                Case = '2b1'
#                print '2b1'
                newV = copy.deepcopy(V) 
                newE_B = copy.deepcopy(E_B)  
                newE_B[0].append(e_prime)
                newE_B[0].remove(e_star)
                
                newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    

                return newE_B, newV, newMR_inv

                
            else:
                #the last case 2b2
                #case1
                if not(e_prime_head_tail_set_union.issubset(V[0])):
                    newV = copy.deepcopy(V)
                    newV[0].append(v_bar_e_star)
                    newV[1].remove(v_bar_e_star)
                    Case = '2b2'
                    newE_B = copy.deepcopy(E_B)   
                    newE_B[1].append(e_prime)
                    newE_B[0].remove(e_star)
                    
                    newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
#                    print '2b2a'

                    return newE_B, newV, newMR_inv
                else:
                    newV = copy.deepcopy(V)                    
                    newE_B = copy.deepcopy(E_B) 
                    v_remove_from_R = e_prime[0]                       
#                    for v in e_prime_head_tail_set_union:
#                        if v in V[0]:
                    newV[0].remove(v_remove_from_R)
                    newV[1].append(v_remove_from_R)
#==============================================================================
#                           this following line could be wrong                            
#==============================================================================
                    newV[0].append(v_bar_e_star)
                    newV[1].remove(v_bar_e_star)                            
                    
#                            break
                    
                    newE_B[0].append(e_prime)
                    newE_B[0].remove(e_star)
                    Case = '2b2'                    
                    newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
#                    print '2b2b'

                    return newE_B, newV, newMR_inv