#!/usr/bin/env python
# -*- coding: utf-8 -*- 

### UNIVERSAL, TURING'S MODEL. 


## --- IMPORTATIONS ----
import matplotlib
matplotlib.use('TkAgg')  # Mode d'utilisation de matplotlib, ici pour fonctionner avec Tkinter
from matplotlib import cm, colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.image as mpimg
import numpy as np
import tkinter as Tk
from tkinter.messagebox import showinfo
from random import choice, randint, shuffle
import pdb


## --- PARAMETRES ---

l = 100   # Taille de la matrice, en nombre de cases
resolution = 1  # Pixel par pouce, choix de la résolution de l'affichege
pas = 500   # Temps (milliseconde) entre chaque mise à jour de la matrice


#---

class Matrice:
    def __init__(self, l):
        self.taille = l
        self.val = np.array([[choice([-1,1]) for i in range(l)] for j in range(l)], dtype=int)
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)
        self.nb = [self.val.sum()]
    
    def update(self, R1, R2, C1, C2, h):   # Met à jour la marice et affiche
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)

        for a in range(-R2+1,R2):
            for b in range(-R2+1, R2):
                if (a,b) != (0,0):
                    if abs(a)<R1 and abs(b)<R1:
                        self.action = plash(a,b,self.val,self.action)  # Calcul des voisins activants
                    
                    else:
                        self.inhib = plash(a,b,self.val,self.inhib) # Calcul des voisins inhibants

        self.regles(C1, C2, h) # Application des règles
        

    def asynchrone(self, i, j, R1, R2, C1, C2, h):   #Attention, retour dans un age sombre !
        action = 0
        inhib = 0
        for x in range(-R2+1,R2):
            for y in range(-R2+1, R2):
                if (x,y) != (0,0):
                    if abs(x)<R1 and abs(y)<R1:
                        action += self.val[(x+i)%l][(y+j)%l]  # Calcul des voisins activants
                    
                    else:
                        inhib += self.val[(x+i)%l][(y+j)%l] # Calcul des voisins inhibants

                        
        m = np.sign(action*C1 + inhib*C2 + h)
        self.val[i][j] = np.choose(m==0, (m,self.val[i][j]))
        

    def old(self):
        self.action = np.zeros((l,l), dtype=int)
        self.inhib = np.zeros((l,l), dtype=int)
        val_copy = np.copy(self.val)
        
        m = np.arange(l)
        shuffle(m)
        n = np.arange(l)
        shuffle(n)
        
        for i in m:
            for j in n:
                for x in range(-R2.get()+1,R2.get()):
                    for y in range(-R2.get()+1, R2.get()):
                        if (x,y) != (0,0) and 0<=x+i<l and 0<=y+j<l:
                            if abs(x)<R1.get() and abs(y)<R1.get():
                                self.action[i][j] += self.val[(x+i)][(y+j)]  # Calcul des voisins activants
                    
                            else:
                                self.inhib[i][j] += self.val[(x+i)][(y+j)] # Calcul des voisins inhibants

                val_copy[i][j] =  self.oldRegles(i,j) # Application des règles
                            
        self.val[:,:] = val_copy
                            
        """for i in range(l):
            for j in range(l):
                for x in range(-R2+1,R2):
                    for y in range(-R2+1, R2):
                        if (x,y) != (0,0) and 0<=x+i<l and 0<=y+j<l :
                            if abs(x)<R1 and abs(y)<R1:
                                self.action[i][j] += self.val[(x+i)][(y+j)]  # Calcul des voisins activants
                    
                            else:
                                self.inhib[i][j] += self.val[(x+i)][(y+j)] # Calcul des voisins inhibants"""
        
       

        
    def regles(self, C1, C2, h):    # Met à jour val, la matrice d'état, en focntion des règles
        m = np.sign(self.action*C1 + self.inhib*C2 + h)
        self.val[:,:] = np.choose(m==0, (m,self.val))  # New Tech !

    def oldRegles(self, i, j):
                sign = self.action[i][j]*C1.get() + self.inhib[i][j]*C2.get() + h.get()
                if sign > 0:
                    return 1
                elif sign < 0:
                    return -1
                else:
                    return self.val[i][j]

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
poisson = cm.winter
rouge = cm.Oranges

## --- FONCTIONS DE CONTROLE ---

class Runner:
    def __init__(self, matrice):
        self.flag = False
        self.n = 0
        self.R1 = R1.get()
        self.R2 = R2.get()
        self.C1 = C1.get()
        self.C2 = C2.get()
        self.h = h.get()
    
    def main(self):
        matrice.update(R1.get(), R2.get())
        nbCellules['text'] = str(matrice.val.sum())
    
    def time(self):
        try:
            matrice.update(self.R1, self.R2, self.C1, self.C2, self.h)
            etape['text'] = str(self.n)
            nb = matrice.val.sum()
            nbCellules['text'] = str(nb)
            matrice.nb.append(nb)
            matrice.affiche()
            self.n += 1
        except:
            showinfo('ERREUR', 'Paramètres incorrects')
            self.flag = False
            
        if self.flag:
            fen.after(5, self.time)
            
    def asynchrone(self):
        etape['text'] = str(self.n)
        x = randint(0,l-1)
        y = randint(0,l-1)
        matrice.asynchrone(x, y, self.R1, self.R2, self.C1, self.C2, self.h)
        
        if (self.n%pas) == 0:
            nb = matrice.val.sum()
            nbCellules['text'] = str(nb)
            matrice.nb.append(nb)
            matrice.affiche()
            
        self.n += 1
        if self.flag:
            fen.after(20, self.asynchrone)

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
        canvas2.draw() # Mise à 0 du graphe

    def set(self):  #  Met à jour les paramètres
        self.R1 = R1.get()
        self.R2 = R2.get()
        self.C1 = C1.get()
        self.C2 = C2.get()
        self.h = h.get()
        print('Set !')


## --- AFFICHAGE ---

matrice = Matrice(l) #Initialisation de la matrice

fen = Tk.Tk()   # Fenêtre Tk principale
fen.title('Universal.')

# --- Style d'affichage (globaux) ---
style = Tk.RIDGE  # Style de relief pour les boutons
haut = 2  # Hauteur des boutons
larg = 10  # Largeur des boutons

# Cadres pour organiser l'affichage : 
cadre_matrice = Tk.Frame(fen)
cadre_matrice.pack(side = Tk.LEFT)

cadre_graph = Tk.Frame(fen)
cadre_graph.pack(side = Tk.LEFT)

cadre_boutons = Tk.Frame(fen)
cadre_boutons.pack(side = Tk.TOP)

cadre_champs = Tk.Frame(fen)
cadre_champs.pack()

cadre_valider = Tk.Frame(fen)
cadre_valider.pack()

cadre_quitter = Tk.Frame(fen)
cadre_quitter.pack(side = Tk.BOTTOM)

f = Figure(figsize=(l/resolution, l/resolution), dpi=resolution)  # Figure d'affichage Matplotlib
img = f.figimage(matrice.val, cmap = noir)  # Création de l'objet image

# Graphique du nombre de cellules vivantes

g = Figure(figsize=(3,3), dpi=100, frameon = False)
graph = g.add_subplot(111)
graph.plot(np.arange(len(matrice.nb)), matrice.nb)

fichier_photo = mpimg.imread("/Users/akim/Google Drive/ISN Python/Project/guepard.png")
h = Figure(figsize=(3,2.5), dpi=100, frameon = False)
photo = h.add_subplot(111)
photo.axis('off')
photo.imshow(fichier_photo)

canvas1 = FigureCanvasTkAgg(f, master = cadre_matrice)  # Création d'un canvas Tk/Matplotlib
canvas1.show()
canvas1.get_tk_widget().pack(side = Tk.LEFT)

canvas2 = FigureCanvasTkAgg(g, master = cadre_graph)  # Création d'un deuxième canvas Tk/Matplotlib
canvas2.show()
canvas2.get_tk_widget().grid(row = 1, column = 1, padx = 5, pady = 5)

canvas3 = FigureCanvasTkAgg(h, master = cadre_graph)  # Création d'un deuxième canvas Tk/Matplotlib
canvas3.show()
canvas3.get_tk_widget().grid(row = 2, column = 1)

#--- Paramètres ---

R1 = Tk.IntVar(fen, value = 5)
R2 = Tk.IntVar(fen, value = 10)
C1 = Tk.DoubleVar(fen, value = 1)
C2 = Tk.DoubleVar(fen, value = -0.1)
h = Tk.DoubleVar(fen, value = 0)

#Presets : 
guepard1={'R1':2, 'R2':10, 'C1':1, 'C2':-0.1, 'h':-18, 'couleur' : jaune}
guepard2={'R1':5, 'R2':10, 'C1':1, 'C2':-0.1, 'h':0, 'couleur' : jaune}
poisson1={'R1':3, 'R2':8, 'C1':2, 'C2':-0.4, 'h':2, 'couleur' : poisson}
hanneton={'R1':3, 'R2':4, 'C1':6.5, 'C2':-3, 'h':0, 'couleur' : rouge}

def preset(animal) :   # Met à jour les réglages
    R1.set(animal['R1'])
    R2.set(animal['R2'])
    C1.set(animal['C1'])
    C2.set(animal['C2'])
    h.set(animal['h'])
    R.set()
    img.cmap = animal['couleur']
    canvas1.draw()

def set_color(couleur):   # Met à jour la couleurs de la map
    img.cmap = couleur
    canvas1.draw()
    
def call_set(event):  # Lorsque que Entrée est préssée, appelle la focntion set() 
    R.set()
    
#--- Barre de menu ---

menubar = Tk.Menu(fen)

menu1 = Tk.Menu(menubar, tearoff=0)
menu1.add_command(label="Guépard peasant", command=lambda: preset(guepard1))
menu1.add_command(label="Guépard royal", command=lambda: preset(guepard2))
menu1.add_separator()
menu1.add_command(label="Poisson 1", command=lambda: preset(poisson1))
menu1.add_separator()
menu1.add_command(label="Hanneton", command=lambda: preset(hanneton))
menubar.add_cascade(label="Presets", menu=menu1)

menu2 = Tk.Menu(menubar, tearoff=0)
menu2.add_command(label="Red", command=lambda: set_color(rouge))
menu2.add_command(label="Black", command=lambda: set_color(noir))
menu2.add_command(label="Fish", command=lambda: set_color(poisson))
menu2.add_command(label="Yellow", command=lambda: set_color(jaune))
menubar.add_cascade(label="Colors", menu=menu2)

fen.config(menu=menubar)

#--- Bouttons ---
            
R = Runner(matrice)
#ButtonGo = Tk.Button(cadre_boutons, text ="GO !", command = R.main)
#ButtonGo.pack(padx = 5, pady = 5)
ButtonTime = Tk.Button(cadre_boutons,text = "Synchrone", command = R.runTime, height = haut, width = larg, relief = style)
ButtonTime.pack(padx = 5,pady = 10)
#ButtonOld = Tk.Button(cadre_boutons,text = "Old",command = R.runOld)
#ButtonOld.pack(padx = 5,pady = 10)
ButtonAsynchrone = Tk.Button(cadre_boutons, text ="Asynchrone", command = R.runAsynchrone, height = haut, width = larg)
ButtonAsynchrone.pack(padx = 5, pady = 5)
ButtonStop = Tk.Button(cadre_boutons, text ="Stop", command = R.stop, height = haut, width = larg)
ButtonStop.pack(padx = 5, pady = 5)
ButtonReset = Tk.Button(cadre_boutons, text ="Reset", command = R.reset, height = haut, width = larg)
ButtonReset.pack(padx = 5, pady = 5)


#--- Champs pour les paramètres -- 

label_R1 = Tk.Label(cadre_champs, text='R1 :')
label_R2 = Tk.Label(cadre_champs, text='R2 :')
label_C1 = Tk.Label(cadre_champs, text='C1 :')
label_C2 = Tk.Label(cadre_champs, text='C2 :')
label_h = Tk.Label(cadre_champs, text='h :')

label_R1.grid(row = 1, column = 1)
label_R2.grid(row = 2, column = 1)
label_C1.grid(row = 3, column = 1)
label_C2.grid(row = 4, column = 1)
label_h.grid(row = 5, column = 1)

ChampR1 = Tk.Entry(cadre_champs, textvariable = R1, width=7)
ChampR2 = Tk.Entry(cadre_champs, textvariable = R2, width=7)
ChampC1 = Tk.Entry(cadre_champs, textvariable = C1, width=7)
ChampC2 = Tk.Entry(cadre_champs, textvariable = C2, width=7)
Champh = Tk.Entry(cadre_champs, textvariable = h, width=7)

ChampR1.bind("<Return>", call_set)
ChampR2.bind("<Return>", call_set)
ChampC1.bind("<Return>", call_set)
ChampC2.bind("<Return>", call_set)
Champh.bind("<Return>", call_set)

ChampR1.grid(row = 1, column = 2, padx = 10)
ChampR2.grid(row = 2, column = 2, padx = 10)
ChampC1.grid(row = 3, column = 2, padx = 10)
ChampC2.grid(row = 4, column = 2, padx = 10)
Champh.grid(row = 5, column = 2, padx = 10)

ButtonValider = Tk.Button(cadre_valider, text="Valider", command = R.set, height = haut, width = larg)
ButtonValider.pack(padx = 5, pady = 10)

BoutonQuitter = Tk.Button(cadre_quitter, text ="Quitter", command = fen.destroy, height = haut, width = larg)
BoutonQuitter.pack(side = Tk.RIGHT, padx = 5, pady = 10)

ChampR1.focus_set()

#--- Labels ---

etape = Tk.Label(cadre_boutons, text='0')  #Compteur de l'avancement (en mol)
etape.pack()

nbCellules = Tk.Label(cadre_boutons, text=str(matrice.val.sum())) # Nombre de cellules vivantes
nbCellules.pack()

#---

fen.mainloop() # Bref, c'est fini. 
