#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 24 novembre 2021
"""

MOVE_N = "N"  # "U" # Boiteau 24/04/2025
MOVE_S = "S"  # "D" # Boiteau 24/04/2025
MOVE_O = "O"  # "L" # Boiteau 24/04/2025
MOVE_E = "E"  # "R" # Boiteau 24/04/2025

import random

from AIs.Fonctions import *


#############################################################################################
# La fonction preprocessing est appelee au debut de la partie
# Elle peut etre utile pour realiser des calculs qui seront utilises ensuite pour effectuer
# les mouvements du joueur dans la fonction Go
#############################################################################################
# Parametres d'entree :
# mazeMap          : dict(pair(int, int), dict(pair(int, int), int)) représentant le labyrinthe
# mazeWidth        : int                  = largeur du labyrinthe (nombre de cases)
# mazeHeight       : int                  = hauteur du labyrinthe
# playerLocation   : pair(int, int)       = coordonnes 2D du rat
# opponentLocation : pair(int,int)        = coordonnes 2D du python
# piecesOfCheese   : list(pair(int, int)) = liste de coordonn�es 2D de chaque fromage
# timeAllowed      : float                = temps max alloué la fonction (en secondes)
##############################################################################################
#    Cette fonction ne retourne rien au sens trict (pas de return) mais le resultat est      #
#    place dans la variable globale chemin recuperable dans le reste du programme            #
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    # print("mazeMap =",mazeMap)
    # print("mazeWidth =",mazeWidth)
    # print("mazeHeight =",mazeHeight)
    # print("playerLocation =",playerLocation)
    # print("opponentLocation =",opponentLocation)
    # print("piecesOfCheese =",piecesOfCheese)
    return


##############################################################################################
# La fonction Go est appelee a chaque fois qu'un mouvement du joueur est attendu
##############################################################################################
# Parametres d'entree :
# mazeMap : dict(pair(int, int), dict(pair(int, int), int)) représentant le labyrinthe
# mazeWidth : int = largeur du labyrinthe (nombre de cases)
# mazeHeight : int = hauteur du labyrinthe
# playerLocation : couple (int, int) = coordonnes 2D du rat
# opponentLocation : pair(int, int) = coordonnes 2D du python
# playerScore : float = nombre de fromages manges par le rat
# opponentScore : float = nombre de fromages manges par le python
# piecesOfCheese : list(pair(int, int)) = liste de coordonn�es 2D de chaque fromage
# timeAllowed : float = temps max alloué la fonction (en secondes)
################################################################################################
# Cette fonction retourne un mouvement (MOVE_N, MOVE_S, MOVE_O, MOVE_E)


def go(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    matAccess = matriceAcces(mazeMap, mazeWidth, mazeHeight)
    print(matAccess)
    targetCheese = piecesOfCheese[0]  # first cheese on list
    # print("playerLocation =",playerLocation) # affichage de la position du rat : a priori, différente à chaque appel
    # print("targetCheese =",targetCheese)     # affichage de la position du froma : elle ne bougera pas
    [Xr, Yr] = playerLocation  # Coordonnées du Rat
    [Xf, Yf] = targetCheese  # Coordonnées du Fromage cible
    #
    listeChoix = [MOVE_N, MOVE_S, MOVE_O, MOVE_E]  # Liste exhaustive des choix possibles pour un mouvement
    mvt = random.choice(listeChoix)  # un des 4 déplacements choisis aléatoirement

    return mvt  # on renvoi le mouvement choisi à l'application pour que le rat se déplace dans le tour courant
