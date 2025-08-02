import numpy as np
import pandas as pd


""" A) """
EPSILON_ZERO = 8.854e-12
K = 1/(4*np.pi*EPSILON_ZERO)

def E(q, x, y):
    """ Returnerer feltstyrken i x- og y-retning i (0,0) fra ladningene """
    dx = 0 - x
    dy = 0 - y

    r = np.sqrt(dx**2 + dy**2) + 1e-10 # Unngå dele på 0 

    Ex = K*(q)/(r**3)*dx
    Ey = K*(q)/(r**3)*dy

    return Ex, Ey


""" B) """
df = pd.read_csv("ladninger.csv")

q = df["charge"].to_numpy()*1e-9
x = df["pos_x"].to_numpy()
y = df["pos_y"].to_numpy()


""" C) """
Ex, Ey = E(q, x, y)

Ex_sum = np.sum(Ex)
Ey_sum = np.sum(Ey)
E_sum = np.sqrt(Ex_sum**2 + Ey_sum**2)

print(f"Ex = {Ex_sum:.3e} N/C") #FIX
print(f"Ey = {Ey_sum:.3e} N/C")
print(f" |E| = {E_sum:.3e} N/C \n")
#################################################################################################
import math

# Coulombs konstant
k = 8.987e9  # N·m^2/C^2

# Liste over ladninger og posisjoner
charges = [
    {"charge": -3e-9, "pos_x": 1, "pos_y": 1},
    {"charge": 4.21e-9, "pos_x": 3, "pos_y": 3},
    {"charge": -3e-9, "pos_x": 5, "pos_y": 1},
    {"charge": 4.21e-9, "pos_x": 3, "pos_y": -1},
    {"charge": 4e-9, "pos_x": 3, "pos_y": 1},
    {"charge": 4.4e-9, "pos_x": 2, "pos_y": 2},
    {"charge": 2e-9, "pos_x": -1, "pos_y": 1},
    {"charge": -6e-9, "pos_x": -3, "pos_y": 3},
    {"charge": 2.5e-9, "pos_x": -5, "pos_y": 1},
    {"charge": 7e-9, "pos_x": -3, "pos_y": -1},
    {"charge": 1.1e-9, "pos_x": 0, "pos_y": 3},
    {"charge": 2.17e-9, "pos_x": 0, "pos_y": -3},
]

# Initialiser totalfeltet
E_x_total = 0
E_y_total = 0

# Beregn bidrag fra hver ladning
for charge in charges:
    q = charge["charge"]*1e-9
    x = charge["pos_x"]
    y = charge["pos_y"]
    
    # Avstand til origo
    r = math.sqrt(x**2 + y**2)
    
    # Elektrisk feltstyrke
    E_i = k * q / (r**2)
    
    # Enhetsvektor komponenter
    r_hat_x = -x / r
    r_hat_y = -y / r
    
    # Komponenter av feltet
    E_i_x = E_i * r_hat_x
    E_i_y = E_i * r_hat_y
    
    # Legg til i totalen
    E_x_total += E_i_x
    E_y_total += E_i_y

# Beregn magnituden
E_magnitude = math.sqrt(E_x_total**2 + E_y_total**2)

# Print resultatene
print(f"Ex = {E_x_total:.3e} N/C")
print(f"Ey = {E_y_total:.3e} N/C")
print(f" |E| = {E_magnitude:.3e} N/C")