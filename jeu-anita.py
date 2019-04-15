#!/usr/bin/env python
# -*- coding: utf-8 -*- 


## Jeu Anita (Game Of life)
# But : tuer toutes les cellules le plus rapidement possible


from random import *
from tkinter import *
from tkinter.messagebox import showinfo
import time
from numpy import *

fen = Tk()
fen.title('Jeu Anita')

log = []
f = open('nb-cellules.txt', 'w')

l = 50   # Taille de la matrice 
c = 15  # facteur multiplicateur (échelle)

can = Canvas(fen, width=c*l, height = c*l)
can.pack(side = LEFT, padx = 5, pady = 5)


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
    
def check(matrice):
    return matrice.any()

def win():
    showinfo('VCTOIRE !', 'Votre temps : ' + str(int(n/10)))
    f.close()


def time():
    global matrice, flag, n
    matrice = update(matrice)
    affiche(matrice)
    n+= 1
    temps['text'] = 'Temps : ' + str(int(n/10))
    sum = matrice.sum()
    score['text'] = 'Cellules : ' + str(sum)
    log.append(sum)
    f.write(str(sum)+'\n')
    f.flush()
    flag = check(matrice)
    if flag:
        fen.after(1, time)
    else:
        fen.after(100,win)

def runTime():
    global flag
    if flag == False:
        flag = True
        time()
        
def pause():
    global flag
    flag = False

def new():
    global flag, matrice, n
    flag = False
    n = 0
    matrice = array([[choice([0,0,0,0,0,1]) for i in range(l)] for j in range(l)])
    affiche(matrice)

new()
    
ButtonGo = Button(fen,text = "Go !",command = runTime)
ButtonGo.pack(padx = 5,pady = 10)
ButtonPause = Button(fen, text='Pause',command = pause)
ButtonPause.pack(padx=5, pady=5)
BoutonQuitter = Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)
ButtonNouveau = Button(fen, text = "Nouvelle partie", command = new)
ButtonNouveau.pack(padx=5, pady=5)


temps = Label(fen, text='Temps : 0')  #Compteur de l'avancement (en mol)
temps.pack()
score = Label(fen, text = 'Cellules : ' + str(matrice.sum()))
score.pack()

can.bind("<Button-1>", click)
can.focus_set()

showinfo('NEW', 'Découvrez les règles qui régissent cet univers et stoppez la terrible invasion par les cellules bleues !')

fen.mainloop()

