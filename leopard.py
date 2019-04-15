#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Game of Life, version 1

from random import *
from tkinter import *
import time
from numpy import *

fen = Tk()

l = 200   # Taille de la matrice 
c = 4    # facteur multiplicateur (échelle)

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)

matrice = array([[randint(0,1) for i in range(l)] for j in range(l)])


def update(matrice):   # Mise à jour de la matrice
    matrice2 = zeros((l,l), dtype=int)
    for i in range(l):
        for j in range(l):
            voisinP = 0    # Nombre de voisins proches
            voisinL = 0    # Nombre de voisins éloignés
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if 0<=i+x<l and 0<=j+y<l and matrice[i+x][j+y] == 1:
                        if abs(x) + abs(y) == 2:
                            voisinL += 1
                        else:
                            voisinP += 1
            matrice2[i][j] = regles(matrice[i][j], voisinP, voisinL)

    return matrice2


def regles(etat, voisinP, voisinL):   #Application des règles du jeu
    if voisinP + voisinL > choice([3,4,5]):
        return 1
    
    else:
        return 0

    if voisinP > 3:
        return 1

                
def affiche(matrice):    #Affichage de la matrice
    can.delete(ALL)
    for i in range(l):
        for j in range(l):
            if matrice[i][j] == 1:
                can.create_rectangle(c*i, c*j, c*i+c, c*j+c, fill='blue')
            else:
                can.create_rectangle(c*i, c*j, c*i+c, c*j+c, fill='azure2')
                
def main():
    global matrice, flag
    affiche(matrice)
    matrice = update(matrice)

def time():
    global matrice, flag
    affiche(matrice)
    matrice = update(matrice)
    if flag == True:
        fen.after(5, time)

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
ButtonPause = Button(fen, text='Stop', command=stop)
ButtonPause.pack(padx=5, pady=5)
BoutonQuitter = Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)
    
fen.mainloop()

    
