# Aufgabe 4: Nandu

import sys
import time

f = open(sys.argv[1])
x, y = map(int, f.readline().split())

# Eine Zeile wird als Ganzzahl gespeichert, jedes Bit repräsentiert ein Feld
assign_bits = lambda n, i, b: n | (1 << i) | (1 << i+1) if b else n & ~(1 << i) & ~(1 << i+1) 
get_bit = lambda n, i: (n >> i) & 1

t = time.time()

# Array mit den Indizes der Q-Variablen
z = [i for i, e in enumerate(f.readline().split()) if e.startswith("Q")]
# Erstellen aller möglichen Kombinationen der Taschenlampen
s = []
for i in range(2**len(z)):
    e = 0
    for j in range(len(z)):
        e |= ((i >> j) & 1) << z[j]
    s.append(e)

i, j = 0, 2
while j < y:
    while i < x:
        c = f.read(1)
        while c == " " or c == "\n":
            c = f.read(1)
        # Da das Licht nicht ohne Baustein wandern kann, wird das Feld dunkel
        if c == 'X':
            s = [e & ~(1 << i) for e in s]
            i += 1
            continue
        # Weisser Baustein
        elif c == 'W':
            s[:] = map(lambda e: assign_bits(e, i, not (get_bit(e, i) and get_bit(e, i+1))), s)
        # Roter Baustein
        elif c == 'r':
            s[:] = map(lambda e: assign_bits(e, i, not get_bit(e, i+1)), s)
        elif c == 'R':
            s[:] = map(lambda e: assign_bits(e, i, not get_bit(e, i)), s)
        # Beim blauen Baustein veraendert sich nicht, das Licht wird weitergegeben
        f.read(3)
        i += 2
    i = 0
    j += 1

f.readline()
# Array mit den Indizes der L-Variablen
k = [i for i, e in enumerate(f.readline().split()) if e.startswith("L")]
# Ausgabe der Wahrheitstabelle
print("".join([f"Q{i+1}|" for i in range(len(z))]) + "|" + "".join([f"L{i+1}|" for i in range(len(k))]))
for index, e in enumerate(s):
    print("".join([f"{get_bit(index, i)} |" for i in range(len(z))]) + "|" + "".join([f"{get_bit(e, k[i])} |" for i in range(len(k))]))

print(f"Berechngszeit: {time.time() - t}")