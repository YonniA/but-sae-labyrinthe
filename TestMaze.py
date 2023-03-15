from Maze import *

print("Exemples d’utilisation :")
laby = Maze(4, 4)
print(laby.info())
print("print(laby)")
print(laby)

print("Cassons quelques murs en redéfinissant manuellement les voisinages des cellules concernées :")
laby.neighbors = {
    (0, 0): {(1, 0)},
    (0, 1): {(0, 2), (1, 1)},
    (0, 2): {(0, 1), (0, 3)},
    (0, 3): {(0, 2), (1, 3)},
    (1, 0): {(2, 0), (0, 0)},
    (1, 1): {(0, 1), (1, 2)},
    (1, 2): {(1, 1), (2, 2)},
    (1, 3): {(2, 3), (0, 3)},
    (2, 0): {(1, 0), (2, 1), (3, 0)},
    (2, 1): {(2, 0), (2, 2)},
    (2, 2): {(1, 2), (2, 1)},
    (2, 3): {(3, 3), (1, 3)},
    (3, 0): {(3, 1), (2, 0)},
    (3, 1): {(3, 2), (3, 0)},
    (3, 2): {(3, 1)},
    (3, 3): {(2, 3)}
}

print(laby)

laby.neighbors[(1,3)].remove((2,3))
laby.neighbors[(2,3)].remove((1,3))
print(laby)

laby.neighbors[(1, 3)].add((2, 3))
laby.neighbors[(2, 3)].add((1, 3))
print(laby)

laby.neighbors[(1, 3)].remove((2, 3))
print(laby)
print(laby.info())

laby.neighbors[(2, 3)].remove((1,3))

c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"Il n'y a pas de mur entre {c1} et {c2} car elles sont mutuellement voisines")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"Il y a un mur entre {c1} et {c2} car {c1} n'est pas dans le voisinage de {c2} et {c2} n'est pas dans le voisinage de {c1}")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2}")

c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"{c1} est accessible depuis {c2} et vice-versa")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"{c1} n'est pas accessible depuis {c2} et vice-versa")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2}")

L = []
for i in range(laby.height):
    for j in range(laby.width):
        L.append((i,j))
print(f"Liste des cellules : \n{L}")

laby = Maze(4, 4, empty = True)
print(laby)

laby = Maze(4, 4, empty = False)
print(laby)

laby = Maze(5, 5, empty = True)
print(laby)

laby.add_wall((0,0), (0,1))
print(laby)

laby.remove_wall((0, 0), (0, 1))
print(laby)

print(laby.get_walls())
laby.add_wall((0,0), (0,1))
print(laby.get_walls())

laby = Maze(5, 5, empty = True)
print(laby)
laby.fill()
print(laby)
laby.empty()
print(laby)

print(laby.get_contiguous_cells((0,1)))

laby.add_wall((0,0), (0,1))
print(laby.get_reachable_cells((0,1)))

print(laby.get_cells())

laby = Maze.gen_btree(4, 4)
print(laby)

laby = Maze.gen_sidewinder(4, 4)
print(laby)

laby = Maze.gen_fusion(15,15)
print(laby)

laby = Maze.gen_exploration(15,15)
print(laby)

laby = Maze.gen_wilson(10,10)
print(laby)

laby = Maze(4,4, empty = True)
print(laby.overlay({
    (0, 0):'c',
    (0, 1):'o',
    (1, 1):'u',
    (2, 1):'c',
    (2, 2):'o',
    (3, 2):'u',
    (3, 3):'!'}))

laby = Maze(4,4, empty = True)
path = {(0, 0): '@',
        (1, 0): '*',
        (1, 1): '*',
        (2, 1): '*',
        (2, 2): '*',
        (3, 2): '*',
        (3, 3): '§'}
print(laby.overlay(path))

laby = Maze.gen_fusion(15, 15)
solution = laby.solve_dfs((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby.overlay(str_solution))

laby = Maze.gen_exploration(15, 15)
solution = laby.solve_bfs((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby.overlay(str_solution))

laby = Maze.gen_exploration(15, 15)
solution = laby.solve_rhr((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby.overlay(str_solution))