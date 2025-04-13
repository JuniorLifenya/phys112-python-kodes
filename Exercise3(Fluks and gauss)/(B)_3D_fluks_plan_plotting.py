###############################################################################
###############################################################################
import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

###############################################################################

xrange = yrange = zrange = [-4, 4]
step = 10

Xlist = Ylist = Zlist = np.linspace(xrange[0], xrange[1], step)
X, Y, Z = np.meshgrid(Xlist, Ylist, Zlist)
###############################################################################
###############################################################################
##### Defines the vector field ################################################
U = Y / Z
V = -X / Z
w = Z

####################### Plotting av felt i 3D      ############################
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection="3d")

####################### Legger til planet i Z=2 ###############################
X_plane, Y_plane = np.meshgrid(Xlist, Ylist)

z_plane = 2
Z_plane = np.full_like(X_plane, z_plane)

####################### Plot instillinger #####################################
ax.quiver(X, Y, Z, U, V, w, length=1, normalize=True, color="black", alpha=0.7)
ax.plot_surface(X_plane, Y_plane, Z_plane, color="blue", alpha=0.8)
ax.set_title("Plane in 3D vektorfelt")
ax.set_xlabel("X", color="red", alpha=0.7)
ax.set_ylabel("Y", color="red", alpha=0.7)
ax.set_zlabel("Z", color="red", alpha=0.7)
plt.show()
