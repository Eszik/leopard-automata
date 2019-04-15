#!/usr/bin/env python
# -*- coding: utf-8 -*- 

## Game Of Life PLASH PLASH !

## --- IMPORTATIONS ----
import matplotlib
matplotlib.use('TkAgg')  # Mode d'utilisation de matplotlib, ici pour fonctionner avec Tkinter
from matplotlib import pyplot as plt
from matplotlib import cm, colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import tkinter as Tk


## --- PARAMETRES ---

l = 1000   # Taille de la matrice, en nombre de cases
resolution = 100  # Pixel par pouce, choix de la résolution de l'affichege
pas = 0   # Temps (milliseconde) entre chaque mise à jour de la matrice
#---


class Matrice:
    def __init__(self, l):
        self.taille = l
        self.val = np.random.randint(0,2,(l,l)).astype(bool)
        self.voisins = np.zeros((l,l), dtype=int)
        self.nb = [self.val.sum()]
    
    def update(self):
        self.voisins = np.zeros((l,l), dtype=int)
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if (a,b) != (0,0):
                    self.voisins = plash(a,b,self.val,self.voisins)

        self.regles()
        canvas1.draw()
        
        graph.clear()
        graph.plot(np.arange(len(self.nb)), self.nb)
        canvas2.draw()


    def regles(self):    # Met à jour val, la matrice d'état, en fonction des règles
        m = (self.voisins == 3)
        self.val[:,:] = np.logical_or(m, np.logical_and( (self.voisins == 2), (self.val == 1) ))



def plash(a,b, source, base): # a et b sont les pas de décalage, 'source' la matrice qu'on va ajouter à 'base'
    if a>=0 and b>=0:
        S = source[:l-a,:l-b] + base[a:,b:]
        S = np.concatenate((base[a:,:b], S), axis=1)
        S = np.concatenate((base[:a,:], S), axis=0)
        
    elif a>=0 and b<0:
        S = source[:l-a,-b:] + base[a:,:l+b]
        S = np.concatenate((S, base[a:,l+b:]), axis=1)
        S = np.concatenate((base[:a,:], S), axis=0)

    elif a<0 and b<=0:
        S = source[-a:,-b:] + base[:l+a,:l+b]
        S = np.concatenate((S, base[:l+a,l+b:]), axis=1)
        S = np.concatenate((S, base[l+a:,:]), axis=0)
        
    elif a<0 and b>0:
        S = source[-a:,:l-b] + base[:l+a,b:]
        S = np.concatenate((base[:l+a,:b],S), axis=1)
        S = np.concatenate((S, base[l+a:,:]), axis=0)

    return S



class Runner:
    def __init__(self):
        self.flag = False
        self.n = 0
    
    def main(self):
        matrice.update()
        nbCellules['text'] = str(matrice.val.sum())
    
    def time(self):
        matrice.update()
        etape['text'] = str(self.n)
        nb = matrice.val.sum()
        nbCellules['text'] = str(nb)
        matrice.nb.append(nb)
        self.n += 1
        if self.flag == True:
            fen.after(pas, self.time)

    def runTime(self):
        if self.flag == False:
            self.flag = True
            self.n = 0
            self.time()

## --- AFFICHAGE ---
matrice = Matrice(l) #Initialisation de la matrice

fen = Tk.Tk()   # Fenêtre Tk principale
f = Figure(figsize=(l/resolution, l/resolution), dpi=resolution)  # Figure d'affichage Matplotlib
img = f.figimage(matrice.val, cmap = cm.Greys)  # Création de l'objet image

g = Figure(figsize=(4,4), dpi=resolution)
graph = g.add_subplot(111)
graph.plot(np.arange(len(matrice.nb)), matrice.nb)

canvas1 = FigureCanvasTkAgg(f, master = fen)  # Création du canvas Tk/Matplotlib
canvas1.show()
canvas1.get_tk_widget().pack(side = Tk.LEFT)

canvas2 = FigureCanvasTkAgg(g, master = fen)  # Création du canvas Tk/Matplotlib
canvas2.show()
canvas2.get_tk_widget().pack(side = Tk.LEFT)
#---

R = Runner()
ButtonGo = Tk.Button(fen, text ="GO !", command = R.main)
ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Tk.Button(fen,text = "Time",command = R.runTime)
ButtonTime.pack(padx = 5,pady = 10)
BoutonQuitter = Tk.Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)

etape = Tk.Label(fen, text='0')
etape.pack()

nbCellules = Tk.Label(fen, text=str(matrice.val.sum()))
nbCellules.pack()
    
fen.mainloop()
