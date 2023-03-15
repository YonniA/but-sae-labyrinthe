import random
class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty=False):
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        if not empty:
            self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}
        else:
            self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}
            for i in range(height):
                for j in range(width):
                    if i > 0:
                        self.neighbors[(i, j)].add((i - 1, j))
                    if i < height - 1:
                        self.neighbors[(i, j)].add((i + 1, j))
                    if j > 0:
                        self.neighbors[(i, j)].add((i, j - 1))
                    if j < width - 1:
                        self.neighbors[(i, j)].add((i, j + 1))

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    # Permet de rajouter un mur entre deux coordonnées c1 et c2 d'un labyrinthe self
    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c1 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire

    def remove_wall(self, c1, c2):
        """
        Supprime le mur entre deux cellules du labyrinthe et ne renvoi rien

        :param c1: Un tuple représentant les coordonnées de la première cellulee
        :param c2: Un tuple représentant les coordonnées de la seconde cellule
        """
        # Test pour savoir si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Si c2 n'est pas un voisin de c1
        if c2 not in self.neighbors[c1]:
            # Ajoute c2 comme voisin de c1
            self.neighbors[c1].add(c2)
        # Si c1 n'est pas un voisin de c2
        if c1 not in self.neighbors[c2]:
            # Ajoute c1 comme voisin de c2
            self.neighbors[c2].add(c1)

    # Permet d'obtenir une liste de tuple des coordonnées des cellules ayant un mur entre elles
    def get_walls(self):
        """
        Renvoi une liste des murs pouvant représenter le labyrinthe

        :return: Une liste de tous les murs dans le labyrinthe
        """
        walls = []  # Initialisation d'une liste vide pour stocker les murs
        # Parcours des lignes du labyrinthe
        for i in range(self.height):
            # Parcours des colonnes du labyrinthe
            for j in range(self.width):
                # Si la cellule actuelle a une cellule voisine en-dessous et ne sont pas voisins
                if i < self.height - 1 and (i + 1, j) not in self.neighbors[(i, j)]:
                    # Ajoute le mur à la liste des murs
                    walls.append(((i, j), (i + 1, j)))
                # Si la cellule actuelle a une cellule voisine à droite et ne sont pas voisins
                if j < self.width - 1 and (i, j + 1) not in self.neighbors[(i, j)]:
                    # Ajoute le mur à la liste des murs
                    walls.append(((i, j), (i, j + 1)))
        # Renvoi la liste des murs
        return walls

    def fill(self):
        """
        Remplace chaque voisin de chaque cellule du labyrinthe par une liste vide et ne renvoi rien
        """
        # Parcours de toutes les cellules du labyrinthe
        for key in self.neighbors.keys():
            # Remplace les voisins de chaque cellule par une liste vide
            self.neighbors[key] = []

    def empty(self):
        """
        Initialise tous les voisins de chaque cellule par une cellule vide
        """
        # Initialisation des voisins de chaque cellule à une cellule vide
        self.neighbors = {(i, j): set() for i in range(self.height) for j in range(self.width)}
        # Parcours de toutes les cellules du labyrinthe
        for i in range(self.height):
            for j in range(self.width):
                # Ajout des voisins pour chaque cellule
                if i > 0:
                    # Voisin du haut
                    self.neighbors[(i, j)].add((i - 1, j))
                if i < self.height - 1:
                    # Voisin du bas
                    self.neighbors[(i, j)].add((i + 1, j))
                if j > 0:
                    # Voisin de gauche
                    self.neighbors[(i, j)].add((i, j - 1))
                if j < self.width - 1:
                    # Voisin de droite
                    self.neighbors[(i, j)].add((i, j + 1))

    def get_contiguous_cells(self, c: tuple) -> list:
        """
        Renvoi une liste des cellules voisines d'une cellule passée en paramètre

        :param c: Tuple représentant les coordonnées d'une cellule du labyrinthe
        """
        # Récupération des coordonnées x et y de la cellule
        x = c[0]
        y = c[1]
        # Initialisation d'une liste de potentielles cellules voisines
        cell_voisines = [(x, y + 1),
                            (x, y - 1),
                            (x - 1, y),
                            (x + 1, y)]
        # Vérification de si les cellules voisines sont valides
        for cell in cell_voisines:
            # On supprime les cellules qui ne sont pas dans le labyrinthe
            if not (0 <= cell[0] < self.height and 0 <= cell[1] < self.width):
                cell_voisines.remove(cell)
        # Renvoi la liste des cellules voisines
        return cell_voisines

    def get_reachable_cells(self, c):
        """
        Renvoi une liste de toutes les cellules accessibles à partir d'une cellule passée en paramètre

        :param c: Tuple représentant les coordonnées d'une cellule du labyrinthe
        :return: Une liste de typles représentant les coordonnées de toute sles cellules accessibles à partir d'une cellule passée en paramètre
        """
        return [cell for cell in self.neighbors[c]]

    def get_cells(self):
        """
        Renvoi une liste de toutes les cellules du labyrinthe

        :return: Liste de tuples représentant les coordonnées de chaque cellule du labyrinthe
        """
        return [cell for cell in self.neighbors.keys()]

    @classmethod
    def gen_btree(cls, h, w):
        """
        Créer un labyrinthe en utilisation l'algorithme de génération par arbre binaire

        :param h: Nombre de lignes du labyrinthe
        :param w: Nombre de colonnes du labyrinthe
        :return: Un labyrinthe
        """
        # Créer un nouveau labyrinthe
        maze = Maze(h, w)
        # Itère sur toutes les cellules dans le labyrinthe
        for i in range(h):
            for j in range(w):
                # Détermine les directions valides pour se déplacer sans sortir du labyrinthe
                directions = []
                if j < w - 1:
                    directions.append('E')
                if i < h - 1:
                    directions.append('S')
                # Si il y 1 ou plusieurs directions possible
                if len(directions) > 0:
                    # en prendre une au hasard
                    direction = random.choice(directions)
                    # Retire le mur à la direction choisie
                    if direction == 'E':
                        maze.remove_wall((i, j), (i, j + 1))
                    elif direction == 'S':
                        maze.remove_wall((i, j), (i + 1, j))
        # Renvoi le labyrinthe généré
        return maze

    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Génère un labyrinthe de dimensions h x w en utilisant l'algorithme Sidewinder

        :param h: Nombre de lignes a générer pour le labyrinthe
        :param w: Nombre de colonnes à générer pour le labyrinthe
        :return: Un labyrinthe ayant pour dimensions h x w
        """
        # Créer un nouveau labyrinthe
        maze = Maze(h, w)
        # Parcours des cellules avec l'algorithme Sidewinder
        for i in range(h - 1):
            sequence = []
            for j in range(w - 1):
                sequence.append((i, j))
                if (j == w - 1 or i < h - 1) and bool(random.getrandbits(1)):
                    # Retire un mur vers le sud
                    choix = random.choice(sequence)
                    maze.remove_wall(choix, (choix[0] + 1, choix[1]))
                    sequence = []
                else:
                    # Retire un mur vers l'est
                    maze.remove_wall((i, j), (i, j + 1))
            sequence.append((i, j))
            choix = random.choice(sequence)
            maze.remove_wall(choix, (choix[0] + 1, choix[1]))
        # Retire les murs du bas pour n'avoir qu'un seul passage
        for j in range(w - 1):
            maze.remove_wall((h - 1, j), (h - 1, j + 1))
        # Renvoi le labyrinthe généré
        return maze

    @classmethod
    def gen_fusion(cls, h, w):
        """
        Créer un labyrinthe en utilisant l'algorithme de fusion de chemin

        :param h: Nombre de lignes du labyrinthe
        :param w: Nombre de colonnes du labyrinthe
        :return: Un labyrinthe
        """
        # Créer un nouveau labyrinthe de dimensions h x w
        laby = cls(h, w)
        # Initialisation de tout les labels à (i,j)
        labels = {}
        for i, j in laby.get_cells():
            labels[(i, j)] = (i, j)
        # Liste de tous les murs du labyrinthe
        walls = laby.get_walls()
        # Mélange de la liste des murs
        random.shuffle(walls)
        # Parcours de tous les murs et fusion des cellules adjacentes si les labels sont différents
        for c1, c2 in walls:
            if (0 <= c1[0] < h and
               0 <= c1[1] < w and
               0 <= c2[0] < h and
               0 <= c2[1] < w):
                label1 = labels[c1]
                label2 = labels[c2]
                if label1 != label2:
                    laby.remove_wall(c1, c2)
                    new_label = label2
                    old_label = label1
                    for cell in labels:
                        if labels[cell] == old_label:
                            labels[cell] = new_label
        # Renvoi le labyrinthe généré
        return laby

    @classmethod
    def gen_exploration(cls, h, w):
        """
        Créer un labyrinthe en utilisant l'algorithme d'exploration exhaustive

        :param h: Nombre de lignes du labyrinthe
        :param w: Nombre de colonnes du labyrinthe
        :return: Un labyrinthe
        """
        # Créer un labyrinthe ayant pour dimensions h x w
        laby = cls(h, w)
        # Obtient toutes les cellules du labyrinthe
        cellules_disponibles = laby.get_cells()
        # Choisit aléatoirement la cellule initiale
        cellule_initiale = random.choice(cellules_disponibles)
        # Ajoute la cellule initiale aux cellules visitées
        cellules_visitees = [cellule_initiale]
        # Initialise une pile avec la cellule initiale
        pile = [cellule_initiale]
        # Explore tant que la pile n'est pas vide
        while pile:
            # Retire la première cellule de la pile
            cellule_courante = pile.pop(0)
            # Obtient toutes les cellules adjacentes non visitées
            cellules_non_visitees = []
            for cellule in laby.get_contiguous_cells(cellule_courante):
                if cellule not in cellules_visitees:
                    if 0 <= cellule[0] < h and 0 <= cellule[1] < w:
                        cellules_non_visitees.append(cellule)
            # Si des cellules adjacentes non visitées existent, en choisit une aléatoirement
            # et retire le mur qui les sépare de la cellule courante. Ajoute la cellule choisie
            # à la liste des cellules visitées et à la pile.
            if cellules_non_visitees:
                pile.insert(0, cellule_courante)
                cellule_suivante = random.choice(cellules_non_visitees)
                laby.remove_wall(cellule_courante, cellule_suivante)
                cellules_visitees.append(cellule_suivante)
                pile.insert(0, cellule_suivante)
        # Renvoi le labyrinthe généré
        return laby

