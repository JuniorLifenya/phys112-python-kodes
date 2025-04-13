###############################################################################
###############################################################################
import numpy as np
import math as m
import pandas as pd

Q = pd.read_csv("ladninger.csv")
# Definer variabler som array-lister fra filen#
q_name = Q["name"].tolist()
q_v = Q["charge"].tolist()
pos_x = Q["pos_x"].tolist()
pos_y = Q["pos_y"].tolist()
k = 8.899e9


# Funksjon som tar info fra csv-filen og beregner elektrisk-felt

F_størst = []
Ø_størst = []


def electric_forces__vector(x, y, q):
    F_2x_tot = 0
    F_2y_tot = 0

    for i in range(0, 12):
        if i == 1:  # Vil ikke ha ladningen q2 sin kraft på seg selv
            continue

        # Lager posisjons-vektor mellom qi-->q2
        r_i2_vector = (
            (x[1] - x[i]),
            (y[1] - y[i]),
        )

        # Magnituden til r-vektoren kvadrert
        r_i2 = np.linalg.norm(r_i2_vector)
        # Printer vektoren og magnituden kvadrert med riktig formatering

        # Definerer vinkelen mellom r_i2_ og x-aksen( vanlige vinkler) i grader
        v = m.atan2(r_i2_vector[1], r_i2_vector[0])
        # Definer vinkelen mellom y-aksen og r_i2_vektor
        ø = m.atan2(r_i2_vector[0], r_i2_vector[1])

        # Definerer kreftene som vi skal bruke
        F_2x = (k * ((abs(q[1] * (q[i])))) / (r_i2**2)) * np.cos(v)
        F_2y = (k * ((abs(q[1] * (q[i])))) / (r_i2**2)) * np.sin(v)

        # Summerer opp kreftene i y og x retning for hver ladning i
        F_2x_tot += F_2x
        F_2y_tot += F_2y

        # Lister for størst kraft og vinkel mellom r_i2_vektor og y-aksen i grader
        F_størst.append(m.sqrt(F_2x**2 + F_2y**2))
        Ø_størst.append(ø * 180 / np.pi)
    # Formatere resultatet til riktig desimaltall og enhet
    F_tot = m.sqrt(F_2x_tot**2 + F_2y_tot**2)
    return f"Fx: {F_2x_tot:.2e} N, Fy: {F_2y_tot:.2e} N, F_tot: {F_tot:.2e} N, \n"


# Tester funksjonen ved å sette inn relevant informasjon fra csv filen
print(electric_forces__vector(pos_x, pos_y, q_v))

print(
    f" Største kraft på q2 er fra q({F_størst.index(max(F_størst))+1}) = {max(F_størst):.3} N"
)
print(
    f" Største vinkel mellom r_i2_vector og y-aksen :{max([i for i in Ø_størst if i != 90]):.3} grader",
    "\n",
)
