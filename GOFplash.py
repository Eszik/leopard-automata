#!/usr/bin/env python
# -*- coding: utf-8 -*- 

## Game Of Life PLASH PLASH !

from random import *
from tkinter import *
import time as tm
from numpy import *

fen = Tk()

l = 5   # Taille de la matrice 
c = 10  # facteur multiplicateur (échelle)

matrice = array([[choice([0,0, 0, 1]) for i in range(l)] for j in range(l)])  # Matrice de départ, aléatoire

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)

Tplash = 0
Taffiche = 0
Tregles = 0
Ttotal = 0

def plash(a,b, source, base):   # a et b sont les pas de décalage, 'source' la matrice qu'on va ajouter à 'base'
    if a>=0 and b>=0:
        S = source[:l-a,:l-b] + base[a:,b:]
        S = concatenate((base[a:,:b], S), axis=1)
        S = concatenate((base[:a,:], S), axis=0)
        
    elif a>=0 and b<0:
        S = source[:l-a,-b:] + base[a:,:l+b]
        S = concatenate((S, base[a:,l+b:]), axis=1)
        S = concatenate((base[:a,:], S), axis=0)

    elif a<0 and b<=0:
        S = source[-a:,-b:] + base[:l+a,:l+b]
        S = concatenate((S, base[:l+a,l+b:]), axis=1)
        S = concatenate((S, base[l+a:,:]), axis=0)
        
    elif a<0 and b>0:
        S = source[-a:,:l-b] + base[:l+a,b:]
        S = concatenate((base[:l+a,:b],S), axis=1)
        S = concatenate((S, base[l+a:,:]), axis=0)

    return S

def update(matrice):   # Mise à jour de la matrice
    global Tplash, Tregles
    t = tm.time()
    voisins = zeros((l,l), dtype=int)
    matrice2 = zeros((l,l), dtype=int)
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if (a,b) != (0,0):
                voisins = plash(a,b,matrice,voisins)

    Tplash = tm.time() - t
    t = tm.time()
    for i in range(l):
        for j in range(l):        
            matrice2[i][j] = regles(matrice[i][j],voisins[i][j])
    Tregles = tm.time() - t
    return matrice2

def regles(etat, voisin):   #Application des règles du jeu
    if voisin == 3:
        return 1
    
    elif voisin == 2 and etat == 1:
        return 1

    else:
        return 0

                
def affiche(matrice):    #Affichage de la matrice
    can.delete(ALL)
    for i in range(l):
        for j in range(l):
            if matrice[i][j] == 1:
                can.create_rectangle(c*i, c*j, c*i+c, c*j+c, width = 0, fill='blue')
    
def main():
    global matrice, flag, Taffiche, Ttotal
    t = tm.time()
    affiche(matrice)
    Taffiche = tm.time() - t
    matrice = update(matrice)
    Ttotal = tm.time() - t

def time():
    global matrice, flag
    affiche(matrice)
    matrice = update(matrice)
    if flag == True:
        fen.after(1, time)

def runTime():
    global flag
    if flag == False:
        flag = True
        time()

affiche(matrice)

flag = False       
ButtonGo = Button(fen, text ="GO !", command = main)
ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Button(fen,text = "Time",command = runTime)
ButtonTime.pack(padx = 5,pady = 10)
BoutonQuitter = Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)
    
fen.mainloop()
