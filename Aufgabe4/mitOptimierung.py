# Aufgabe 4: Nandu (optimized)

import sys
import time

class Node:
    def __init__(self):
        self.number = 0
        self.cache = None
        self.children = set()
        
class TruthTable:
    def __init__(self, literals, arr):
        self.arr = arr
        self.literals = literals # Q1, Q2, ..., Qn

    # Hilfsmethode
    def calculate_index(self, s):
        index = 0
        for i,v in enumerate(self.literals):
            if s & (1 << (v - 1)):
                index += 2 ** i
        return index

    # Gibt einen Bestimmenten Wert aus der Wahrheitstabelle zurueck
    def get(self, s):
        return self.arr[self.calculate_index(s)]
        
    # Fuegt zwei Wahrheitstabellen zusammen
    def merge(self, other, func):
        new_literals = sorted(list(set(self.literals + other.literals)))
        new_arr = [False] * (2 ** len(new_literals))
        for i in range(len(new_arr)):
            s = 0
            for j in range(len(new_literals)):
                s |= ((i >> j) & 1) << (new_literals[j] - 1)
            new_arr[i] = func(self.get(s), other.get(s))
        return TruthTable(new_literals, new_arr)

    # Wendet eine Funktion auf alle Werte der Wahrheitstabelle an und gibt eine neue Wahrheitstabelle zurueck
    def modify(self, func):
        new_literals = self.literals.copy()
        new_arr = self.arr.copy()
        for i in range(len(self.arr)):
            new_arr[i] = func(new_arr[i])
        return TruthTable(new_literals, new_arr)

    # Gibt die Wahrheitstabelle als String zurueck
    def __str__(self) -> str:
        string = "".join([f"Q{i}|" for i in self.literals]) + "L" + "\n"
        for i in range(len(self.arr)):
            for j in range(len(self.literals)):
                string += str((i >> j) & 1) + " |"
            string += str(bin(self.arr[i])[2:]) + "\n"
        return string

t = time.time()

# Modellieren des Graphen
with open(sys.argv[1]) as file:
    output = [] # Liste der L-Knoten
    x, y = map(int, file.readline().split())
    grid = [l.split() for l in file.read().splitlines()]
    # Speichert die Knoten in kombination der Koordinaten
    nodes = [[None] * x for _ in range(y)]
    for i in range(x):
        if grid[0][i].startswith("Q"):
            input_node = Node()
            input_node.number = int(grid[0][i][1:])
            nodes[0][i] = input_node
    for j in range(1, y):
        i = 0
        while i < x:
            if grid[j][i] == "X":
                i+=1
                continue
            else:
                # Der B Knoten speichert eine Referenz auf den Knoten, der sich ueber ihm befindet
                if grid[j][i] == "B":
                    nodes[j][i+1] = nodes[j-1][i+1]
                    nodes[j][i] = nodes[j-1][i]
                    i+=2
                    continue
                elif grid[j][i].startswith("L"):
                    nodes[j][i] = Node()
                    nodes[j][i].number = int(grid[j][i][1:])
                    nodes[j][i].children = {nodes[j-1][i]}
                    output.append(nodes[j][i])
                    i+=1
                    continue
                else:
                    not_node = Node()
                    # Ein NAND Gatter besteht aus einem NOT Knoten, der ein AND Gatter als Kind hat
                    if grid[j][i] == "W":
                        and_node = Node()
                        and_node.children = {nodes[j-1][i+1], nodes[j-1][i]}
                        not_node.children = {and_node}
                        nodes[j][i+1] = nodes[j][i] = not_node
                    elif grid[j][i] == "r":
                        not_node.children = {nodes[j-1][i+1]}
                    elif grid[j][i] == "R":
                        not_node.children = {nodes[j-1][i]}
                    nodes[j][i] = nodes[j][i+1] = not_node
                    i+=2
                    continue

# Rekursive Funktion, die die Wahrheitstabelle eines Knotens berechnet
def calculate_truth_table(node) -> TruthTable:
    # Wenn die Wahrheitstabelle bereits berechnet wurde, wird sie aus dem Cache gelesen
    if node.cache != None:
        return node.cache
    # Basisfall, Wenn der Knoten ein Input Knoten ist, wird die Standartwahrheitstabelle zurueckgegeben
    if len(node.children) == 0:
        return TruthTable([node.number], [False, True])
    # Ist der Knoten ein NOT Knoten, wird die Wahrheitstabelle des Kindes negiert
    elif len(node.children) == 1:
        t = calculate_truth_table(list(node.children)[0])
        node.cache = t.modify(lambda e: not e)
    # Ist der Knoten ein AND Knoten, werden die Wahrheitstabellen der Kinder gemerged
    elif len(node.children) == 2:
        t_1 = calculate_truth_table(list(node.children)[0])
        t_2 = calculate_truth_table(list(node.children)[1])
        node.cache = t_1.merge(t_2, lambda a, b: a and b)
    return node.cache

# Berechnen der Wahrheitstabellen fuer alle L-Knoten
for node in output:
    print(f"Tabelle fuer L{node.number}")
    print(calculate_truth_table(list(node.children)[0]))

print(f"Berechnungszeit: {time.time() - t}")