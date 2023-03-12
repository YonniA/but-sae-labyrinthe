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
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire

    def remove_wall(self, c1, c2):
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        if c2 not in self.neighbors[c1]:
            self.neighbors[c1].add(c2)
        if c1 not in self.neighbors[c2]:
            self.neighbors[c2].add(c1)

    def get_walls(self):
        walls = []
        for i in range(self.height):
            for j in range(self.width):
                if i < self.height - 1 and (i + 1, j) not in self.neighbors[(i, j)]:
                    walls.append(((i, j), (i + 1, j)))
                if j < self.width - 1 and (i, j + 1) not in self.neighbors[(i, j)]:
                    walls.append(((i, j), (i, j + 1)))
        return walls

    def fill(self):
        for key in self.neighbors.keys():
            self.neighbors[key] = []

    def empty(self):
        self.neighbors = {(i, j): set() for i in range(self.height) for j in range(self.width)}
        for i in range(self.height):
            for j in range(self.width):
                if i > 0:
                    self.neighbors[(i, j)].add((i - 1, j))
                if i < self.height - 1:
                    self.neighbors[(i, j)].add((i + 1, j))
                if j > 0:
                    self.neighbors[(i, j)].add((i, j - 1))
                if j < self.width - 1:
                    self.neighbors[(i, j)].add((i, j + 1))

    def get_contiguous_cells(self, c: tuple) -> list:
        x = c[0]
        y = c[1]
        cell_voisines = [(x, y + 1),
                            (x, y - 1),
                            (x - 1, y),
                            (x + 1, y)]
        for cell in cell_voisines:
            if not (0 <= cell[0] < self.height and
                    0 <= cell[1] < self.width):
                cell_voisines.remove(cell)
        return cell_voisines

    def get_reachable_cells(self, c):
        return [cell for cell in self.neighbors[c]]

    def get_cells(self):
        return [cell for cell in self.neighbors.keys()]

    @classmethod
    def gen_btree(cls, h, w):
        maze = Maze(h, w)
        for i in range(h):
            for j in range(w):
                directions = []
                if j < w - 1:
                    directions.append('E')
                if i < h - 1:
                    directions.append('S')
                if len(directions) > 0:
                    direction = random.choice(directions)
                    if direction == 'E':
                        maze.remove_wall((i, j), (i, j + 1))
                    elif direction == 'S':
                        maze.remove_wall((i, j), (i + 1, j))
        return maze

    @classmethod
    def gen_sidewinder(cls, h, w):
        maze = Maze(h, w)
        for i in range(h - 1):
            sequence = []
            for j in range(w - 1):
                sequence.append((i, j))
                if (j == w - 1 or i < h - 1) and bool(random.getrandbits(1)):
                    choix = random.choice(sequence)
                    maze.remove_wall(choix, (choix[0] + 1, choix[1]))
                    sequence = []
                else:
                    maze.remove_wall((i, j), (i, j + 1))
            sequence.append((i, j))
            choix = random.choice(sequence)
            maze.remove_wall(choix, (choix[0] + 1, choix[1]))
        for j in range(w - 1):
            maze.remove_wall((h - 1, j), (h - 1, j + 1))
        return maze


