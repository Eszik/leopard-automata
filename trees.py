# Fractal turtle trees

from turtle import *

def regle(chaine):
    
    if chaine == 'A':
        return 'A+A--A+A'
    elif chaine == 'B':
        return 'BAB'
    else :
        return chaine

def iteration(chaine1):
    chaine2 = ""
    for ch in chaine1:
        chaine2 = chaine2 + regle(ch)
        
    return chaine2
    
def chaine(axiome, longueur):
    chaine1 = axiome
    chaine2 = ""
    for i in range(longueur):
        chaine2 = iteration(chaine1)
        chaine1 = chaine2
    
    return chaine2
    
def draw(long, angle, instruction):
    for cmd in instruction:
        if cmd == 'A':
            t.forward(long)
        elif cmd == '-':
            t.right(angle)
        elif cmd == '+':
            t.left(angle)

t = Turtle()
wn = Screen()

t.up()
t.back(200)
t.down()

draw(5,60, chaine('A', 4))
wn.exitonclick()
