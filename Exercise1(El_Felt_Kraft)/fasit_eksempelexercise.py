import numpy as np
import math as m
import pandas as pd

Q = pd.read_csv("ladninger.csv")
# Definer variabler som array-lister fra filen#
q_name = Q["name"].tolist()
q_v = Q["charge"].tolist()
pos_x = Q["pos_x"].tolist()
pos_y = Q["pos_y"].tolist()


# Definerer funksjonen, slik som ønsket i oppgaven
def el_Force_108(x, y, q):
    k = 8.899e9
    r_102_vector = (
        (x[1] - x[9]),
        (y[1] - y[9]),
    )

    # Bruker np.linalg.norm til å definere lengden på vektoren
    r = np.linalg.norm(r_102_vector)
    print(
        f"r_{10}2_vektor: {r_102_vector}\nMagnituden kvadrert: {r**2:.3} m",
    )
    # Definerer vinkelen vår ved bruk av m.atan2(tar inn to verdier) fra matte biblioteket
    ø = m.atan2(r_102_vector[1], r_102_vector[0])
    print(f"Vinkel i grader: {ø*180/np.pi:.3} \n ")

    # Definerer kreftene våre ved å dekomponere og bruke vinkelen
    F_x = k * ((abs(q[1] * (q[9])))) / (r**2) * np.cos(ø)
    F_y = k * ((abs(q[1] * (q[9])))) / (r**2) * np.sin(ø)
    F = m.sqrt(F_x**2 + F_y**2)

    # Returnerer verdiene vi er ute etter med riktig desimaler
    return f"Fx: {F_x:.2e} N , Fy: {F_y:.2e} N , Total F: {F:.3} N \n"


print(el_Force_108(pos_x, pos_y, q_v))
