#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 24 novembre 2021
"""

MOVE_U = "N"  # "U" # Boiteau 24/04/2025
MOVE_D = "S"  # "D" # Boiteau 24/04/2025
MOVE_L = "O"  # "L" # Boiteau 24/04/2025
MOVE_R = "E"  # "R" # Boiteau 24/04/2025

import random


#############################################################################################
# La fonction preprocessing est appelee au debut de la partie
# Elle peut etre utile pour realiser des calculs qui seront utilises ensuite pour effectuer
# les mouvements du joueur dans la fonction turn
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
# La fonction turn est appelee a chaque fois qu'un mouvement du joueur est attendu
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
# Cette fonction retourne un mouvement (MOVE_NORTH, MOVE_WEST ...)


# def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
def go(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    # print("piecesOfCheese =",piecesOfCheese)
    targetCheese = piecesOfCheese[0]  # first cheese on list
    # targetCheese=bestCheese(playerLocation,piecesOfCheese) # Fromage le plus proche
    # print("playerLocation =",playerLocation)
    # print("targetCheese =",targetCheese)
    [Xr, Yr] = playerLocation  # Coordonées du Rat
    [Xf, Yf] = targetCheese  # Coordonées du Fromage cible
    #
    listeChoix = [MOVE_U, MOVE_D, MOVE_L, MOVE_R]  # Liste exhaustive des choix possibles
    mvt = random.choice(listeChoix)  # un des 4 déplacements choisis aléatoirement
    # mvt est le déplacement renvoyé à chaque itération ou en mode pas à pas (touche 'S' du clavier)
    # print("mouvement =",mvt)
    return mvt
