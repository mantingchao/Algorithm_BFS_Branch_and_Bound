#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:47:50 2021

@author: Manting
"""

import sys
import pandas as pd
import heapq as hq
import time

#%%
df = (pd.read_excel("test instance.xlsx" ,header = None)).transpose() # read excel
proc = df.values.tolist() # transform to list
job = proc[1 : 11]
#job = [[6, 0], [2, 2], [3, 2], [2, 6], [5, 7], [2, 9]]

#%% MinHeap
def heap_insert(arr, n, x):
    j = n - 1
    parent = (j - 1) // 2
    while parent >= 0:
        if x[0] < arr[parent][0]:
            arr[j] = arr[parent]
            j = parent
            if parent == 0:
                break
            parent = (parent - 1) // 2
        else:
            break
    arr[j] = x
    
def heapify(arr, n):
    x = arr[n - 1]
    i = 0
    j = 2 * i + 1
    while j < n:
        if j + 1 < n:
            if arr[j][0] > arr[j + 1][0]:
                j += 1
        if arr[j][0] >= x[0]:
            break
        else:
            arr[(j - 1) // 2] = arr[j]
            j = 2 * j + 1
    arr[(j - 1) // 2] = x
    arr.pop(n - 1)

#%% SRPT
def srptHeap(procc, t):
    #t = 0 # current arrive time
    complete = 0 # already number of finished process
    srpt = [] # heap
    total = 0 # the objective value
    proc = procc.copy()
    job_q = len(proc)
    
    while complete != job_q: # until all processes finished
        while proc !=[] and proc[0][1] <= t:
            srpt.append(proc[0])
            heap_insert(srpt, len(srpt), proc[0].copy())
            proc.remove(proc[0])
            # print(srpt) 
        if len(srpt) != 0 and srpt[0][0] == 0: # heapify
            heapify(srpt, len(srpt))
            complete += 1
            total += t
            # print(total,t)
        if len(srpt) != 0: # reduce remaining time
            srpt[0][0] -= 1
            
        t += 1
    return total 
    
#%% counting makespan and sumC
def SRPT(makespan, seq, sumC):
    if makespan == 0:
        makespan = sum(seq)
        return makespan, makespan
    else:
        if makespan < seq[1]:
            makespan_new = sum(seq)
        else:
            makespan_new = makespan + seq[0]
        return makespan_new, sumC + makespan_new
    
#%% Best First Search
def without(head, job): #return all branch of head
    jobc = job.copy()
    if(type(head[0]) == int):
        jobc.remove(head)
        return jobc
    
    for i in head:
        jobc.remove(i)
    
    return jobc

def BestFS(job):
    c, ub = 0, 0
    heaplst = []
    res = []
    bestval = sys.maxsize
    
    for i in job:
        LB = sum(i) + srptHeap(without(i, job), sum(i)) 
        #print(LB,i,without(i,job))
        c += 1
        hq.heappush(heaplst, [LB, [i], sum(i), sum(i)])
        
    while(heaplst[0][0] < bestval):
        heappop = hq.heappop(heaplst)
        head = heappop[1]
        makespan = heappop[2]
        sumc = heappop[3]
        
        for i in without(head, job):
            headc = head.copy()
            headc.append(i)
            makespan_n, sumC_n = SRPT(makespan, i, sumc)
            
            if len(headc) == len(job):
                if sumC_n < bestval:
                    bestval = sumC_n
                    res = headc
                    ub += 1
            else:
                LB = sumC_n + srptHeap(without(headc, job), makespan_n)
                if LB < bestval:
                    c += 1
                    hq.heappush(heaplst, [LB, headc, makespan_n, sumC_n])
                   
    return bestval, res, c, ub

#%% main()
s = time.time()
a, b, c, ub = BestFS(job)
e = time.time()
print('\nBestFS:')
print(' Objective value: ', a,'\n Optimal permutation: ', b, '\n BestFS run time:', e-s)
print(' count: ', c)  
print(' UB下降次數: ', ub) 
