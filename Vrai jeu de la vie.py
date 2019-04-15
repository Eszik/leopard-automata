#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# (Ne faites pas attention à ces deux premières lignes ; la première sert à être lisible sous Unix, et la seconde à être reconnu comme du codage UTF-8, ce qui peut être indispensable dans certaines situations)


## Jeu de la vie


# Un projet de Flora Gaudillière, Maud Biquard et Vincent Blavy


## Modules utilisés


from tkinter import *
from random import *
from pickle import *
import os


## Variables


# Variables globales
# Grandeurs physiques
c = 2 # Taille (en pixels) du côté d'une cellule
largeur = 400 # Largeur de la grille (en nombre de cellules)
hauteur = 400 # Hauteur de la grille (en nombre de cellules)
check = 0 # Nombre total de cellules en vie.
epaisseur = 1 # Épaisseur de la bordure des cellules. Le principal intérêt de la poser en tant que variable est de pouvoir la passer à 0 si jamais on réduit sensiblement la taille des cases
vitesse = 1 # Délai entre deux étapes de l'avance automatique

# Variables globales d'état
# Ces variables globales informent de l'activation ou non d'un mode de fonctionnement donné du programme
auto = 0 # Variable qui indique si le programme est en avance automatique (auto = 2), en mode étape par étape (auto = 1) ou en pause (auto = 0)
nyan = 0 # Variable qui indique si l'affichage arc-en-ciel est activé (nyan = 1) ou désactivé (nyan = 0)
simulation = 0 # Variable qui indique si le programme doit prendre en compte le modèle "simple" du jeu de la vie (simulation = 0), ou bien la modélisation avancée (simulation = 1)
fraction = 0 # Variable qui indique si la fenêtre est en affichage uni (fraction = 0) ou fractionné (fraction = 1)

# Dictionnaires
# Les dictionnaires contiennent des informations sur les cases (avec pour arguments les coordonnées dans la grille)
dico = {"hauteur":hauteur,"largeur":largeur,"check":check} # C'est la variable la plus importante du programme : elle contient de multiples informations, à savoir : les dimensions de la grille, l'état de chacune des cellules, le nombre de cellules en vie. 
statut = {} # Ce dictionnaire contient, pour chaque cellule, le nombre de voisines vivantes. Il est utilisé comme variable locale des sous-programmes de calcul d'état suivant
dicoplus = {} # Contiendra l'état postérieur calculé avant sa validation. Concrètement, ce ne sera jamais une variable globale, mais toute variable locale d'un sous-programme correspondant à un dictionnaire de transition sera nommé ainsi.
couleur = {} # Ceci est un petit bonus. Pour plus de joie. Il contient la couleur dans laquelle afficher chaque case.

# Règles du jeu
vie = 3*[False] + [True] + 5*[False] # Liste des nombres de voisins pour lesquels une case est forcément en vie
stable = 2*[False] + [True] + 6*[False] # Liste des nombres de voisins pour lesquels une case ne change pas d'état
change = 9*[False] # Liste des nombres de voisins pour lesquels une case vivante meurt mais une case morte naît (il n'existe aucun cas dans les règles traditionnelles du jeu de la vie, et cela correspond fort peu à la théorie des simulations cellulaires. Mais il fallait le faire exister pour des raisons d'exhaustivité)

# Paramètres avancés
# Ces paramètres de calcul correspondent à une approche des simulations cellulaires plus proche des phénomènes observables dans la réalité. 
seuil = 0
rayaction = 5
coaffaction = 1
rayinhib = 10
coeffinhib = 0.1


## Sous-programmes


## Sous-programmes d'avance automatique
# Rappel : la variable auto vaut 2 en avance automatique, 1 en avance étape par étape et 0 en pause
# Certains sous programmes (avance/avancer ou accelere/accelerer) sont en deux parties car ler éxécution nécessite un temps d'attente après une partie des instructions


# Le programme "avance" lance le programme en avance automatique à une vitesse de 5 étapes par seconde
def avance() :
    global auto # Autorisations
    stop() # Met en pause l'avance automatique afin d'éviter un cumul des demandes de calcul
    fenetre.after(vitesse+10,avancer) # Lance la seconde partie du programme une fois que toutes les requêtes sont arrêtées
def avancer() :
    global auto, vitesse
    auto = 2 # Active l'avance automatique
    vitesse = 200 # 5 étapes par seconde
    etatplus() # Boucle de calcul


# Le programme "accelere" lance le programme en avance automatique à une vitesse de 20 étapes par seconde
def accelere() :
    global auto # Autorisations
    stop() # Met en pause l'avance automatique afin d'éviter un cumul des demandes de calcul
    fenetre.after(vitesse+10,accelerer) # Lance la seconde partie du programme une fois que toutes les requêtes sont arrêtées
def accelerer() :
    global auto, vitesse
    auto = 2 # Active l'avance automatique
    vitesse = 50 # 20 étapes par seconde
    etatplus() # Boucle de calcul


# Le programme "accelereplus" lance le programme en avance automatique à une vitesse absolument démente. C'est un easter egg, activable en appuyant sur la touche "="
def accelereplus(event) :
    global auto # Autorisations
    stop() # Met en pause l'avance automatique afin d'éviter un cumul des demandes de calcul
    fenetre.after(vitesse+10,accelererplus) # Lance la seconde partie du programme une fois que toutes les requêtes sont arrêtées
def accelererplus() :
    global auto, vitesse
    auto = 2 # Active l'avance automatique
    vitesse = 1 # Règle la vitesse sur le plus vite possible (a priori, 1000 étapes par seconde)
    etatplus() # Boucle de calcul


# Le programme "step" fait avancer le programme d'exactement une étape
def step() :
    global auto # Autorisations
    auto = 1 # Active l'avance étape par étape
    etatplus() # Boucle de calcul
    auto = 0 # Remet en pause une fois l'avance terminée


# Le programme "stop" arrête l'avance du programme
def stop() :
    global auto # Autorisations
    auto = 0 # Met en pause


# Le programme "etatplus" est crucial : c'est ce programme qui lance et met fin la boucle de calcul. C'est le carrefour de l'information, le centre névralgique du programme.
def etatplus() :
    dicoplus = calcul(dico) # Effectue le calcul de l'état suivant
    
    if auto > 0 : # Vérifie que le programme n'est pas censé être en pause
        valide(dicoplus)
    
    if auto > 1 : # Vérifie que le programme est censé avancer automatiquement
        fenetre.after(vitesse, etatplus) # Lance un nouveau calcul d'état si l'avance automatique est activée


# L'intérêt du programme "valide" est double ; d'un côté, il valide les étapes futures calculées, et d'un autre, il évite que le programme "etatplus" ne se renvoie que dans lui-même, ce qui créerait une saturation de la récursivité
def valide(dicoplus) :
    global dico, auto, check # Autorisations
    
    dico = dicoplus # Si le programme n'est pas censé être en pause, alors l'avance d'une étape est validée : l'étape précédente (dico) est effacée et remplacé par le nouvel état (dicoplus)
    check = dico["check"] # On sort du dictionnaire le nombre de cases en vie
    if check == 0 : # Vérifie si un état vide a été atteint
        auto = 0 # Si la grille est vide, alors le programme est mis en pause pour éviter un gaspillage de la puissance de calcul
    dessin() # Affichage du nouvel état


## Sous-programmes de calcul


# Le programme "calcul" donne, à partir d'un dictionnaire d'état, le dictionnaire correspondant à l'étape suivante
def calcul(dico) :
    dicoplus = {"hauteur":dico["hauteur"],"largeur":dico["largeur"],"check":dico["check"]} # Création du dictionnaire de transition
    statut = {}
    hauteur = dico["hauteur"] # Pour plus de commodité, on fait en sorte de ne pas avoir à aller chercher dans un dictionnaire les dimensions de la grille à chaque utilisation
    largeur = dico["largeur"]
    for x in range(largeur) : # Cette boucle tue toutes les cases
        for y in range (hauteur) :
            statut[x, y] = 0
    
    if simulation == 0 : 
    ## Calcul synchrone en jeu de la vie standard
        
    # Première partie : comptage du nombre de voisins vivants. Dans cette partie, chaque cellule vivante va envoyer à tous ses voisins l'information comme quoi elle est vivante
        
        # Pour les coins
        if dico[0,0] == 1 : # Coin supérieur gauche
            statut[0,1] += 1
            statut[1,1] += 1
            statut[1,0] += 1
        
        if dico[0, hauteur-1] ==1 : # Coin inférieur gauche
            statut[0, hauteur-2] += 1 
            statut[1, hauteur-2] += 1
            statut[1, hauteur-1] += 1
        
        if dico[largeur-1, hauteur-1] == 1 : # Coin inférieur droit
            statut[largeur-1, hauteur-2] +=1 
            statut[largeur-2, hauteur-2] +=1 
            statut[largeur-2, hauteur-1] += 1
        
        if dico[largeur-1, 0] == 1 : # Coin supérieur droit
            statut[largeur-1, 1] += 1
            statut[largeur-2, 1] += 1 
            statut[largeur-2, 0] += 1
        
        # Pour les colonnes de gauche et de droite
        for y in range (1, hauteur - 1) :
            if dico[0, y] == 1 : # Colonne la plus à gauche
                statut[0, y-1] += 1
                statut[1, y-1] += 1 
                statut[1, y] +=1 
                statut[1, y+1] +=1 
                statut[0, y+1] +=1 
            
            if dico[largeur-1, y] == 1 : # Colonne la plus à droite
                statut[largeur-1, y-1] += 1
                statut[largeur-2, y-1] += 1
                statut[largeur-2, y] += 1
                statut[largeur-2, y+1] += 1 
                statut[largeur-1, y+1] += 1 
        
        # Pour toutes les autres colonnes
        for x in range (1, largeur - 1) :
            if dico[x, 0] ==1 : # Ligne du haut
                statut[x-1, 0] += 1
                statut[x-1, 1] += 1
                statut[x, 1] += 1
                statut[x+1, 1] += 1
                statut[x+1, 0] += 1 
            
            for y in range (1, hauteur - 1) : # Cases ne touchant aucun bord
                if dico[x, y] == 1 :
                    statut[x-1, y] += 1
                    statut[x-1, y+1] += 1
                    statut[x, y+1] += 1
                    statut[x+1, y+1] += 1
                    statut[x+1, y] += 1
                    statut[x+1, y-1] += 1
                    statut[x, y-1] += 1
                    statut[x-1, y-1] += 1 
            
            if dico[x, hauteur-1] == 1 : # Ligne du bas
                statut[x+1, hauteur-1] += 1
                statut[x+1, hauteur-2] += 1
                statut[x, hauteur-2] += 1
                statut[x-1, hauteur-2] += 1
                statut[x-1, hauteur-1] += 1 
        
        # Attribution du nombre de voisins (et comptage, au passage, du nombre de cases en vie)
        check = 0 # On remet à 0 le nombre de cellules en vie
        for y in range (hauteur) :
            for x in range (largeur) :
                if vie[statut[x, y]] : # Si le nombre de voisins fait systématiquement vivre une cellule
                    dicoplus[x, y] = 1 # Alors cette cellule est vivante
                    check += 1 # Et donc, on la compte en tant que cellule vivante
                elif stable[statut[x, y]] : # Si le nombre de voisins laisse la cellule inchangée
                    dicoplus[x, y] = dico[x, y] # Alors... son état reste inchangé
                    check += dico[x, y] # Et on actualise le comptage de cellules vivantes
                elif change[statut[x, y]] : # Si le nombre de voisins est tel que l'état de la cellule changera forcément
                    dicoplus[x, y] = 1 - dico[x, y] # Alors cet état change
                    check += dicoplus[x, y] # Et on actualise le comptage de cellules vivantes
                else : # Et si la cellule est morte
                    dicoplus[x, y] = 0 # Alors elle meurt
        dicoplus["check"] = check # On enregistre dans le dictionnaire le nombre de cellules vivantes ainsi compté
        return dicoplus # Et on renvoie au reste du programme le nouvel état calculé
        
    ## Calcul synchrone en modélisation avancée (actuellement vide)
    else : # Simulation avancée
        pass # Actuellement vide


# Le calcul asynchrone est un mode de calcul où le passage d'un état à un autre ne se fait plus génération par génération, mais cellule par cellule. Une cellule change à la fois. Si on demande au programme de calculer le nouvel état de deux cellules, le nouvel état de la première sera pris en compte pour le calcul du nouvel état de la seconde.
# En réalité, ce programme est un programme de calcul semi-asynchrone : il exécutera un calcul asynchrone pour toutes les cellules de la grille, une fois, dans un ordre aléatoire. Ce mode de calcul est optimal dans le cadre de la simulation avancée.
def asynchrone(dico) :
    ## Actuellement vide
    pass # Actuellement vide


## Sous-programmes d’action de l'utilisateur


# Le sous-programme "clic" inverse l'état d'une cellule sur laquelle l'utilisateur clique
def clic(event) :
    global info, check, dico
    
    # Récupération des coordonnées de la case sur laquelle on a cliqué
    x = (event.x - 3) // c
    y = (event.y - 3) // c
    
    dico[x, y] = 1 - dico[x, y] # Inversion de l'état de la case sur laquelle l'utilisateur a cliqué
    check = check - 1 + 2*dico[x, y] # Actualisation du nombre de cellules vivantes
    
    # Affichage du nouvel état de la case
    if dico[x, y] == 1 : # Si l'on vient de faire naître une cellule
        canvas.create_rectangle(x*c+2, y*c +2, (x+1)*c+2, (y+1)*c +2, fill = '#%s'%(couleur[x,y]), outline = '#d0efef', width = epaisseur) # Colore la case en vie
    else : # Si l'on vient de tuer une cellule
        canvas.create_rectangle(x*c+2, y*c +2, (x+1)*c+2, (y+1)*c +2, fill = '#e0ffff', outline = '#d0efef', width = epaisseur) # Décolore la case morte
    
    # Réécrit le nombre de cellules vivantes. La boucle try sert à faire en sorte que le programme puisse ne pas planter s'il n'y avait pas précédemment de nombre de cellules affiché
    try :
        info.destroy() # Efface le précédent nombre de cellules vivantes
    except (TclError, NameError) :
        pass
    info = Label(frame1, text = "%s cellules vivantes" % (check)) # Indique le nouveau nombre de cellules en vie
    info.pack(side = BOTTOM)


# Le programme "sautetape" fait avancer d'un coup le programme d'un nombre donné d'étapes, saisi au clavier par l'utilisateur. Seule la dernière étape sera affichée.
def sautetape(event) :
    global auto, bouh # Autorisations
        
    auto = 1 # Ce programme relève de l'avance étape par étape
    saut = etape.get() # Attribue à une variable saut la valeur demandée par l'utilisateur
    dicoplus = dico # On pose un dictionnaire de transition, pour ne pas altérer le dictionnaire d'origine au cas où un ordre de pause viendrait annuler le saut d'étapes
    clearerror() # Efface les messages d'erreur précédemment générés
    
    # Effectue le saut d'étape. La boucle try sert à faire en sorte que le programme puisse ne pas planter si cette tâche ne peut être accomplie
    try :
        saut = int(saut) # Convertit la valeur entrée par l'utilisateur en entier
        for i in range (saut) :
            dicoplus = calcul(dicoplus) # Boucle de calcul, répétée jusqu'à l'avant-dernière étape
        valide(dicoplus) # Calcule et affiche la dernière étape
        auto = 0 # Remet en pause une fois l'avance terminée
    except ValueError : # Affiche un message d'erreur si un problème survient
        bouh = Label(fenetre, text = "Ce n'est pas comme ça que ça marche ; il faut entrer un nombre. Entier. Positif.")
        bouh.pack()


## Sous-programmes d'édition de la fenêtre


# Le programme "resize" modifie les dimensions de la grille pour de nouvelles valeurs, saisies au clavier par l'utilisateur.
def resize() :
    global canvas, largeur, hauteur, dico, bouh # Autorisations
    
    clearerror() # Efface les messages d'erreur précédemment générés

    # Enregistrement des valeurs entrées
    l = champ.get() 
    h = entree.get()
    
    # Redimensionnement de la grille. La boucle try sert à faire en sorte que le programme puisse ne pas planter si cette tâche ne peut être accomplie
    try :
        h = int(h) # Conversion des valeurs saisies par l'utilisateur en entiers
        l = int(l)
        
        # Extension, si nécessaire, de l'aire enregistrée dans le dictionnaire principal : on crée des cellules mortes pour combler l'espace vide.
        if l > largeur : # Extension sur le bord gauche
            for x in range (largeur,l) :
                for y in range (hauteur) :
                    dico[x,y] = 0
            
            if h > hauteur : # Extension dans le coin inférieur droit
                for x in range (largeur,l) :
                    for y in range (hauteur, h) :
                        dico[x,y] = 0
        
        if h > hauteur : # Extension sur le bord du bas
            for x in range (largeur) :
                for y in range (hauteur,h) :
                    dico[x,y] = 0
        # Note : si on réduit la taille de la grille, les cellules en-dehors de la nouvelle grille ne seront pas effacées, mais ne seront pas prises en compte lors des calculs.
        
        largeur = l # Enregistrement des nouvelles dimensions
        hauteur = h
        dico["largeur"] = l # Enregistrement dans le dictionnaire principal des nouvelles dimensions
        dico["hauteur"] = h
        rainbow2() # Actualisation du tableau de couleur des cellules
        
        # Création de la nouvelle grille
        canvas.destroy() # Si les valeurs entrés sont correctes, alors l'ancienne grille est détruite pour faire place à la nouvelle
        creer_canvas()
        dessin()
    except ValueError : # Message d'erreur
        bouh = Label(fenetre, text = "Vous avez triché, veuillez changer les valeurs")
        bouh.pack()


# Le programme "reroll" permet de modifier la taille des cellules
def reroll(cell) :
    global c, canvas, epaisseur
    
    c = int(cell) # Modifie la varaible associée à la taille des cellules
    
    if c <= 2 :
        epaisseur = 0
    else :
        epaisseur = 1
    
    # Création de la nouvelle grille
    canvas.destroy() # Si les valeurs entrés sont correctes, alors l'ancienne grille est détruite pour faire place à la nouvelle
    creer_canvas()
    dessin()


def fractionne() :
    global fraction, tox, frame1, frame2, frame3
    
    fraction = 1 - fraction
    
    frame1.destroy()
    frame2.destroy()
    frame3.destroy()
    if fraction == 1 :
        tox = Toplevel(fenetre)
        tox.title("Interface de l'utilisateur")
    else :
        tox.destroy()
    frames()
    creer_canvas()
    resizer()
    bond()
    boutons()
    dessin()


## Sous-programmes de changement des règles


# Le programme "draft" active et désactive la simulation avancée
def draft() :
    global simulation # Autorisations
    
    pass

# Le programme "nait" intègre à la simulation 
def nait(a) :
    global vie, change, stable
    
    if vie[a] :
        vie[a] = False
        stable[a] = True
    elif stable[a] :
        stable[a] = False
        vie[a] = True
    elif change[a] :
        change[a] = False
    else :
        change[a] = True


def vit(a) :
    global vie, change, stable
    
    if change[a] :
        change[a] = False
        vie[a] = True
    elif vie[a] :
        vie[a] = False
        change[a] = True
    elif stable[a] :
        stable[a] = False
    else :
        stable[a] = True


## Sous-programmes de prise en main
# Ces programmes ne servent à rien, mis à part à rendre le programme plus agréable à utiliser


# Les programmes "jump" et "skip" permettent de passer d'un des deux champs d'entrée où l'utilisateur entre les nouvelles dimensions à l'autre lorsque l'utilisateur appuie sur la touche entrée, ou bien de lancer les deux redimensionnements si les deux champs sont remplis
def skip(event) :
    l = champ.get() # Récupère les valeurs des deux champs d'entrée
    h = entree.get()
    if l == '' :
        pass # Ne fait rien si le champ d'entrée sélectionné est vide
    elif h == '' :
        entree.focus_set() # Change la sélection vers l'autre champ d'entrée si celui sélectionné est rempli et l'autre vide
    else :
        resize() # Lance le redimensionnement si les deux champs sont remplis
def jump(event) :
    l = champ.get() # Récupère les valeurs des deux champs d'entrée
    h = entree.get()
    if h == '' :
        pass # Ne fait rien si le champ d'entrée sélectionné est vide
    elif l == '' :
        champ.focus_set() # Change la sélection vers l'autre champ d'entrée si celui sélectionné est rempli et l'autre vide
    else :
        resize() # Lance le redimensionnement si les deux champs sont remplis


# Le programme "clearerror" efface les messages d'erreur précédemment générés. C'est inutile, mais pratique
def clearerror() :
    # Efface les messages d'erreur précédemment générés. La boucle try sert à faire en sorte que le programme puisse ne pas planter si cette tâche ne peut être accomplie
    try :
        bouh.destroy()
    except (TclError, NameError) : # Si il n'y a pas de message d'erreur à effacer cette commande demandera au programme de ne pas le considérer comme une situation anormale
        pass


## Sous-progammes de couleur
# Ce programme est tout vert et bleu... mais en appuyant sur la touche "*", un easter egg se déclenche ; c'est l'arc-en-ciel !


# Le programme "easter" déclenche et désenclenche le mode arc-en-ciel
def easter(event) :
    global nyan # Autorisations
    
    nyan = 1 - nyan # Fait savoir au reste du programme que la couleur va s'enclencher / se désenclencher
    colorier() # Affiche la couleur
    dessin() # Affiche le nouvel état
    


# Le programme "colorier" remplace le vert uniforme par un arc-en-ciel quand la couleur est activée, et le réinstalle quand la couleur est déactivée
def colorier() :
    global couleur # Autorisations
    
    if nyan == 0 : # Si la couleur est désactivée
        for x in range (largeur) :
            for y in range (hauteur) :
                couleur[x,y] = "00ff2e" # On met du vert uniforme
        
    else : # Si la couleur est activée
        for x in range (largeur) :
            for y in range (hauteur) :
                couleur[x,y] = rouge + bleu[x] + vert[y] # La couleur de chaque case sera différente


# Le sous-programme "rainbow 1" fixe un taux aléatoire de rouge qui sera le même pour toutes les cases de la grille. Il est activé en cas de remplissage aléatoire de la grille
def rainbow1() :
    global rouge # Autorisations
    
    rouge = str(hex(randint(0,255))) # On génère aléatoirement un entier en hexadécimal compris entre 0 et FF
    if len(rouge) <= 3 : # Si ce n'est qu'un nombre à un chiffre (ou lettre) en hexa, alors on rajoute un 0 devant, pour la lisibilité par le programme
        rouge = "0" + rouge[2]
    else : # Et sinon... bah on n'a pas besoin d'ajouter un 0, mais on corrige quand même, car le format du nombre généré n'est pas lisible tel quel.
        rouge = str(rouge[2] + rouge[3])


# Le programme "rainbow", deuxième du nom, attribue une valeur de vert et de bleu à chaque case, en dégradé (de plus en plus bleu en allant vers la droite, et de plus en plus vert en allant vers le bas)
def rainbow2() :
    global bleu, vert # Autorisations
    
    vert = [] # On a des listes. Le vert sera fixé par ligne, et le bleu par colonne
    bleu = []
    
    for x in range (largeur) :
        blue = str(hex((x*256)//largeur)) # On génère et rend lisible un nombre en hexadéimal selon le même procédé que dans le programme "rainbow 1"
        if len(blue) <= 3 :
            bleu.append("0" + blue[2])
        else :
            bleu.append(str(blue[2] + blue[3]))
    
    for y in range (hauteur) : # On génère et rend lisible un nombre en hexadéimal selon le même procédé que dans le programme "rainbow 1"
        green = str(hex((256*y)//largeur))
        if len(green) <= 3 :
            vert.append("0" + green[2])
        else :
            vert.append(str(green[2] + green[3]))
    
    colorier() # Actualisation de la couleur de la grille


## Sous-programmes de sauvegarde


def top(a) :
    global box, field, bouh
    
    box = Toplevel(fenetre) # Crée une surfenêtre qui demande le nom du fichier à sauvegarder ou charger
    clearerror() # Efface les messages d'erreur précédemment générés
    
    ## Cas de la sauvegarde
    if a == 1 : # Quand on veut sauvegarder un fichier
        box.title("Sauvegarder un fichier") # Donne un titre à la surfenêtre
        demande = Label(box, text = "Entrez le nom du fichier à sauvegarder :") # Crée un petit texte explicatif indiquant à l'utilisateur qu'il doit donner un petit nom au fichier  sauvegarder
        if auto == 0 : # J'ai fait en sorte qu'on ne puisse sauvegarder que pendant la pause, parce que je n'ose pas imaginer les bugs que ça ferait si la configuration changeait pendant qu'on la sauvegarde
            pass
        else : # Affiche un message d'erreur si le programme n'est pas en pause
            bouh = Label(fenetre, text = "Veuillez mettre en pause pour sauvegarder.")
            bouh.pack()
        
    ## Cas du chargement
    else : # Quand on veut charger un fichier
        box.title("Charger un fichier") # Donne un titre à la surfenêtre
        demande = Label(box,text = "Entrez le nom du fichier à charger :") # Crée un petit texte explicatif indiquant à l'utilisateur qu'il doit entrer le nom du fichier à charger
    
    field = Entry(box, bd = 3) # Crée un petit champ d'entré où l'utilisateur indiquera le nom du fichier
    if a == 1 :
        fin = Button(box, text = "Ok", command = sauvegarde) # Petit bouton pour valider le nom de fichier
    else :
        fin = Button(box, text = "Ok", command = charger) # Petit bouton pour valider le nom de fichier
    
    demande.pack()
    field.pack()
    fin.pack()


# Le programme "nommer" transforme le nom de fichier entré par l'utilisateur en un chemin d'accès menant au dossier où est enregistré le fichier .py en train de tourner.
def nommer() :
    global box
    nom = field.get()
    ## À améliorer : récupération de chemin d'accès
    chemin = "W:\ " # Ceci est à améliorer
    chemin = chemin[0] + chemin[1] + chemin[2] # Ceci est à améliorer
    nom = chemin + nom + ".txt"
    box.destroy()
    return nom


# Le programme "sauvegarde" permet de sauvegarder une configuration, afin de la réinvestir plus tard.
def sauvegarde() :
    nom = nommer() # Transforme le nom de fichier entré par l'utilisateur en un chemin d'accès
    dico["check"] = check # Sauvegarde le nombre de cellules en vie
    fichier = open('%s'%(nom),'wb') # Crée un fichier du nom entré
    dump(dico,fichier) # Le module pickle enregistre le dictionnaire principal, en l'encodant, dans le fichier
    fichier.close() # Referme le fichier


# Le programme "charger" permet de récupérer une configuration préalablement enregistrée
def charger() :
    global dico, largeur, hauteur, canvas, bouh # Autorisations
    
    nom = nommer() # Transforme le nom de fichier entré par l'utilisateur en un chemin d'accès
    
    try : # Récupère le fichier. La boucle try est là pour que le programme ne plante pas s'il y a une erreur, ou si le fichier n'existe juste pas.
        fichier = open('%s'%(nom),'rb') # Ouvre le fichier et le lit
        dico = load(fichier) # désérialisation, décodage du fichier grâce au module pickle
        fichier.close() # Referme le fichier
    except FileNotFoundError : # Génère un message d'erreur, si le fichier demandé n'est pas trouvé
        bouh = Label(fenetre, text = "Fichier non trouvé")
        bouh.pack()       
    
    largeur = dico["largeur"] # Lecture des nouvelles dimensions de la grille
    hauteur = dico["hauteur"]
    rainbow2() # Actualisation du tableau de couleur des cellules
    
    # Création de la nouvelle grille
    canvas.destroy() # Si les valeurs entrés sont correctes, alors l'ancienne grille est détruite pour faire place à la nouvelle
    creer_canvas()
    dessin()

## Sous-programmes de dessin


# Le programme "grille"... euh... dessine la grille
def grille() :
    for i in range (2, largeur*c +3, c) :
        canvas.create_line(i, 0, i, hauteur*c+3, fill = '#d0efef')
    for i in range (2, hauteur*c + 3, c) :
        canvas.create_line(0, i, largeur*c+3, i, fill = '#d0efef')


# Le programme "aléatoire" remplit la grille de façon aléatoire. C'est là qu'on ressent que l'évolution au niveau de l'évidence des noms entre les plus anciens sous-programmes et les plus récents.
def aleatoire() :
    global dico, check # Autorisations
    
    check = 0 # Met à 0 le compte des cellules vivantes
    for x in range(largeur) :
        for y in range (hauteur) :
            dico[x, y] = randint(0, 1) # Génère pour chaque cellule un état aléatoire
            check += dico[x, y] # Tient à jour le compte des cellules vivantes
    dessin() # Affichage du nouvel état


# Le programme "effacer" génère une grille vide et la dessine
def effacer() : 
    global dico, check # Autorisations
    
    check = 0 # On sait d'avance qu'on n'aura plus aucune cellule vivante
    for x in range(largeur) : # Cette boucle tue toutes les cases
        for y in range (hauteur) :
            dico[x, y] = 0
    dessin() # Affichage du nouvel état


# Le programme "dessin" efface l'intégralité de la grille, avant de dessiner les cellules vivantes
def dessin() :
    global info # Autorisations
    
    canvas.delete(ALL) # Efface tout
    grille() # Redessine la grille
    for x in range (largeur) : # Cette boucle colore les cases vivantes
        for y in range (hauteur) :
            if dico[x, y] == 1 :
                canvas.create_rectangle(x*c+2, y*c+2, (x+1)*c+2, (y+1)*c+2, fill = '#%s'%(couleur[x,y]), outline = '#d0efef', width = epaisseur) 
    
    # Réécrit le nombre de cellules vivantes. La boucle try sert à faire en sorte que le programme puisse ne pas planter s'il n'y avait pas précédemment de nombre de cellules affiché
    try :
        info.destroy() # Efface le précédent nombre de cellules vivantes
    except (TclError, NameError) :
        pass
    info = Label(frame1, text = "%s cellules vivantes" % (check)) # Indique le nouveau nombre de cellules en vie
    info.pack(side = BOTTOM)



## Fenêtre graphique


fenetre = Tk() # Fenêtre
fenetre.title("Le jeu de la vie") # Donne un titre à la fenêtre


## Des frames, pour organiser l'espace

# Frames correspondant à des parties de la fenêtre principale
def frames() :
    global frame1, frame2, frame3, frameC, framesize, nombre, tableau
    frame1 = Frame(fenetre, bg = '#efefef', borderwidth = 0, relief = FLAT) # Partie supérieure de la fenêtre, contenant la grille et l'interface utilisateur
    if fraction == 0 :
        frame2 = Frame(fenetre, bg = '#efefef', borderwidth = 0, relief = FLAT) # La ligne du haut conitiendra les boutons d'avance manuelle et automatique, d'arrêt, et d'autres trucs.
        frame3 = Frame(fenetre, bg = '#efefef', borderwidth = 0, relief = FLAT) # La ligne du bas contiendra surtout les boutons concernant l'édition du contenu de la grille
        frameC = Frame(frame1, bg = '#efefef', borderwidth = 0, relief = FLAT) # Partie supérieure droite de la fenêtre, qui contiendra l'interface utilisateur
    
    else :
        frame2 = Frame(tox, bg = '#efefef', borderwidth = 0, relief = FLAT) # La ligne du haut conitiendra les boutons d'avance manuelle et automatique, d'arrêt, et d'autres trucs.
        frame3 = Frame(tox, bg = '#efefef', borderwidth = 0, relief = FLAT) # La ligne du bas contiendra surtout les boutons concernant l'édition du contenu de la grille
        frameC = Frame(tox, bg = '#efefef', borderwidth = 0, relief = FLAT) # Partie supérieure droite de la fenêtre, qui contiendra l'interface utilisateur
        
    frame1.pack(side = TOP, padx = 5, pady = 0)
    frame3.pack(side = BOTTOM, padx = 5, pady = 0)
    frame2.pack(side = BOTTOM, padx = 5, pady = 0)
    
    # Frames correspondant à des sous-parties d'autres frames
    framesize = Frame(frameC, bg = '#efefef', borderwidth = 0, relief = FLAT) # Frame contenant le menu de redimensionnement de la grille
    nombre = LabelFrame(frameC, text = "Sauter un nombre d'étapes :", bg = '#efefef', borderwidth = 0, relief = FLAT) # Ce widget fut un label, un bouton, une frame, un champ d'entrée... et il survit, encore et toujours
    
    frameC.pack(side = RIGHT, padx = 5, pady = 0, expand = 1, fill = X)

frames()




## L'interface

# Initialisation de la grille
def creer_canvas() :
    global canvas
    
    canvas = Canvas(frame1, width = largeur*c+1, height = hauteur*c+1, bg = '#e0ffff') # Zone qu'occupera la grille
    canvas.bind("<Button-1>", clic) # Fait en sorte que le programme réagisse quand on clique sur la grille
    fenetre.bind("<Key-*>", easter)
    fenetre.bind("<Key-=>", accelereplus)
    
    canvas.pack(side = TOP, padx = 5, pady = 5)
    grille() # Initialise la grille

creer_canvas()
effacer() # Remplit la grille de cases mortes pour initialiser
rainbow1()
rainbow2()


# L'interface utilisateur à proprement parler, contenu dans la frame "frameC" (Décrit de haut en bas)

# Le menu de redimensionnement de la grille
def resizer() :
    global champ, entree # Autorisations
    
    framesize.pack(side = TOP, padx = 5, pady = 5) # La frame qui contiendra le tout (sauf le bouton)
    
    Label(framesize, text = "Largeur :").grid(row = 0, column = 0, padx = 5, pady = 5) # Un titre, pour qu'on sache ce qu'on entre
    Label(framesize, text = "Hauteur :").grid(row = 1, column = 0, padx = 5, pady = 5) # Un autre titre
    champ = Entry(framesize, bd = 3) # Un champ d'entrée, pour la largeur de la grille
    entree = Entry(framesize, bd = 3) # Un second champ d'entrée, pour la hauteur
    champ.bind("<Return>", func=skip) # Fait en sorte que le champ d'entrée réagisse quand on appuie sur le bouton entrée
    entree.bind("<Return>", func=jump)
    
    champ.grid(row = 0, column = 1, padx = 5, pady = 5)
    entree.grid(row = 1, column = 1, padx = 5, pady = 5)

resizer()

# Le menu de saut d'étapes
def bond() :
    global etape
    
    nombre.pack(side = TOP, padx = 5, pady = 5) # RIP
    
    etape = Entry(nombre, bd = 3) # Un champ d'entrée, pour le nombre d'étapes à calculer sans afficher
    etape.bind("<Return>",func=sautetape)
    
    etape.pack(side = TOP, padx = 5, pady = 5)

bond()


def changement(a) :
    global cell, slide, cox
    if a == 1 :
        try :
            ## Changer la taille des cellules
            cell = IntVar()
            slide = Scale(cox, from_ = 1, to = 20, variable = cell, command = reroll, label = "Taille des cellules", orient = 'horizontal')
            slide.pack(side = TOP, padx = 4, pady = 4)
            slide.set(10)
        except (NameError, TclError) :
            cox = Toplevel(fenetre)
            changement(1)
        
    elif a == 2 :
        try :
            ## Le tableau de changement de règles
            tableau = LabelFrame(cox, text = "Changer les règles :", bg = '#efefef', borderwidth = 0, relief = FLAT) # Frame contenant le tableau de changement de règles
            tableau.pack(side = TOP, padx = 10, pady = 10) # La frame qui contiendra le tout
            
            Label(tableau, text = "Cellule morte naît").grid(row = 1, column = 0)
            Label(tableau, text = "Cellule vivante vit").grid(row = 2, column = 0)
            
            for i in range(9) : # Cette boucle crée le contenu du tableau
                Label(tableau, text = "%s"%(i)).grid(row = 0, column = i+1)
                active = Checkbutton(tableau, command = lambda a=i: nait(a))
                active.grid(row = 1, column = i+1)
                if i == 3 :
                    active.select()
                meh = Checkbutton(tableau, command = lambda a=i: vit(a))
                meh.grid(row = 2, column = i+1)
                if i == 3 or i == 2 :
                    meh.select()
        except (NameError, TclError) :
            cox = Toplevel(fenetre)
            changement(2)

## Boutons
# Les boutons sont répartis sur deux lignes : frame2 (ligne du haut) et frame3 (ligne du bas)
# La création des boutons est référencée dans un sous-programme afin de pouvoir les détacher de la fenêtre principale en cas de besoin

def boutons() :
    # Boutons de la ligne du haut (action sur l'avance auto)
    next = Button(frame2, text = "Étape suivante", command = step) # Passe à l'étape suivante
    marche = Button(frame2, text = "Avance auto", command = avance) # Lance l'avance automatique
    arret = Button(frame2, text = "Stop", command = stop) # Arrête l'avance automatique
    vite = Button(frame2, text = "Avance rapide", command = accelere) # Lance l'avance rapide
    
    next.pack(side = LEFT, padx = 4, pady = 4)
    marche.pack(side = LEFT, padx = 4, pady = 4)
    vite.pack(side = LEFT, padx = 4, pady = 4)
    arret.pack(side = LEFT, padx = 4, pady = 4)
    
    # Boutons de la ligne du bas (action sur la grille + ragequit)
    random = Button(frame3, text = "Configuration aléatoire", command = aleatoire) # Génère et affiche un état aléatoire
    delete = Button(frame3, text = "Effacer", command = effacer) # Efface la grille
    espace = Label(frame3, text = "               ")
    ragequit = Button(frame3, text = "Ragequit", command = fenetre.destroy) # Pour quitter
    
    random.pack(side = LEFT, padx = 4, pady = 4)
    delete.pack(side = LEFT, padx = 4, pady = 4)
    espace.pack(side = LEFT, padx = 2, pady = 4)
    ragequit.pack(side = RIGHT, padx = 4, pady = 4)

boutons()



## La barre de menu


menubar = Menu(fenetre)

menufichier = Menu(menubar, tearoff = 0)
menufichier.add_command(label = "Sauvegarder", command = lambda : top(1))
menufichier.add_command(label = "Ouvrir", command = lambda : top(0))
menufichier.add_separator()
menufichier.add_command(label = "Quitter", command = fenetre.destroy)
menubar.add_cascade(label = "Fichier", menu = menufichier)

menuaffichage = Menu(menubar, tearoff = 0)
menuaffichage.add_command(label = "Affichage fractionné", command = fractionne)
menuaffichage.add_command(label = "Détails", command = lambda : changement(1))
menubar.add_cascade(label = "Affichage", menu = menuaffichage)

menusim = Menu(menubar, tearoff = 0)
menusim.add_command(label = "Changer les règles", command = lambda : changement(2))
menusim.add_command(label = "Simulation avancée", command = draft)
menubar.add_cascade(label = "Simulation", menu = menusim)

fenetre.config(menu=menubar)

## Instruction de boucle principale
# L'instruction "fenetre.mainloop()" est juste trop importante pour que j'en parle pas. C'est la ligne qui clot le programme en beauté.


fenetre.mainloop()
