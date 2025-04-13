import numpy as np
import math as m
import pandas as pd

# Leser filen og definerer variabler som lister #
Q = pd.read_csv("ladninger.csv")
q_name = Q["name"].to_numpy()
q_v = Q["charge"].to_numpy()
pos_x = Q["pos_x"].to_numpy()
pos_y = Q["pos_y"].to_numpy()
k = 8.899e9


# Funksjon som tar info fra csv-filen og beregner elektrisk-felt
def electric_forces__vector(x, y, q):
    E_x = 0
    E_y = 0
    r_i0_hat = 0
    for i in range(0, 12):
        if i == 6:  # Vil ikke ha origo med
            continue
        # Lager posisjons-vektor mellom qi og Origo
        r_i0_vector = (
            (0 - int(x[i])),
            (0 - int(y[i])),
        )
        # Magnituden til r-vektoren kvadrert
        r_i0 = np.linalg.norm(r_i0_vector)
        print(f"{r_i0_vector}, {r_i0:.3}")
        # Definerer vinkelen i grader
        ø = m.atan2(r_i0_vector[1], r_i0_vector[0])

        for t in range(0, 12):
            if r_i0 == 0:
                continue
            r_i0_hat += np.array(((r_i0_vector / r_i0)))
            # Definerer og printer ut kreftene vi er ute etter
            E_x += (k * ((abs((q[t])))) / (r_i0**2)) * np.cos(ø)
            E_y += (k * ((abs((q[t])))) / (r_i0**2)) * np.sin(ø)

    E = m.sqrt(E_x**2 + E_y**2)

    # Formatere resultatet til riktig desimaltall og enhet
    return f"Ex: {E_x:.2e}N [i] , Ey: {E_y:.2e}N [j], Total E: {E:.2e}N {r_i0_hat}"


# Test the function with positions and charges from the file
print(electric_forces__vector(pos_x, pos_y, q_v))
print(
    f"Vi ser at ladning q6 befinner seg allerede i origo, så i teorien lager den et uendelig elektrisk feltstyrke der"
)
