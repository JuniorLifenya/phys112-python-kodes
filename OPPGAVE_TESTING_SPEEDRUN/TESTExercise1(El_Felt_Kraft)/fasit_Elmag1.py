import numpy as np
import pandas as pd


""" A) """
EPSILON_ZERO = 8.854e-12
K = 1/(4*np.pi*EPSILON_ZERO)

def E(q, x, y):
    """ Returnerer feltstyrken i x- og y-retning i (0,0) fra ladningene """
    dx = 0 - x
    dy = 0 - y

    r = np.sqrt(dx**2 + dy**2)

    Ex = K*(q)/(r**3)*dx
    Ey = K*(q)/(r**3)*dy

    return Ex, Ey


""" B) """
df = pd.read_csv("ladninger.csv")

q = df["charge"].to_numpy()*10**(-9)
x = df["pos_x"].to_numpy()
y = df["pos_y"].to_numpy()


""" C) """
Ex, Ey = E(q, x, y)

Ex_sum = np.sum(Ex)
Ey_sum = np.sum(Ey)
E_sum = np.sqrt(Ex_sum**2 + Ey_sum**2)

print(f"Fx = {Ex_sum:.3e} N")
print(f"Fy = {Ey_sum:.3e} N")
print(f" F = {E_sum:.3e} N")