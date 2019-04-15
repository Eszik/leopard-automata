## Jeu de la vie
# Direction du projet : Flora Gaudillière
# Programmation : Maud Biquard et Vincent Blavy

## Modules utilisés
from tkinter import *
from random import *


### Fenêtre de dialogue demandant la taille de la grille

def obtention() : # Validation de la taille initiale de la grille
    global box, largeur, hauteur, bouh # Autorisations
    l = champ.get() # Attribue à une variable l la valeur entrée pour la largeur
    h = entree.get() # Attribue à une variable h la valeur entrée pour la hauteur

# Efface les messages d'erreur précédemment générés
    try :
        bouh.destroy() 
    except (TclError, NameError) :
        42
    finally :

        try : # Va essayer d'exécuter le bloc indenté qui suit ; mais ne fera rien si ça génère une erreur
            h = int(h) # Convertit h en entier
            l = int(l) # Convertit l en entier
            box.destroy() # Détruit la mini-fenêtre
        except ValueError : # Affiche un message d'erreur
            bouh=Label(box, text="Erreur sur les valeurs insérées")
            bouh.pack()
        largeur = l # Validation de la largeur entrée
        hauteur = h # validation de la hauteur entrée


## Fenêtre initiale

box = Tk() # Mini-fenêtre
box.title("Entrez la taille de la grille")
framelarge = Frame(box, borderwidth = 0, relief = FLAT) # Une frame, pour mieux organiser l'espace
framelarge.pack(padx=5,pady=5)
Label(framelarge,text="Largeur :").grid(row=0,column=0,padx=5,pady=5) # Un titre, pour qu'on sache ce qu'on entre
champ = Entry(framelarge, bd=3) # Un champ d'entrée, pour la largeur de la grille
entree = Entry(framelarge, bd=3) # Un second champ d'entrée, pour la hauteur
ok = Button(box, text="Ok",command=obtention) # Bouton servant à valider
champ.grid(row=0,column=1,padx=5,pady=5)
Label(framelarge,text = "Hauteur :").grid(row=1,column=0,padx=5,pady=5) # Un autre titre
entree.grid(row=1,column=1,padx=5,pady=5)
ok.pack(padx=4,pady=4)
box.mainloop()


## Sous-programmes du programme principal

def clic(event) : # Inverse l'état de la case sur laquelle on clique

    # Récupération des coordonnées de la case sur laquelle on a cliqué
    x = (event.x - 3) // c
    y = (event.y - 3) // c
    
    dico[x,y] = 1 - dico[x,y] # Inversion de l'état de la case
    
    # Affichage du nouvel état de la case
    if dico[x,y] == 1 :
        canvas.create_rectangle(x*c+2, y*c +2, (x+1)*c+2, (y+1)*c +2, fill='#00ff2e',outline='#d0efef')
    else :
        canvas.create_rectangle(x*c+2, y*c +2, (x+1)*c+2, (y+1)*c +2, fill='light cyan',outline='#d0efef')

def etapeplus() : # Avance d'exactement une étape
    global auto # Autorisations
    auto = 1 # Auto vaut 1 lors du fonctionnement étape par étape
    etatplus()

def avance() :
    global auto, vitesse # Autorisations
    auto = 2 # Active l'avance automatique
    vitesse = 200 # 5 étapes par seconde
    etatplus()
        
def accelere() :
    global vitesse, auto # Autorisations
    auto = 2 # Active l'avance automatique
    vitesse = 1 # 20 étapes par seconde
    etatplus()

def stop() :
    global auto # Autorisations
    auto = 0 # Met en pause

def etatplus() : 
    calcul() # Effectue le 
    if auto > 0 :
        redessin()
    if auto > 1 :
        fenetre.after(vitesse,etatplus)

def calcul() :
    global dicoplus # Autorisations
    
    # Comptage du nombre de voisins
    
    # Pour les coins
    statut[0,0] = dico[0,1] + dico[1,1] + dico[1,0] # Coin supérieur gauche
    statut[0,hauteur-1] = dico[0,hauteur-2] + dico[1,hauteur-2] + dico[1,hauteur-1] # Coin inférieur gauche
    statut[largeur-1,hauteur-1] = dico[largeur-1,hauteur-2] + dico[largeur-2,hauteur-2] + dico[largeur-2,hauteur-1] # Coin inférieur droit
    statut[largeur-1,0] = dico[largeur-1,1] + dico[largeur-2,1] + dico[largeur-2,0] # Coin supérieur droit


    # Pour les colonnes de gauche et de droite
    for y in range (1, hauteur - 1) :
        statut[0,y] = dico[0, y-1] + dico[1, y-1] + dico[1, y] + dico[1, y+1] + dico[0, y+1] # Colonne la plus à gauche
        statut[largeur-1,y] = dico[largeur-1, y-1] + dico[largeur-2, y-1] + dico[largeur-2, y] + dico[largeur-2, y+1] + dico[largeur-1, y+1] # Colonne la plus à droite


    # Pour toutes les autres colonnes 
    for x in range (1, largeur - 1) :
        statut[x,0] = dico[x-1,0] + dico[x-1,1] + dico[x,1] + dico[x+1,1] + dico[x+1,0] # Ligne du haut
        for y in range (1, hauteur - 1) :
            statut[x,y] = dico[x-1,y] + dico[x-1,y+1] + dico[x,y+1] + dico[x+1,y+1] + dico[x+1,y] + dico[x+1,y-1] + dico[x,y-1] + dico[x-1,y-1] # Cases ne touchant aucun bord
        statut[x,hauteur-1] = dico[x+1,hauteur-1] + dico[x+1,hauteur-2] + dico[x,hauteur-2]  + dico[x-1,hauteur-2] + dico[x-1,hauteur-1] # Ligne du bas


    # Attribution du nombre de voisins 
    for y in range (hauteur) :
        for x in range (largeur) :
            if statut[x,y] in vie :
                dicoplus[x,y] = 1
            elif statut[x,y] in stable :
                dicoplus[x,y] = dico[x,y]
            elif statut[x,y] in change :
                dicoplus[x,y] = 1 - dico[x,y]
            else :
                dicoplus[x,y] = 0


def aleatoire() : # Grille aléatoire
    global dico, check # Autorisations
    check = 0
    for x in range(largeur) :
        for y in range (hauteur) :
            dico[x,y] = randint(0,1)
            check += dico[x,y]
    dessin() # Affichage du nouvel état


# Compte le nombre de cases en vie
    check = 0
    for x in range(largeur) :
        for y in range (hauteur) :
            check = dico[x,y] + check


def redessin() : # Vérifie que le programme n'est pas à l'arrêt avant d'afficher la nouvelle grille
    global dico, auto, check # Autorisations
    
# Vérifie si l'état est stable
    stable = 1
    if dico == dicoplus :
        stable = 1
    else :
        dico = dicoplus

# Compte le nombre de cases en vie
    check = 0
    for x in range(largeur) :
        for y in range (hauteur) :
            check = dico[x,y] + check

# Met en pause si un état stable (ou vide) a été atteint
    if check == 0 or stable == 0:
        auto = 0 
    dessin() # Affichage du nouvel état


def effacer() : # Génère une grille vide et la dessine
    global dico, check # Autorisations
    
# Tue toutes les cases
    for x in range(largeur) :
        for y in range (hauteur) :
            dico[x,y] = 0
    dessin() # Affichage du nouvel état


def dessin() : # Colore les cases vivantes et efface les cases mortes
    canvas.delete(ALL)
    grille()
    for x in range (largeur) :
        for y in range (hauteur) :
            if dico[x,y] == 1 :
                canvas.create_rectangle(x*c+2,y*c+2,(x+1)*c+2,(y+1)*c+2,fill='#00ff2e',outline='#d0efef') # Colore les cases vivantes


def resize() : # Redimensionne la grille
    global canvas, largeur, hauteur # Autorisations
    
# Efface le message d'erreur précédemment généré
    try :
        bouh.destroy() 
    except (TclError, NameError) :
        42
    finally : # Cette fonction est nécessaire pour que le reste marche s'il n'y avait pas de message d'erreur
    
# Enregistrement des valeurs entrées
        l = champ.get() 
        h = entree.get()
        
# Vérifie que les valeurs entrées sont entières
        try :
            h = int(h)
            l = int(l)
            canvas.destroy()
        except ValueError : # Message d'erreur
            bouh=Label(fenetre, text="Erreur sur les valeurs insérées")
            bouh.pack()
            

        largeur = l
        hauteur = h
        canvas = Canvas(frameA,width =largeur*c+1, height =hauteur*c+1, bg ='light cyan') # Créée la zone qu'occupera la grille, redimensionnée
        canvas.bind("<Button-1>", clic) # Fait en sorte que le programme réagisse quand on clique sur la grille
        canvas.pack(side =LEFT, padx =5, pady =5)
        grille() # Dessine la grille
        
        
def grille() : # Dessine la grille
    for i in range (2,largeur*c +3,c) :
        canvas.create_line(i,0,i,hauteur*c+3,fill ='#d0efef')
    for i in range (2,hauteur*c + 3,c) :
        canvas.create_line(0,i,largeur*c+3,i,fill ='#d0efef')
        
def nombreetape() :
    global auto # Autorisations
    n=etape.get()
    try :
        n = int(n)
    except ValueError :
        42
    auto = 1
    for i in range (1,n) :
        calcul()
    etatplus()


## Variables

c = 2 # Taille du côté d'une cellule
statut = {} # Nombre de voisines en vie
dico = {}
for x in range (largeur) :
    for y in range (hauteur) :
        dico[x,y] = 0 # Vaut 0 si la case est morte et 1 si la case est vivante
check = 0
dicoplus = {} # Dictionnaire de transition
auto = 1 # Le programme avance automatiquement si auto vaut 2 et n'avance pas si auto vaut 0
vitesse = 1000 # Délai entre deux étapes
vie = [3] # Liste des nombres de voisins pour lesquels une case est forcément en vie
stable = [2] # Liste des nombres de voisins pour lesquels une case ne change pas d'état
change = [] # Liste des nombres de voisins pour lesquels une case vivante meurt mais une case morte naît (il n'existe aucun cas dans les règles traditionnelles... mais c'est bon à avoir si jamais on pense à une fonctionnalité de changement de règles (ceci est un commentaire abusivement long pour un tableau vide))


## Programme principal
## Fenêtre graphique

fenetre = Tk() # Fenêtre
fenetre.title("Le jeu de la vie")
frameA = Frame(fenetre, bg = '#efefef', borderwidth = 0, relief =FLAT) # Partie supérieure de la fenêtre, contenant la grille et le menu de changement de taille
frameA.pack(side=TOP, padx = 5, pady=0)
canvas = Canvas(frameA,width =largeur*c+1, height =hauteur*c+1, bg ='light cyan') # Zone qu'occupera la grille
canvas.bind("<Button-1>", clic) # Fait en sorte que le programme réagisse quand on clique sur la grille
canvas.pack(side =LEFT, padx =5, pady =5)
grille() # Dessine la grille
frameC = Frame(frameA, borderwidth = 0, relief =FLAT) # Partie supérieure droite de la fenêtre, qui contiendra le menu de changement de taille
frameC.pack(side=RIGHT, padx = 5, pady=5)
framelarge = Frame(frameC, borderwidth = 0, relief = FLAT) # Une frame, pour mieux organiser l'espace
framelarge.pack(side=TOP,padx=5,pady=10)
Label(framelarge,text="Largeur :").grid(row=0,column=0,padx=5,pady=5) # Un titre, pour qu'on sache ce qu'on entre
champ = Entry(framelarge, bd=3) # Un champ d'entrée, pour la largeur de la grille
entree = Entry(framelarge, bd=3) # Un second champ d'entrée, pour la hauteur
champ.grid(row=0,column=1,padx=5,pady=5)
Label(framelarge,text = "Hauteur :").grid(row=1,column=0,padx=5,pady=5) # Un autre titre
entree.grid(row=1,column=1,padx=5,pady=5)
ok = Button(frameC, text="Changer la taille",command=resize)
ok.pack(side=TOP, padx=4,pady=4)
nombre = Button(frameC, text="Valider le nombre d'étapes", command =nombreetape)
etape=Entry(frameC, bd=3)
nombre.pack(side=BOTTOM) # RIP
etape.pack(side=BOTTOM)
tableau = Frame(frameC, borderwidth = 0, relief = FLAT)
tableau.pack(side=BOTTOM)
for i in range(9) :
    Label(tableau,text="%s"%(i)).grid(row=0,column=i)
    

## Boutons

# Les boutons sont répartis sur deux lignes : frameB (ligne du haut) et frameD (ligne du bas)
frameB = Frame(fenetre, borderwidth = 0, relief = FLAT) # La ligne du haut contiendra surtout les boutons concernant l'édition du contenu de la grille
frameB.pack(side=TOP, padx = 5, pady = 0)
frameD = Frame(fenetre, borderwidth = 0, relief = FLAT) # La ligne du bas conitiendra les boutons d'avance manuelle et automatique, d'arrêt, et d'autres trucs.
frameD.pack(side=TOP, padx = 5, pady = 0)

# Liste des boutons
ragequit = Button(frameD, text = "Ragequit", command=fenetre.destroy) # Pour quitter
random = Button(frameB, text = "Configuration aléatoire", command=aleatoire) # Génère et affiche un état aléatoire
next = Button(frameD, text="Étape suivante", command = etapeplus) # Passe à l'étape suivante
delete = Button(frameB, text = "Effacer", command=effacer) # Efface la grille
marche = Button(frameD, text = "Avance auto", command=avance) # Lance l'avance automatique
arret = Button(frameD, text = "Stop", command=stop) # Arrête l'avance automatique
vite = Button(frameD, text="Avance rapide", command =accelere) # Lance l'avance rapide
random.pack(side = LEFT, padx = 4, pady = 4)
delete.pack(side=RIGHT, padx= 4, pady =4)
next.pack(side=LEFT, padx = 4, pady = 4)
marche.pack(side = LEFT, padx=4, pady=4)
vite.pack(side= LEFT, padx=4, pady=4)
arret.pack(side = LEFT, padx=4, pady = 4)
ragequit.pack(side = RIGHT, padx= 4, pady = 4)
fenetre.mainloop()
