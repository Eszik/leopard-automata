#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from random import randint
from tkinter import *
import time
from numpy import *

fen = Tk()

l = 200 # Taille de la matrice 
c = 1   # facteur multiplicateur (échelle)

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)

matrice = array([[randint(0,1) for i in range(l)] for j in range(l)])


def update(matrice):   # Mise à jour de la matrice
    matrice2 = zeros((l,l), dtype=int)
    voisins = zeros((l,l,2), dtype=int)
    for i in range(l):
        for j in range(l):
            if matrice[i][j] == 1:
                for x in [-1,0,1]:
                    for y in [-1,0,1]:
                        if abs(x) + abs(y) == 2:
                            voisins[(x+i)%l][(y+j)%l][1] +=1
                        else:
                            voisins[(x+i)%l][(y+j)%l][0] +=1
    for i in range(l):
        for j in range(l):            
            matrice2[i][j] = regles(matrice[i][j], voisins[i][j][0], voisins[i][j][1])

    return matrice2


def regles(etat, voisinsProches, voisinsEloignes):   #Application des règles du jeu
    if voisinsProches + voisinsEloignes > randint(3,5):
        return 1
    
    elif voisinsProches > 3:
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
    global matrice, flag
    affiche(matrice)
    matrice = update(matrice)

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

def stop():
    global flag
    flag = False
    
flag = False       
ButtonGo = Button(fen, text ="GO !", command = main)
ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Button(fen,text = "Time",command = runTime)
ButtonTime.pack(padx = 5,pady = 10)
ButtonStop = Button(fen,text = "Stop",command = stop)
ButtonStop.pack(padx = 5,pady = 10)
    
fen.mainloop()

    
