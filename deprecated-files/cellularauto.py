# -*- coding: utf-8 -*- 


# game of life 

from random import randint
from tkinter import *
import time

fen = Tk()

l = 5   # Taille de la matrice 
c = 30    # facteur multiplicateur (échelle)

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)

matrice = [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 1, 1, 1, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]


def update(matrice):   # Mise à jour de la matrice
    m = [[0]*l]*l
    for i in range(l):
        for j in range(l):
            voisin = 0    # Nombre de voisins à 1
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if 0<=i+x<l and 0<=j+y<l and (x,y)!=(0,0) and matrice[i+x][j+y] == 1:
                        voisin += 1
            m[i][j] = regles(matrice[i][j], voisin)

    return m


def regles(etat, voisin):   #Application des règles du jeu
    if voisin == 3 and etat == 0:
        return 1
    
    elif voisin == 2:
        return etat

    elif voisin < 2 or voisin > 3:
        return 0

                
def affiche(matrice):    #Affichage de la matrice
    can.delete(ALL)
    for i in range(l):
        for j in range(l):
            if matrice[i][j] == 1:
                can.create_rectangle(c*i+1, c*j+1, c*i+c, c*j+c, fill='blue')
            else:
                can.create_rectangle(c*i+1, c*j+1, c*i+c, c*j+c, fill='azure2')

def main():
    global matrice, flag
    affiche(matrice)
    matrice = update(matrice)
    """if flag == True:
        fen.after(1000, main)"""

def run():
        main()

flag = False       
ButtonGo = Button(fen, text ="GO !", command = run)
ButtonGo.pack(padx = 5, pady = 5)
    
fen.mainloop()

"""for a in range(10):
    affiche(matrice1)
    matrice1 = update(matrice1)
    print('Ok')
    time.sleep(1)"""
    
