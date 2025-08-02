import numpy as np 
import matplotlib.pyplot as plt 
import math as m
import pandas as pd

#######################################################################################################
#######################################################################################################

epsilon_0 = 8.85e-12
K = 1/(4 * np.pi * epsilon_0)

df = pd.read_csv("ladninger.csv")
q_C = df["charge"].to_numpy()*1e9 # List of the charge number
q_xpos = df["pos_x"].to_numpy() # List of all charges 
q_ypos = df["pos_y"].to_numpy()

# The total field strength in x direction is Ex = K(Qq)/r^2cos(theta) , sine for y direction 
# I want to use that the theta will be the arctan of y/x positions
def E_loop(q,x,y):
    Ex = 0 
    Ey = 0 
    for i in range (len(q)):
        qi , xi , yi = q[i] , x[i] , y[i]
        r0 = [0,0] # To avoid directly deviding by 0 
        
        ri0 = np.sqrt((r0[0]-xi)**2 + (r0[1]-yi)**2) + 1e-10 # Include a small epsilon here 
        øi = np.arctan2(-yi,-xi) # arctan2 takes two arguments, and dont accumalte charges with +=

        Ex += K*np.cos(øi)* (qi)/(ri0**3)
        Ey += K*np.sin(øi)* (qi)/(ri0**3)
    Etot = np.sqrt((Ex)**2+ (Ey)**2)

    return f" Ex = {np.sum(Ex):.3e} N/C \n Ey = {np.sum(Ey):.3e} N/C \n |E| = {np.sum(Etot):.3e} N/C \n"

print(E_loop(q_C,q_xpos,q_ypos))
###############################################################################################

import numpy as np
import pandas as pd

# Konstanter
ε0 = 8.854e-12  # Permittivitet i vakuum (F/m)
K  = 1 / (4 * np.pi * ε0)

# Les inn CSV-filen
df = pd.read_csv('ladninger.csv')

# Ekstraher og konverter til SI-enheter
q = df["charge"].to_numpy()*1e-9  # nC → C
x = df["pos_x"].to_numpy()          # meter
y = df["pos_y"].to_numpy()          # meter

# Vektor fra hver ladning til origo (0,0)
dx = -x
dy = -y
r  = np.hypot(dx, dy) + 1e-12       # avstand, med liten epsilon for å unngå null

# Beregn feltkomponentene
Ex = np.sum(K * q * dx / r**3)
Ey = np.sum(K * q * dy / r**3)
E_magnitude = np.hypot(Ex, Ey)

# Skriv ut resultatene
print(f"Ex = {Ex:.3e} N/C")
print(f"Ey = {Ey:.3e} N/C")
print(f"|E| = {E_magnitude:.3e} N/C \n")

################################################################################################

import numpy as np
import pandas as pd

epsilon_0 = 8.854e-12
K = 1 / (4 * np.pi * epsilon_0)

df = pd.read_csv("ladninger.csv")
q_C = df["charge"].to_numpy() *1e-9 # C to nC
q_xpos = df["pos_x"].to_numpy()
q_ypos = df["pos_y"].to_numpy()

def calculate_electric_field(q, x, y):
    Ex = 0.0
    Ey = 0.0
    for i in range(len(q)):
        qi = q[i]
        xi = x[i]
        yi = y[i]
        
        # Avstand fra ladning til origo (0,0)
        dx = -xi  # Fra ladning til origo i x
        dy = -yi  # Fra ladning til origo i y
        r_squared = dx**2 + dy**2
        
        # Hopp over ladninger ved origo
        if r_squared < 1e-12:
            continue
            
        r = np.sqrt(r_squared)
        
        # Enhetsvektor FRA ladningen TIL origo
        ux = dx / r
        uy = dy / r
        
        # Feltstyrke fra denne ladningen
        E_mag = K * qi / r_squared
        Ex += E_mag * ux
        Ey += E_mag * uy
        
    Etot = np.sqrt(Ex**2 + Ey**2)
    return Ex, Ey, Etot

Ex, Ey, E_total = calculate_electric_field(q_C, q_xpos, q_ypos)
print(f"Ex = {Ex:.3e} N/C")
print(f"Ey = {Ey:.3e} N/C")
print(f"E = {E_total:.3e} N/C")

##############################################################################################

