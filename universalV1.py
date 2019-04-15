#!/usr/bin/env python
# -*- coding: utf-8 -*- 

### UNIVERSAL, TURING'S MODEL. 


## --- IMPORTATIONS ----
import matplotlib
matplotlib.use('TkAgg')  # Mode d'utilisation de matplotlib, ici pour fonctionner avec Tkinter
from matplotlib import cm, colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import tkinter as Tk
from random import choice, randint


## --- PARAMETRES ---

l = 100   # Taille de la matrice, en nombre de cases
resolution = 100  # Pixel par pouce, choix de la résolution de l'affichege
pas = 50   # Temps (milliseconde) entre chaque mise à jour de la matrfice

R1 = 2
R2 = 10
C1 = 1
C2 = -0.1
h = -18
#---

""" Exemples de paramètre :
R1 = 3
R2 = 5
C1 = 1
C2 = -0.1
h = 0

"""

class Matrice:
    def __init__(self, l):
        self.taille = l
        self.val = np.array([[choice([-1,1]) for i in range(l)] for j in range(l)], dtype='int')
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)
        self.nb = [self.val.sum()]
    
    def update(self):   # Met à jour la marice et affiche
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)

        # Calcul des voisins activants :
        for a in range(-R1+1,R1):
            for b in range(-R1+1, R1):
                if (a,b) != (0,0):
                    self.action = plash(a,b,self.val,self.action)

        # Calcul des voisins inhibants :
        for a in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
            for b in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
                self.inhib = plash(a,b,self.val,self.inhib)

        self.regles() # Application des règles
        

    def asynchrone(self, i, j):   #Attention, retour dans un age sombre !
        action = 0
        inhib = 0
        for x in range(-R1+1,R1):
            for y in range(-R1+1, R1):
                if (x,y) != (0,0):
                    action += self.val[(x+i)%l][(y+j)%l]
                            
        for x in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
            for y in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
                inhib += self.val[(x+i)%l][(y+j)%l]
                        
        m = np.sign(action*C1 + inhib*C2 + h)
        self.val[i][j] = np.choose(m==0, (m,self.val[i][j]))
        

    def old(self):
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)

        for i in range(l):
            for j in range(l):
                # Calcul des voisins activants :
                for a in range(-R1+1,R1):
                    for b in range(-R1+1, R1):
                        if (a,b) != (0,0):
                            if 0<=a+i<l and 0<=b+j<l :
                                self.action[a+i][b+j] += self.val[a+i][b+j]

                # Calcul des voisins inhibants :
                for a in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
                    for b in np.concatenate((np.arange(-R2+1,-R1+1),np.arange(R1,R2)),axis=0):
                        if 0<=a+i<l and 0<=b+j<l :
                            self.inhib[a+i][b+j] += self.val[a+i][b+j]

        self.regles() # Application des règles

        
    def regles(self):    # Met à jour val, la matrice d'état, en focntion des règles
        m = np.sign(self.action*C1 + self.inhib*C2 + h)
        self.val[:,:] = np.choose(m==0, (m,self.val[:,:]))  # New Tech !

    def affiche(self):
        canvas1.draw() # Mise à jour de l'image
        
        graph.clear()
        graph.plot(np.arange(len(self.nb)), self.nb)
        canvas2.draw() # Mise à jour du graphique
    

#---

def plash(a,b, ajout, base):   # a et b sont les pas de décalage, 'ajout' la matrice qu'on va ajouter à 'base'
    if a>=0 and b>=0:
        S = ajout[:l-a,:l-b] + base[a:,b:]
        S = np.concatenate((base[a:,:b], S), axis=1)
        S = np.concatenate((base[:a,:], S), axis=0)
        
    elif a>=0 and b<0:
        S = ajout[:l-a,-b:] + base[a:,:l+b]
        S = np.concatenate((S, base[a:,l+b:]), axis=1)
        S = np.concatenate((base[:a,:], S), axis=0)

    elif a<0 and b<=0:
        S = ajout[-a:,-b:] + base[:l+a,:l+b]
        S = np.concatenate((S, base[:l+a,l+b:]), axis=1)
        S = np.concatenate((S, base[l+a:,:]), axis=0)
        
    elif a<0 and b>0:
        S = ajout[-a:,:l-b] + base[:l+a,b:]
        S = np.concatenate((base[:l+a,:b],S), axis=1)
        S = np.concatenate((S, base[l+a:,:]), axis=0)

    return S

## --- COULEURS ---
noir = cm.Greys
jaune = cm.gnuplot

## --- AFFICHAGE ---

matrice = Matrice(l) #Initialisation de la matrice

fen = Tk.Tk()   # Fenêtre Tk principale
f = Figure(figsize=(l/resolution, l/resolution), dpi=resolution)  # Figure d'affichage Matplotlib

img = f.figimage(matrice.val, cmap = noir)  # Création de l'objet image

# Graphique du nombre de cellules vivantes
g = Figure(figsize=(4,4), dpi=resolution)
graph = g.add_subplot(111)
graph.plot(np.arange(len(matrice.nb)), matrice.nb)

canvas1 = FigureCanvasTkAgg(f, master = fen)  # Création d'un canvas Tk/Matplotlib
canvas1.show()
canvas1.get_tk_widget().pack(side = Tk.LEFT, fill=Tk.BOTH, expand=1)

canvas2 = FigureCanvasTkAgg(g, master = fen)  # Création d'un deuxième canvas Tk/Matplotlib
canvas2.show()
canvas2.get_tk_widget().pack(side = Tk.LEFT)


## --- FONCTIONS DE CONTROLE ---

class Runner:
    def __init__(self, matrice):
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
        matrice.affiche()
        self.n += 1
        if self.flag:
            fen.after(pas, self.time)
            
    def asynchrone(self):
        etape['text'] = str(self.n)
        x = randint(0,l-1)
        y = randint(0,l-1)
        matrice.asynchrone(x,y)
        
        if (self.n%pas) == 0:
            nb = matrice.val.sum()
            nbCellules['text'] = str(nb)
            matrice.nb.append(nb)
            matrice.affiche()
            
        self.n += 1
        if self.flag:
            fen.after(0, self.asynchrone)

    def old(self):
        matrice.old()
        matrice.affiche()
        if self.flag:
            fen.after(0, self.old)

    def runTime(self):
        if self.flag == False:
            self.flag = True
            self.n = 0
            self.time()
            
    def runAsynchrone(self):
        if self.flag == False:
            self.flag = True
            self.n = 0
            self.asynchrone()
            
    def runOld(self):
        if self.flag == False:
            self.flag = True
            self.n = 0
            self.old()

    def stop(self):
        print ("stopping !")
        self.flag = False

    def reset(self):
        self.flag = False
        self.n = 0
        matrice.val[:,:] = np.array([[choice([-1,1]) for i in range(l)] for j in range(l)], dtype='int')
        matrice.nb = [matrice.val.sum()]
        canvas1.draw() # Mise à 0 de l'image
        graph.clear()
        canvas2.draw() #Mise à 0 du graph
            
R = Runner(matrice)
ButtonGo = Tk.Button(fen, text ="GO !", command = R.main)
ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Tk.Button(fen,text = "Time",command = R.runTime)
ButtonTime.pack(padx = 5,pady = 10)
ButtonOld = Tk.Button(fen,text = "Old",command = R.runOld)
ButtonOld.pack(padx = 5,pady = 10)
ButtonAsynchrone = Tk.Button(fen, text ="Asynchrone", command = R.runAsynchrone)
ButtonAsynchrone.pack(padx = 5, pady = 5)
ButtonStop = Tk.Button(fen, text ="Stop", command = R.stop)
ButtonStop.pack(padx = 5, pady = 5)
ButtonReset = Tk.Button(fen, text ="Reset", command = R.reset)
ButtonReset.pack(padx = 5, pady = 5)
BoutonQuitter = Tk.Button(fen, text ="Quitter", command = fen.destroy)
BoutonQuitter.pack(padx=5, pady=5)

etape = Tk.Label(fen, text='0')  #Compteur de l'avancement (en mol)
etape.pack()
    
nbCellules = Tk.Label(fen, text=str(matrice.val.sum())) # Nombre de cellules vivantes
nbCellules.pack()

fen.mainloop()
