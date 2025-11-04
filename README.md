PyRat ![icon](resources/various/pyrat.ico)
===================

![icon](resources/illustrations/rat.png)

Remi a faim. Il y a du fromage dans le labyrinthe. Aide-le à le trouver !

Quick Guide
---------------------------------
1. Installe le jeu (voir section Installation)
2. Copie le fichier bots/bot.py.example vers bots/mon_bot.py et édite-le pour créer ton propre bot
3. Edite le fichier config.ini pour choisir ton bot et les paramètres du labyrinthe
4. Lance le jeu (voir section Installation)

Installation
---------------------------------
- Ouvrir le dossier pyrat dans vs code
- Ouvrir un terminal (console) (Ctrl+Shift+%) ou via le menu Terminal/Nouveau Terminal
- Dans la console, lancer la commande suivante pour insaller uv : `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Une fois uv installé, installer et lancer PyRat avec la commande suivante (toujours dans la console): `uv run main.py`
- Le jeu devrait se lancer. Utiliser les touches directionnelles pour déplacer le rat manuellement, ou laisser le bot jouer à sa place.
- Pour pouvoir lancer le jeu via VSCode, sélectionner l'environnement Python (Ctrl+Shift+P puis "Python: Select Interpreter" et choisir "pyrat")
- Vous pouvez maintenant lancer le jeu en ouvrant le fichier main.py et en cliquant sur "Run Python File" en haut à droite.


Configuration
---------------------------------

Le fichier de configuration par défaut est config.ini. Vous pouvez passer un autre fichier comme argument lors de l'exécution du jeu.

**Exemples**
-  `uv run main.py -c another_config.ini`
-  `uv run main.py -c levels/level_01.ini`


Le fichier de configuration est un ensemble de paires clé=valeur. Les clés disponibles sont:
- `width`: largeur du labyrinthe (en cellules)
- `height`: hauteur du labyrinthe (en cellules)
- `pieces` : nombre de morceaux de fromage dans le labyrinthe
- `density`: densité des murs dans le labyrinthe (entre 0 et 1, 0= pas de mur, 1=plein de murs)
- `rat` : nom du fichier python dans le répertoire bots/ contrôlant le rat
- `step`: True/False, si True le jeu est en mode pas à pas. Il s'arrête à chaque tour et attend une entrée utilisateur pour continuer (Touche directionnelle, ou `C` pour continuer le bot)


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

une cellule (case de la grille) est représentée par un tuple (i, j)
- (0,0) représente la cellule en haut à gauche
- (5,0) représente la cellule de la 6ème ligne, première colonne
- (1,5) représente la cellule de la 2ème ligne, 6ème colonne


### neighbors_map

neighbors_map est un dictionnaire qui associe chaque cellule à ses cellules voisines ET atteignables

**Exemple** : `{(0,0):[(0,1),(1,0)], (0,1):[(0,0),(1,1),(0,2)], ...}`

Ce qui se lit :
- depuis la cellule (0,0), on peut aller en (0,1) ou en (1,0)
- depuis la cellule (0,1), on peut aller en (0,0), en (1,1) ou en (0,2)

Si on a un mur entre deux cellules, elles ne sont pas considérées comme voisines, et elles n'apparaissent pas dans la liste des voisines.

### player_location

player_location est la cellule où se trouve le joueur (coordonnées i,j) i: row; j: column

**Exemple** : (0,0) => Le joueur est dans la cellule (0,0), en bhaut à gauche

### pieces_of_cheese

Liste des cellules où se trouvent les morceaux de fromage

**Exemple** : [(0,1), (4,3), (2,5)] => Il y a du fromage en (0,1), en (4,3) et en (2,5)
