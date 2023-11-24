# Aufgabe 5: Stadtfuerung

import sys
import time

t_start = time.time()

class Tourpunkt:
    def __init__(self, l, t, e, p):
        self.ort, self.zeit, self.essentiel, self.position = l, int(t), e == "X", int(p)

with open(sys.argv[1]) as file:
    n = int(file.readline())
    tour = [Tourpunkt(*file.readline().strip().split(',')) for _ in range(n)]
    first_essentiel = next((i for i in range(n) if tour[i].essentiel), 0)

class Teiltour:
    def __init__(self, s, e, w, b):
        self.start, self.end, self.weight, self.before, self.m = s, e, w, b, 0

# Identifizieren der Teiltouren
q = {} # Speichert das letzte Vorkommen eines Ortes nach einem essentiellen Punkt
teiltouren = [Teiltour(0,0,0,0)]
for index in range(first_essentiel,first_essentiel+n+1):
    t = tour[index%n]
    # Wenn der Ort schon einmal vorkam, dann ist er der Endpunkt einer Teiltour
    if t.ort in q:
        last_occurence, n_intervals_before = q[t.ort]
        start = tour[last_occurence]
        # Berechnen der Ersparnis
        saving = t.position - start.position if t.position >= start.position else tour[-1].position - start.position + t.position
        if saving != 0: teiltouren.append(Teiltour(last_occurence, index%n, saving, n_intervals_before))
    if t.essentiel: q = {}
    # Speichern des letzten Vorkommens eines Ortes und die Anzahl der Teiltouren die vor dem Starpunkt enden
    q[t.ort] = (index%n, len(teiltouren) - 1)

# Berechnen der optimalen Lösung
for i in range(1, len(teiltouren)):
    t = teiltouren[i]
    t.m = max(teiltouren[i-1].m, teiltouren[t.before].m + teiltouren[i].weight)

# Rückverfolgen der optimalen Lösung
L = [] # Liste der Teiltouren, die in der optimalen Lösung enthalten sind
i = len(teiltouren) - 1
while i > 0:
    t = teiltouren[i]
    if t.weight + teiltouren[t.before].m >= teiltouren[i-1].m:
        L.append(t)
        i = t.before
    else:
        i -= 1

# Kürzen der Tour
in_tour = [True] * n # Speichert, ob ein Punkt in der Tour enthalten ist
saving = [0] * n # Speichert die Ersparnis beim Endpunkt einer Teiltour
for t in L:
    if t.end > t.start:
        in_tour[t.start+1:t.end] = [False] * (t.end - (t.start + 1))
        saving[t.end] = t.weight
    else:
        in_tour[t.start+1:] = [False] * (n - (t.start + 1))
        in_tour[:t.end] = [False] * t.end
        saving[t.end] = tour[t.end].position

# Ausgabe der neuen Tour
s = 0
l = 0
for i in range(n):
    if in_tour[i]:
        s += saving[i]
        l = tour[i].position - s
        print(f'{tour[i].ort},{tour[i].zeit},{"X" if tour[i].essentiel else " "},{tour[i].position-s}')
print(f"Laenge der alten Tour: {tour[-1].position}")
print(f"Laenge der neuen Tour: {l}")
print(f"Zeit: {time.time() - t_start}s")