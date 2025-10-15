#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 23 déc. 2021

@author: laferté, guibourg
"""

import numpy

INFINI = 0  # 1000 devient 0, 0 on ne peut pas y aller, n on peut en n pas # boiteau 24/04/2025


def affMatrice(M):
    (W, H) = numpy.shape(M)
    for j in range(H - 1, -1, -1):
        for i in range(W):
            if M[i, j] == INFINI:
                print("-", end="")
            elif M[i, j] == 0:
                print(" ", end="")
            else:
                print(int(M[i, j]), end="")
        print(" ")


##################################################
# Matrice des distances (type matrice adjacence) #
# en entrée mazeMap, mazeWidth, mazeHeight       #
# En sortie : la matrice des distances           # # boiteau 24/04/2025
# En sortie : la matrice des accès (0 ou 1)      #
##################################################
# def matriceDistances(mazeMap, mazeWidth, mazeHeight): # boiteau 24/04/2025
def matriceAcces(mazeMap, mazeWidth, mazeHeight):  # boiteau 24/04/2025
    nbSommets = mazeWidth * mazeHeight
    x = mazeMap[(0, 0)]
    A = numpy.zeros((nbSommets, nbSommets))
    for i in range(mazeWidth):
        for j in range(mazeHeight):  # tenir compte de la symétrie de A et s'arrêter avant ...
            num = j * mazeWidth + i
            x = mazeMap[(i, j)]
            # voisin de droite
            if i < mazeWidth - 1:
                if (i + 1, j) in x:
                    A[num, num + 1] = x[(i + 1, j)]
                    A[num + 1, num] = x[(i + 1, j)]
                else:
                    A[num, num + 1] = INFINI
                    A[num + 1, num] = INFINI
            # voisin de gauche
            if i > 0:
                if (i - 1, j) in x:
                    A[num, num - 1] = x[(i - 1, j)]
                    A[num - 1, num] = x[(i - 1, j)]
                else:
                    A[num, num - 1] = INFINI
                    A[num - 1, num] = INFINI
            # voisin haut
            if j < mazeHeight - 1:
                if (i, j + 1) in x:
                    A[num, num + mazeWidth] = x[(i, j + 1)]
                    A[num + mazeWidth, num] = x[(i, j + 1)]
                else:
                    A[num, num + mazeWidth] = INFINI
                    A[num + mazeWidth, num] = INFINI
            # voisin bas
            if j > 0:
                if (i, j - 1) in x:
                    A[num, num - mazeWidth] = x[(i, j - 1)]
                    A[num - mazeWidth, num] = x[(i, j - 1)]
                else:
                    A[num, num - mazeWidth] = INFINI
                    A[num - mazeWidth, num] = INFINI
    # print("matrice des distances")
    # print("matrice des acces")
    # affMatrice(A)
    return A
