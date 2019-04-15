#!/usr/bin/env python
# -*- coding: utf-8 -*- 

## PLASH PLASH  

from random import *
from tkinter import *
import time
from numpy import *

l = 10

matrice = array([[choice([0,1]) for i in range(l)] for j in range(l)])
action = zeros((l,l), dtype=int)
inhib = zeros((l,l), dtype=int)


def plash(a,b):
    if a>=0 and b>= 0:
        S = matrice[:-a,:-b] + action[a:,b:]
        S = concatenate((action[a:,:b], S), axis=1)
        S = concatenate((action[:a,:], S), axis=0)
        
    elif a>=0 and b<0:
        S = matrice[:-a,b:] + action[a:,:-b]
        S = concatenate((S, action[a:,-b:]), axis=1)
        S = concatenate((action[:a,:], S), axis=0)

    elif a<0 and b<=0:
        S = matrice[a:,b:] + action[:-a,:-b]
        S = concatenate((S, action[:-a,-b:]), axis=1)
        S = concatenate((S, action[-a:,:]), axis=0)
        
    elif a<0 and b>0:
        S = matrice[a:,:-b] + action[:-a,b:]
        S = concatenate((S, action[:-a,:b]), axis=1)
        S = concatenate((S, action[-a:,:]), axis=0)
    
    return S
