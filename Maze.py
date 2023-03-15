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
        """
        Ajoute le mur entre deux cellules du labyrinthe

        :param c1: Un tuple représentant les coordonnées de la première cellulee
        :param c2: Un tuple représentant les coordonnées de la seconde cellule
        """
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
        Supprime le mur entre deux cellules du labyrinthe

        :param c1: Un tuple représentant les coordonnées de la première cellulee
        :param c2: Un tuple représentant les coordonnées de la seconde cellule
        """
        # Test pour savoir si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        if c2 not in self.neighbors[c1]: # Si c2 n'est pas un voisin de c1
            self.neighbors[c1].add(c2) # Ajoute c2 comme voisin de c1
        if c1 not in self.neighbors[c2]: # Si c1 n'est pas un voisin de c2
            self.neighbors[c2].add(c1) # Ajoute c1 comme voisin de c2


    # Permet d'obtenir une liste de tuple des coordonnées des cellules ayant un mur entre elles
    def get_walls(self):
        """
        Renvoi une liste des murs pouvant représenter le labyrinthe

        :return: Une liste de tous les murs dans le labyrinthe
        """
        walls = []  # Initialisation d'une liste vide pour stocker les murs
        # Parcours de toutes les cellules du labyrinthe
        for i in range(self.height):
            # Parcours des colonnes du labyrinthe
            for j in range(self.width):
                if i < self.height - 1 and (i + 1, j) not in self.neighbors[(i, j)]: # Si la cellule actuelle a une cellule voisine en-dessous et ne sont pas voisins
                    walls.append(((i, j), (i + 1, j))) # Ajoute le mur à la liste des murs
                if j < self.width - 1 and (i, j + 1) not in self.neighbors[(i, j)]: # Si la cellule actuelle a une cellule voisine à droite et ne sont pas voisins
                    walls.append(((i, j), (i, j + 1))) # Ajoute le mur à la liste des murs
        return walls # Renvoi la liste des murs

    def fill(self):
        """
        Remplace chaque voisin de chaque cellule du labyrinthe par une liste vide et ne renvoi rien
        """
        # Parcours de toutes les cellules du labyrinthe
        for key in self.neighbors.keys():
            self.neighbors[key] = [] # Remplace les voisins de chaque cellule par une liste vide

    def empty(self):
        """
        Initialise tous les voisins de chaque cellule par une cellule vide
        """
        self.neighbors = {(i, j): set() for i in range(self.height) for j in range(self.width)} # Initialisation des voisins de chaque cellule à une cellule vide
        # Parcours de toutes les cellules du labyrinthe
        for i in range(self.height):
            for j in range(self.width):
                # Ajout des voisins pour chaque cellule
                if i > 0:
                    self.neighbors[(i, j)].add((i - 1, j)) # Voisin du haut
                if i < self.height - 1:
                    self.neighbors[(i, j)].add((i + 1, j)) # Voisin du bas
                if j > 0:
                    self.neighbors[(i, j)].add((i, j - 1)) # Voisin de gauche
                if j < self.width - 1:
                    self.neighbors[(i, j)].add((i, j + 1)) # Voisin de droite

    def get_contiguous_cells(self, c):
        """
        Renvoie la liste des cellules contigües à c dans la grille (sans s’occuper des éventuels murs).

        :param c: la cellule
        :return: renvoie une liste de voisins
        """
        (i, j) = c
        contiguous_cells = []
        if i > 0:
            contiguous_cells.append((i - 1, j))
        if i < self.height - 1:
            contiguous_cells.append((i + 1, j))

        if j > 0:
            contiguous_cells.append((i, j - 1))
        if j < self.width - 1:
            contiguous_cells.append((i, j + 1))
        return contiguous_cells


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
        génére un labyrinthe grâce à l'algorithme d'arbre binaire.

        :param h: hauteur du labyrinthe
        :param w: largeur du labyrinthe
        :return: le labyrinthe généré
        """
        maze = Maze(h, w) # Création d'un nouveau labyrinthe
        # Itère sur toutes les cellules du labyrinthe
        for i in range(h):
            for j in range(w):
                # Détermine les directions valides pour se déplacer sans sortir du labyrinthe
                directions = []
                if j < w - 1:
                    directions.append('E')
                if i < h - 1:
                    directions.append('S')
                if len(directions) > 0: # Si il y 1 ou plusieurs directions possible
                    direction = random.choice(directions) # en prendre une au hasard
                    # Retire le mur à la direction choisie
                    if direction == 'E':
                        maze.remove_wall((i, j), (i, j + 1))
                    elif direction == 'S':
                        maze.remove_wall((i, j), (i + 1, j))
        return maze # Renvoi le labyrinthe généré

    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        génére un labyrinthe grâce à l'algorithme Sidewinder.

        :param h: hauteur du labyrinthe
        :param w: largeur du labyrinthe
        :return: le labyrinthe généré
        """
        maze = Maze(h, w) # Création d'un nouveau labyrinthe
        # Parcours des cellules du labyrinthe avec l'algorithme Sidewinder
        for i in range(h - 1):
            sequence = []
            for j in range(w - 1):
                sequence.append((i, j))
                if (j == w - 1 or i < h - 1) and bool(random.getrandbits(1)):
                    # Retire un mur vers le sud
                    choix = random.choice(sequence)
                    maze.remove_wall(choix, (choix[0] + 1, choix[1])) # Retire un mur vers le sud
                    sequence = []
                else:
                    maze.remove_wall((i, j), (i, j + 1)) # Retire un mur vers l'est
            sequence.append((i, j))
            choix = random.choice(sequence)
            maze.remove_wall(choix, (choix[0] + 1, choix[1]))
        # Retire les murs du bas pour n'avoir qu'un seul passage
        for j in range(w - 1):
            maze.remove_wall((h - 1, j), (h - 1, j + 1))
        return maze # Renvoi le labyrinthe généré

    @classmethod
    def gen_fusion(cls, h, w):
        """
        génére un labyrinthe grâce à l'algorithme de fusion de chemins.

        :param h: hauteur du labyrinthe
        :param w: largeur du labyrinthe
        :return: le labyrinthe généré
        """
        laby = cls(h, w) # Création d'un nouveau labyrinthe
        # Initialisation de tout les labels à (i,j)
        labels = {}
        for i, j in laby.get_cells():
            labels[(i, j)] = (i, j)
        walls = laby.get_walls() # Liste de tous les murs du labyrinthe
        random.shuffle(walls) # Mélange de la liste des murs
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
        return laby # Renvoi le labyrinthe généré

    @classmethod
    def gen_exploration(cls, h, w):
        """
        génére un labyrinthe grâce à l'algorithme de l'exploration exhaustive.

        :param h: hauteur du labyrinthe
        :param w: largeur du labyrinthe
        :return: le labyrinthe généré
        """
        laby = cls(h, w) # Création d'un nouveau labyrinthe
        cellules_disponibles = laby.get_cells() # Obtient toutes les cellules du labyrinthe
        cellule_initiale = random.choice(cellules_disponibles) # Choisit aléatoirement la cellule initiale
        cellules_visitees = [cellule_initiale] # Ajoute la cellule initiale aux cellules visitées
        pile = [cellule_initiale] # Initialise une pile avec la cellule initiale
        # Explore tant que la pile n'est pas vide
        while pile:
            cellule_courante = pile.pop(0) # Retire la première cellule de la pile
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
        return laby # Renvoi le labyrinthe généré

    @classmethod
    def gen_wilson(cls, h, w):
        """
        génére un labyrinthe grâce à l'algorithme Wilson.

        :param h: hauteur du labyrinthe
        :param w: largeur du labyrinthe
        :return: le labyrinthe généré
        """
        # Génère un labyrinthe plein de murs
        laby = cls(h, w)

        # Génère la liste de toutes les cellules à visiter
        cellules_dispo = laby.get_cells()
        random.shuffle(cellules_dispo)  # Mélange -> Obtenir une cellule aléatoire facilement

        cellules_dispo.pop(0)  # Visite une cellule aléatoire -> Supprimer une cellule de la liste équivaut à "marquer comme visitée"

        while cellules_dispo:  # Tant qu'il reste des cellules à visiter
            chemin = []  # Chemin contiendra toutes les cellules visitées dans cette itération
            cellule_courante = cellules_dispo[
                0]  # Définir une cellule courante aléatoire (cellules_dispo a été mélangé)

            while cellule_courante in cellules_dispo:  # Tant que notre cellule courante n'est pas visitée
                possibilites = laby.get_contiguous_cells(cellule_courante)  # Toutes les directions possibles

                # Supprime la direction de laquelle on vient
                if chemin:
                    possibilites.remove(chemin[-1])

                chemin.append(cellule_courante)  # Ajoute la cellule précédente au chemin
                cellule_courante = random.choice(possibilites)  # Choisi une nouvelle direction aléatoire

                if cellule_courante in chemin:  # Évite les boucles
                    chemin = chemin[0:chemin.index(cellule_courante)]  # Coupe la boucle !

            chemin.append(cellule_courante)  # N'oublie pas la dernière cellule

            # Casse les murs !
            for i in range(1, len(chemin)):
                laby.remove_wall(chemin[i - 1], chemin[i])

            # Marquer comme visitée
            for cellule in chemin[0:-1]:
                cellules_dispo.remove(cellule)
        # Renvoi le labyrinthe généré
        return laby

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            # content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i, j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += " " + content[(0, j)] + " ┃" if (0, j + 1) not in self.neighbors[(0, j)] else " " + content[
                (0, j)] + "  "
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " " + content[(i + 1, j)] + " ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else " " + \
                                                                                                                 content[
                                                                                                                     (
                                                                                                                     i + 1,
                                                                                                                     j)] + "  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt

    def solve_dfs(self, start, stop):
        """
        Résout le labyrinthe en utilisant le parcours en largeur.

        :param start: Cellule servant de point de départ
        :param stop: Cellule servant de point d'arrivée
        :return: la liste des cellules à explorer dans l'ordre pour aller du point start à stop.
        """
        visite = []
        pile = [start]  # Placer start dans la struture d’attente (pile) et marquer start
        found = False
        predecesseurs = {start: start}  # Mémoriser l’élément prédécesseur de start comme étant start
        while len(visite) < self.width * self.height and not found:  # Tant qu’il reste des cellules non-marquées
            cell = pile.pop()  # Prendre la « première » cellule et la retirer de la structure
            if cell == stop:
                found = True  # on a trouvé un chemin vers la cellule de destination
            else:
                for neighbor in self.get_reachable_cells(cell):  # Pour chaque voisine de cell
                    if neighbor not in visite:  # Si elle n’est pas marquée
                        visite.append(neighbor)  # La marquer
                        pile.append(neighbor)  # La mettre dans la structure d’attente
                        predecesseurs[neighbor] = cell  # Mémoriser son prédécesseur comme étant c

        cell = stop
        way = []
        while cell != start:
            way.append(cell)
            cell = predecesseurs[cell]  # mettre le prédécesseur de cell dans cell
        way.append(start)

        return way
    def solve_bfs(self, start, stop):
        """
        Résout le labyrinthe en utilisant le parcours en largeur.

        :param start: Cellule servant de point de départ
        :param stop: Cellule servant de point d'arrivée
        :return: la liste des cellules à explorer dans l'ordre pour aller du point start à stop.
        """
        visite = []
        file = [start]  # Placer start dans la struture d’attente (pile) et marquer start
        found = False
        predecesseurs = {start: start}  # Mémoriser l’élément prédécesseur de start comme étant start
        while len(visite) < self.width * self.height and not found:  # Tant qu’il reste des cellules non-marquées
            cell = file.pop(0)  # Prendre la « première » cellule et la retirer de la structure
            if cell == stop:
                found = True  # on a trouvé un chemin vers la cellule de destination
            else:
                for neighbor in self.get_reachable_cells(cell):  # Pour chaque voisine de cell
                    if neighbor not in visite:  # Si elle n’est pas marquée
                        visite.append(neighbor)  # La marquer
                        file.append(neighbor)  # La mettre dans la structure d’attente
                        predecesseurs[neighbor] = cell  # Mémoriser son prédécesseur comme étant c

        cell = stop
        way = []
        while cell != start:
            way.append(cell)
            cell = predecesseurs[cell]  # mettre le prédécesseur de cell dans cell
        way.append(start)

        return way

    def solve_rhr(self, start, stop):
        """
        Résout le labyrinthe en utilisant la technique de la main droite, à partir de la cellule de départ donnée.

        :param start: cellule de départ
        :param stop: cellule de fin
        :return: La liste ordonnée des cellules visitées pour atteindre la sortie.
        """
        # On initialise la cellule courante avec la cellule de départ et la direction avec 'droite'.
        cellule_courante = start
        direction_courante = 'bas' \
                             ''
        cellules_visitees = [cellule_courante]

        while cellule_courante != stop:
            # On détermine la cellule suivante en fonction de la direction courante.
            if direction_courante == 'droite':
                cellule_suivante = (cellule_courante[0], cellule_courante[1] + 1)
            elif direction_courante == 'bas':
                cellule_suivante = (cellule_courante[0] + 1, cellule_courante[1])
            elif direction_courante == 'gauche':
                cellule_suivante = (cellule_courante[0], cellule_courante[1] - 1)
            else:
                cellule_suivante = (cellule_courante[0] - 1, cellule_courante[1])

            # Si la cellule suivante n'a pas de mur dans la direction courante, on avance dans cette direction.
            if cellule_suivante in self.neighbors[cellule_courante]:
                cellules_visitees.append(cellule_suivante)
                cellule_courante = cellule_suivante
                # On tourne à droite en changeant la direction courante de 90° dans le sens horaire.
                if direction_courante == 'droite':
                    direction_courante = 'bas'
                elif direction_courante == 'bas':
                    direction_courante = 'gauche'
                elif direction_courante == 'gauche':
                    direction_courante = 'haut'
                elif direction_courante == 'haut':
                    direction_courante = 'droite'
            # Sinon, on tourne à gauche en changeant la direction courante de 90° dans le sens anti-horaire.
            else:
                # On tourne à gauche en changeant la direction courante de 90° dans le sens anti-horaire.
                if direction_courante == 'droite':
                    direction_courante = 'haut'
                elif direction_courante == 'haut':
                    direction_courante = 'gauche'
                elif direction_courante == 'gauche':
                    direction_courante = 'bas'
                elif direction_courante == 'bas':
                    direction_courante = 'droite'
        return cellules_visitees

    def distance_geo(self,c1,c2):
        """
        Renvoie la distance geo géodésique

        :param c1: première cellule
        :param c2: deuxième cellule
        :return: la distance geo géodésique
        """
        return len(self.solve_bfs(c1, c2))

    def distance_man(self,c1,c2):
        """
        Renvoie la distance de manhattan

        :param c1: première cellule
        :param c2: deuxième cellule
        :return: la distance de manhattan
        """
        return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])