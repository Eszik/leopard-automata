#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Game of Life, avec choix de l'état initial

from random import *
from tkinter import *
import time
from numpy import *

fen = Tk()

l = 50   # Taille de la matrice 
c = 15  # facteur multiplicateur (échelle)

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)

matrice = array([[0]*l]*l)

def update(matrice):   # Mise à jour de la matrice
    matrice2 = zeros((l,l), dtype=int)
    for i in range(l):
        for j in range(l):
            voisin = 0    # Nombre de voisins à 1
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if (x,y)!=(0,0) and matrice[(i+x)%l][(j+y)%l] == 1:   # Présence du modulo l : topologie torique !
                        voisin += 1
            matrice2[i][j] = regles(matrice[i][j], voisin)

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
                can.create_rectangle(c*i, c*j, c*i+c, c*j+c, fill='blue')
            else:
                can.create_rectangle(c*i, c*j, c*i+c, c*j+c, fill='azure2')

def click(event):
    x = int(event.x/c)
    y = int(event.y/c)
    can.delete(ALL)
    matrice[x][y] = (matrice[x][y]+1)%2
    affiche(matrice)
    
    
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
        
def pause():
    global flag
    flag = False
    
flag = False       

ButtonGo = Button(fen, text ="GO !", command = main)
ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Button(fen,text = "Time",command = runTime)
ButtonTime.pack(padx = 5,pady = 10)
ButtonPause = Button(fen, text='Pause',command = pause)
ButtonPause.pack(padx=5, pady=5)
BoutonQuitter = Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)

can.bind("<Button-1>", click)
#can.bind("<Button-3>", erase)
affiche(matrice)
fen.mainloop()
