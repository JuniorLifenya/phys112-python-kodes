###############################################################################
###############################################################################
import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

###############################################################################
# Definerer variabler

xrange = yrange = zrange = [-4, 4]  # Definerer x,y,z aksen
step = 8  # Definer antall punkter på retningsfeltet

###############################################################################
###############################################################################

# Definerer hele x,y planet med steps som antall punkter på dette planet.
Xlist = Ylist = Zlist = np.linspace(xrange[0], xrange[1], step)
X, Y, Z = np.meshgrid(Xlist, Ylist, Zlist)

################ Lister som blir til variabler og funksjoner ##################
# Felt med simpel piler pekende utover
U = X
V = Y
w = Z
################ Plotting av figuren, og projekter til 3D #####################
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection="3d")

###############################################################################

################ Definerer kulen i 3D #########################################

radius = 3  # Kule-radius
kulens_oppløsning = 10
phi = np.linspace(0, np.pi, kulens_oppløsning)  # Polar vinkel
theta = np.linspace(0, 2 * (np.pi), kulens_oppløsning)  # Azimutal vinkel
ø, t = np.meshgrid(phi, theta)

# Convert spherical coordinates to Cartesian coordinates
X_sphere = radius * np.cos(t) * np.sin(ø)
Y_sphere = radius * np.sin(t) * np.sin(ø)
Z_sphere = radius * np.cos(ø)

################ Plot instillinger ############################################
ax.plot_surface(X_sphere, Y_sphere, Z_sphere, color="blue", alpha=1, edgecolor="yellow")
ax.quiver(X, Y, Z, U, V, w, length=1, normalize=True, color="black", alpha=0.9)
ax.set_title(f" {kulens_oppløsning} segment-oppløst Kule i felt")
ax.set_xlabel("X", color="red")
ax.set_ylabel("Y", color="red")
ax.set_zlabel("Z", color="red")
plt.show()
