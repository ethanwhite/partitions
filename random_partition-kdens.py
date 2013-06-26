#!/usr/bin/env sage -python

from sage.all import *
import sys
sys.path.append("/home/kenlocey/metrics")
import metrics
import partitions as parts
import os
from os import path, access, R_OK  # W_OK for write permission
import  matplotlib.pyplot as plt
from pylab import *
import numpy as np
from scipy.stats import gaussian_kde
from scipy import stats
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import re
import math

""" The code below compares random partitioning nplottions of Sage and Locey and McGlinn (20??)
    to full feasible sets. These analyses confirm that the nplottion of L&M (20??) are unbiased.
    The figure generated by the code below contains a lot of info. The code uses full feasible sets,
    the random partitioning nplottion in Sage, and the random partitioning nplottions developed in
    L&M (20??), both for cases when 0' are or are not allowed.
    
    The code generates figure 1 of Locey and McGlinn (20??) """

witches = ['multiplicity','top_down','divide_and_conquer','bottom_up']
colors = ['r','b','m','g']

fig = plt.figure()
nplot = 1 # a variable used to designate which nplottions and analyses are used for particular subplots
sample_size = 500 # min number of macrostates needed to safely capture distributional features
                  # across the feasible set

while nplot <= 4:
    ax = ax = fig.add_subplot(2,2,nplot)

    if nplot < 3:
        Q = 50
        N = 10
    else:
        Q = 500 # The full feasible set can't be generated for N = 500 & S = 50
        N = 50
    
    for i in range(1,6):
        partitions = []
        for i, which in enumerate(witches):
            if nplot == 1 or nplot == 3:
                zeros = 'no'
                partitions = parts.rand_parts(Q,N,sample_size,which,zeros)
            else:
                zeros = 'yes'
                partitions = parts.rand_parts(Q,N,sample_size,which,zeros)
            #D = metrics.get_kdens_obs_Evar(partitions) # evenness
            #D = metrics.get_kdens_obs_gini(partitions) # inequality
            D = metrics.get_kdens_obs_var(partitions) # variance
            #D = metrics.get_kdens_obs_skew(partitions) # skewness
            #D = metrics.get_kdens_obs_MD(partitions)  # median summand
            plt.xlim(min(D[0]),max(D[0]))
            plt.plot(D[0],D[1],color=colors[i],lw=0.7)
        
    
    if nplot == 1: # using the full feasible set, no zero values (i.e. proper integer partitions)
        for i in range(1,2):
            partitions = []
            for p in Partitions(Q,length=N):
                partitions.append(p)
        
        #D = metrics.get_kdens_obs_Evar(partitions) # evenness
        #D = metrics.get_kdens_obs_gini(partitions) # inequality
        D = metrics.get_kdens_obs_var(partitions) # variance
        #D = metrics.get_kdens_obs_skew(partitions) # skewness
        #D = metrics.get_kdens_obs_MD(partitions)  # median summand
        plt.xlim(min(D[0]),max(D[0]))
        plt.plot(D[0],D[1],color='k',lw=3,alpha=0.5)
        
    elif nplot == 2: # using the full feasible set, zero values included
        for i in range(1,2):
            partitions = []    
            n = 1
            while n <= N:
                
                numparts = parts.NrParts(Q,n)    
                part = parts.firstpart(Q,n,None)
                ct2 = 0
                while ct2 < numparts:
                    
                    part = parts.next_restricted_part(part)
                    if len(part) == N: partitions.append(part) 
                    else:
                        part2 = list(part)
                        zeros = [0]*(N-len(part))
                        part2.extend(zeros)
                        partitions.append(part2)
                        
                    #print nplot,numparts-ct2
                    ct2+=1
                n+=1
        #D = metrics.get_kdens_obs_Evar(partitions) # evenness
        #D = metrics.get_kdens_obs_gini(partitions) # inequality
        D = metrics.get_kdens_obs_var(partitions) # variance
        #D = metrics.get_kdens_obs_skew(partitions) # skewness
        #D = metrics.get_kdens_obs_MD(partitions)  # median summand
        plt.xlim(min(D[0]),max(D[0]))
        plt.plot(D[0],D[1],color='k',lw=3,alpha=0.5)
    
    elif nplot == 3: 
        for i in range(1,6):
            partitions = []
            while len(partitions) < sample_size: # Use the random partition nplottion in Sage to generate a sample of partitions for N and S
                part = Partitions(Q).random_element()
                if len(part) == N:
                    partitions.append(part)
                   #print nplot,i, sample_size - len(partitions)   
                else:
                    part = list(Partition(part).conjugate())
                    if len(part) == N:
                        partitions.append(part)
                        #print nplot,i,sample_size - len(partitions)   
            #D = metrics.get_kdens_obs_Evar(partitions) # evenness
            #D = metrics.get_kdens_obs_gini(partitions) # inequality
            D = metrics.get_kdens_obs_var(partitions) # variance
            #D = metrics.get_kdens_obs_skew(partitions) # skewness
            #D = metrics.get_kdens_obs_MD(partitions)  # median summand
            plt.xlim(min(D[0]),max(D[0]))
            plt.plot(D[0],D[1],color='k',lw=0.7,alpha=0.6)
        
        
    elif nplot == 4:
        for i in range(1,6):
            partitions = []
            while len(partitions) < sample_size: # Use the random partition nplottion in Sage to generate a sample of partitions for N and S
                part = list(Partitions(Q).random_element())
                if len(part) == N:
                    partitions.append(part)
                elif len(part) < N:
                    zeros = [0]*(N-len(part))
                    part.extend(zeros)
                    partitions.append(part)
                
                #print nplot,i,sample_size - len(partitions)   
            #D = metrics.get_kdens_obs_Evar(partitions) # evenness
            #D = metrics.get_kdens_obs_gini(partitions) # inequality
            D = metrics.get_kdens_obs_var(partitions) # variance
            #D = metrics.get_kdens_obs_skew(partitions) # skewness
            #D = metrics.get_kdens_obs_MD(partitions)  # median summand
            plt.xlim(min(D[0]),max(D[0]))
            if nplot == 4:  plt.ylim(0,0.01)
            elif nplot == 3: plt.ylim(0,0.01)
            #else: plt.ylim(0,max(D[1])+0.02)
            plt.plot(D[0],D[1],color='k',lw=0.7,alpha=0.6)
                
                     
    if nplot == 1 or nplot == 3:
        plt.plot([0],[0], color='r', lw=2, label = 'Multi')
        plt.plot([0],[0], color='b',lw=2, label='T-D')    
        plt.plot([0],[0], color='m',lw=2, label='D&Q')
        plt.plot([0],[0], color='g',lw=2, label='B-U')
        plt.plot([0],[0], color='k',lw=2, label='F-S, Q='+str(Q)+',N='+str(N),alpha=0.5)
        plt.ylabel("pdf",fontsize=8)    
    else:
    
        plt.plot([0],[0], color='r', lw=2, label = 'Multi')
        plt.plot([0],[0], color='b',lw=2, label='T-D')    
        plt.plot([0],[0], color='m',lw=2, label='D&Q')
        plt.plot([0],[0], color='g',lw=2, label='B-U')
        plt.plot([0],[0], color='k',lw=2, label='F-S, Q='+str(Q)+',N='+str(N)+', zeros',alpha=0.5)    
        
    print nplot
    nplot+=1
        
    plt.tick_params(axis='both', which='major', labelsize=8)
    leg = plt.legend(loc=1,prop={'size':8})        
    leg.draw_frame(False)

plt.savefig('/home/kenlocey/randpart-kdens_'+str(sample_size)+'.png', dpi=400, pad_inches=0)
