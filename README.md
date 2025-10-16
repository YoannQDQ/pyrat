PyRat ![icon](resources/various/pyrat.ico)
===================

Remi a faim. Il y a du fromage dans le labyrinthe. Aide-le à le trouver !

Quick Guide
---------------------------------
1. Installe le jeu (voir section Installation)
2. Copie le fichier bots/bot.py.example vers bots/mon_bot.py et édite-le pour créer ton propre bot
3. Edite le fichier config.ini pour choisir ton bot et les paramètres du labyrinthe
4. Lance le jeu (voir section Installation)

Installation
---------------------------------

- Installer uv : `pip install uv`
- Synchroniser uv (installera toutes les dépendances) : `uv sync`
- Lancer le jeu : `uv run main.py`


Configuration
---------------------------------

Le fichier de configuration par défaut est config.ini. Vous pouvez passer un autre fichier comme argument lors de l'exécution du jeu.
Example: `uv run main.py -c another_config.ini`

Le fichier de configuration est un ensemble de paires clé=valeur. Les clés disponibles sont:
- width: largeur du labyrinthe (en cellules)
- height: hauteur du labyrinthe (en cellules)
- pieces : nombre de morceaux de fromage dans le labyrinthe
- density: densité des murs dans le labyrinthe (entre 0 et 1, 0= pas de mur, 1=plein de murs)
- rat : nom du fichier python dans le répertoire bots/ contrôlant le rat
- step: True/False, si True le jeu est en mode pas à pas. Il s'arrête à chaque tour et attend une entrée utilisateur pour continuer (Touche directionnelle, ou `C` pour continuer le bot)


Bots Files
---------------------------------

Les fichiers de bots sont situés dans le répertoire bots/. Vous pouvez créer votre propre bot en copiant bot.py.example vers bots/votre_bot.py et en l'éditant.
Le fichier de bot doit contenir au moins la fonction `go`, qui prend 3 arguments et retourne une des constantes MOVE_N, MOVE_S, MOVE_E ou MOVE_O.

Cette fonction est appelée à chaque tour de jeu. Elle doit retourner une des constantes `MOVE_N`, `MOVE_S`, `MOVE_E` ou `MOVE_O` pour indiquer dans quelle direction le joueur doit se déplacer.
Si le déplacement n'est pas possible (ex : il y a un mur dans cette direction, ou le bord du labyrinthe), alors le joueur ne bouge pas, et perd son tour (le compteur de "Miss" augmente de 1).



```Python
from bots.utils import MOVE_E, MOVE_N, MOVE_O, MOVE_S

def go(neighbors_map, player_location, pieces_of_cheese):
    # A modifier : exemple de bot qui se contente d'aller toujours à l'Est
    return MOVE_E
```



### Cellule

une cellule (case de la grille) est représentée par un tuple (x, y)
- (0,0) représente la cellule en bas à gauche
- (5,0) représente la 5ème cellule de la ligne du bas
- (1,5) représente la 5ème cellule (en partant du bas) de la deuxième colonne


### neighbors_map

neighbors_map est un dictionnaire qui associe chaque cellule à ses cellules voisines ET atteignables

**Exemple** : `{(0,0):[(0,1),(1,0)], (0,1):[(0,0),(1,1),(0,2)], ...}`

Ce qui se lit :
- depuis la cellule (0,0), on peut aller en (0,1) ou en (1,0)
- depuis la cellule (0,1), on peut aller en (0,0), en (1,1) ou en (0,2)

Si on a un mur entre deux cellules, elles ne sont pas considérées comme voisines, et elles n'apparaissent pas dans la liste des voisines.

### player_location

player_location est la cellule où se trouve le joueur (coordonnées x,y)

**Exemple** : (0,0) => Le joueur est dans la cellule (0,0), en bas à gauche

### pieces_of_cheese

Liste des cellules où se trouvent les morceaux de fromage

**Exemple** : [(0,1), (4,3), (2,5)] => Il y a du fromage en (0,1), en (4,3) et en (2,5)
