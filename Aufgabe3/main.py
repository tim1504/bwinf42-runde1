# Aufgabe 3: Zauberschule

# Dieses Python Modul implementiert einen Binary Heap, der als Priority Queue verwendet wird
import heapq
import sys
import time

t_start = time.time()

f = open(sys.argv[1])
height, width = map(int, f.readline().split())
# Dreidimensionales Array, das die Distanz jedes Punktes zum Startpunkt speichert
# Waende haben den Wert -1 und werden somit vom Algorithmus ignoriert
dist = [[[-1] * 2 for _ in range(height)] for _ in range(width)]

for z in range(2):
    for y in range(height):
        for x in range(width):
            c = f.read(1)
            if c == "A":
                start = (x, y, z)
                dist[x][y][z] = 0
            elif c != "#":
                dist[x][y][z] = float('inf')
                if c == "B": end = (x, y, z)
        f.read(1)
    f.read(1)
f.close()

# Priority Queue, die die Punkte nach ihrer heuristischen Distanz sortiert
queue = [(0,0) + start]
# Dictionary, das fuer jeden Punkt den Vorgaenger und den Schritt dorthin speichert
source = {}
while queue:
    _, g, x, y, z = heapq.heappop(queue)
    # Wurde der Punkt schon mal besucht, wird er uebersprungen
    if g > dist[x][y][z]: continue
    if (x, y, z) == end:
        break
    # Berechnung der Kanten des Knotens anhand der Koodinaten
    for tg, tx, ty, tz, tc in [(g+1, x+1, y, z, '>'), (g+1, x-1, y, z, '<'), (g+1, x, y+1, z, 'v'), (g+1, x, y-1, z, '^'), (g+3, x, y, not z, '!')]:
        # Das freie Feld kann ueber einen kuerzeren Weg erreicht werden
        if tg < dist[tx][ty][tz]:
            dist[tx][ty][tz] = tg
            # Die Manhatten Distanz beschreibt eine untere Schranke fuer die Distanz zum Zielknoten
            h = abs(end[0]-tx) + abs(end[1]-ty) + abs(end[2]-tz) * 3
            # Ein Punkt kann mehrmals in der Priority Queue vorkommen, wenn er spaeter ueber einen kuerzeren Weg erreicht wird
            # Deswegen wird der Punkt mit der realen Distanz in die Priority Queue eingefuegt
            heapq.heappush(queue, (tg + h, tg, tx, ty, tz))
            source[(tx, ty, tz)] = (x, y, z, tc)

# Rekonstruktion des Pfades
current = end
path = ""
while current != start:
    x, y, z, c = source[current]
    path = c + path
    current = (x, y, z)

print("Kuerzester Pfad: " + path)
print(f"Laenge: {dist[end[0]][end[1]][end[2]]}")
print(f"Berechnungszeit: {time.time() - t_start}s")