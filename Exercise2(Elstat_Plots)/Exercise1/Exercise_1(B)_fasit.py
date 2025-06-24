import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###########################################################################################################

# Definerer variabler
k = 1  # Because we are using the gauss CGS system where Q is in electrostatic unit
xrange = [-12, 14]  # Definerer x aksen
yrange = [-12, 14]  # Definerer y aksen
step = 200  # Definer antall punkter på retnings-feltet
q = np.array([[1, 2, 3]]) # The format of our point like charge. 
###########################################################################################################
###########################################################################################################

# Define the whole x,y plane with steps as amount of points in it.
Xlist = np.linspace(xrange[0], xrange[1], step)
Ylist = np.linspace(yrange[0], yrange[1], step)
X, Y = np.meshgrid(Xlist, Ylist)


# Defines the position vector and electric fields for each point in the plane


def addpointcharge2D(Ex, Ey, X, Y, q): # Function to add a point charge to the electric field
    r2 = k * ((X - q[0]) ** 2 + (Y - q[1]) ** 2)
    Ex += k * (q[2] * (X - q[0])) / (r2) ** (3 / 2)
    Ey += k * (q[2] * (Y - q[1]) / (r2) ** (3 / 2))
    return Ex, Ey


# Starts the electric field components as empty arrays with the same shape as X and Y
Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)

for i in range(len(q)):
    addpointcharge2D(Ex, Ey, X, Y, q[i])
E_log = np.log((Ex**2 + Ey**2) ** 0.5)


################### Instillinger for retningsfeltet######################################

fig, ax = plt.subplots()
ax.streamplot(
    X, Y, Ex, Ey, color="red", linewidth=1, density=4, arrowstyle="->", arrowsize=1
)


# Endrer hvordan vi ser på ladningen med [(zoom), indre radius, ytre radius]
levels = np.linspace(-2.5, 4, 300)

################### Instillinger for ladning i feltet####################################
# Definerer vår fargebar på sida, sammen med selve ladningens intensitet
cb = ax.contourf(X, Y, E_log, levels=levels, cmap="turbo_r")

print("Max E:", np.max(E_log))
plt.xlabel("X-akse")
plt.ylabel("Y-akse")
fig.colorbar(cb)
plt.title("Intensitets plot for en positiv ladning")
plt.show()
