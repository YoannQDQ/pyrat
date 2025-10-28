"""
CELLULE
==========================
une cellule est représentée par un tuple (x, y)
- (0,0) représente la cellule en bas à gauche
- (5,0) représente la 5ème cellule de la ligne du bas
- (1,5) représente la 5ème cellule (en partant du bas) de la deuxième colonne


neighbors_map
==========================
neighbors_map est un dictionnaire qui associe chaque cellule à ses cellules voisines ET atteignables

Exemple : {(0,0):[(0,1),(1,0)], (0,1):[(0,0),(1,1),(0,2)], ...}

Ce qui se lit :
    - depuis la cellule (0,0), on peut aller en (0,1) ou en (1,0)
    - depuis la cellule (0,1), on peut aller en (0,0), en (1,1) ou en (0,2)

Si on a un mur entre deux cellules, elles ne sont pas considérées comme voisines, et elles n'apparaissent pas dans la liste des voisines.

player_location
==========================
player_location est la cellule où se trouve le joueur (coordonnées x,y)
Exemple : (0,0) => Le joueur est dans la cellule (0,0), en bas à gauche

pieces_of_cheese
==========================
Liste des cellules où se trouvent les morceaux de fromage
Exemple : [(0,1), (4,3), (2,5)] => Il y a du fromage en (0,1), en (4,3) et en (2,5)

function go
==========================
La fonction go est appelée à chaque tour de jeu. Elle doit retourner une des constantes MOVE_N, MOVE_S, MOVE_E ou MOVE_O
pour indiquer dans quelle direction le joueur doit se déplacer.
Si le déplacement n'est pas possible (ex : il y a un mur dans cette direction, ou le bord du labyrinthe),
alors le joueur ne bouge pas, et perd son tour (le compteur de "Miss" augmente de 1).

"""

from bots.utils import MOVE_E, MOVE_N, MOVE_O, MOVE_S

i = 0


def go(neighbors_map, player_location, pieces_of_cheese):
    # A modifier : exemple de bot qui tourne en rond
    global i
    if i % 8 < 2:
        direction = MOVE_E
    elif i % 8 < 4:
        direction = MOVE_N
    elif i % 8 < 6:
        direction = MOVE_O
    else:
        direction = MOVE_S
    i += 1
    return direction
