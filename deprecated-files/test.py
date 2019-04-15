#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tkinter import *

fen = Tk()

class Nombre:
    def __init__(self, value):
        self.value = value
        
    def set(self, value):
        self.value = value

    def get(self):
        return self.value

R1 = IntVar(fen, value = 5)
R2 = IntVar(fen, value = 10)
C1 = DoubleVar(fen, value = 1)
C2 = DoubleVar(fen, value = -0.1)
h = DoubleVar(fen, value = 0)

menubar = Menu(fen)

def preset(animal) :
    R1.set(animal['R1'])
    R2.set(animal['R2'])
    C1.set(animal['C1'])
    C2.set(animal['C2'])
    h.set(animal['h'])
    

guepard1={'R1':2, 'R2':10, 'C1':1, 'C2':-0.1, 'h':-18}
guepard2={'R1':5, 'R2':10, 'C1':1, 'C2':-0.1, 'h':0}
poisson1={'R1':3, 'R2':8, 'C1':2, 'C2':-0.4, 'h':2}
hanneton={'R1':3, 'R2':4, 'C1':6.5, 'C2':-3, 'h':0}
    
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Guépard peasant", command=lambda: preset(guepard1))
menu1.add_command(label="Guépard royal", command=lambda: preset(guepard2))
menu1.add_separator()
menu1.add_command(label="Poisson 1", command=lambda: preset(poisson1))
menu1.add_separator()
menu1.add_command(label="Hanneton", command=lambda: preset(hanneton))
menubar.add_cascade(label="Preset", menu=menu1)

"""
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Modifier la taille", command=alert)
menubar.add_cascade(label="Taille", menu=menu2)"""

fen.config(menu=menubar)

fen.mainloop()
