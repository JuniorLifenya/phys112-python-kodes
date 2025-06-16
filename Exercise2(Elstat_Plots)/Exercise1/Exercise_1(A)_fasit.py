###############################################################################
###############################################################################
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

###############################################################################
###############################################################################

# Definerer variabler
xrange = [-13, 13]  # Definerer x aksen
yrange = [-13, 13]  # Definerer y aksen
step = 200  # Definer antall punkter på retningsfeltet

###############################################################################
###############################################################################


# Definerer hele x,y planet med steps som antall punkter på planet.
Xlist = np.linspace(xrange[0], xrange[1], step)
Ylist = np.linspace(yrange[0], yrange[1], step)
X, Y = np.meshgrid(Xlist, Ylist)


################ Våre funksjoner som skal plottes  ############

U = 2*X
V = -2*Y 
f = X**2 - Y**2

################ Plotting av retningsfeltet(ax1) og nivåkurve(ax2) ##############
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))


Nivåkurve = ax2.contourf(X, Y, f)

Retningsfelt = ax1.streamplot(
    X, Y, U, V, color="black", linewidth=1, density=3, arrowstyle="->", arrowsize=1
)

##################################################################################
##################################################################################

################ Plot instillinger #################
ax1.set_title("Retningsfelt")
ax2.set_title("Nivåkurve")
fig.supxlabel("X-akse")
fig.supylabel("Y-akse")
plt.show()

##################################################################################
##################################################################################