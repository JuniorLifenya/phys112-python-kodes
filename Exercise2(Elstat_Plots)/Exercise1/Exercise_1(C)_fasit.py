import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###########################################################################################################

# Define our changeable variables
k = 1  # Because we are using the gauss CGS system where Q is in electrostatic unit
xrange = [-12, 14]  # This is our x axis
yrange = [-13, 14]  # This is our y axis
step = 200  # Define number of points to consider on the direction field
Q = pd.read_csv("ladninger.csv")
q_name = Q["name"].to_numpy()
q_v = Q["charge"].to_list()
pos_x = Q["pos_x"].to_list()
pos_y = Q["pos_y"].to_list()

q = np.array([[(pos_x[i]), (pos_y[i]), (q_v[i]) * 10**9] for i in range(0, 7)])

# q = np.array([[1, 1, -3], [3, 3, 4.21], [6, 1, -3], [3, -1, 4.21]])
# qrange = [-3, 3]  # Code for making a random amount of charges
print(q)

###########################################################################################################
###########################################################################################################

# Define the whole x,y plane with steps as amount of points in it.
Xlist = np.linspace(xrange[0], xrange[1], step)
Ylist = np.linspace(yrange[0], yrange[1], step)
X, Y = np.meshgrid(Xlist, Ylist)  # Creates the actual x,y-grid needed for plotting

# Alternativ code for random charges
# qmin = [xrange[0], xrange[0], qrange[0]]
# qmax = [xrange[1], xrange[1], qrange[1]]
# q = np.random.uniform(low=qmin, high=qmax, size=(4, 3))  # An array containing info of charges that will be created randomly ()

###########################################################################################################
###########################################################################################################


# Create a function for the electric field and its components given an array of the charges info
def addpointcharge2D(Ex, Ey, X, Y, q):
    r2 = k * ((X - (q[0])) ** 2 + (Y - (q[1])) ** 2)
    Ex += k * ((q[2]) * (X - (q[0]))) / (r2) ** (3 / 2)
    Ey += k * ((q[2]) * (Y - (q[1])) / (r2) ** (3 / 2))
    return (Ex), (Ey)


# Creates some empty arrays where we will have our X,Y grid
Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)

# Define the actual total electric field. We use the logarithm as it is too large
for i in range(len(q)):
    addpointcharge2D(Ex, Ey, X, Y, q[i])
    E_log = np.log((Ex**2 + Ey**2) ** 0.5)

###########################################################################################################

# Definerer det vi skal plotte. Og siden vi skal kombinerer figur og akser så bruker vi denne
fig, ax = plt.subplots()

# Instillinger for bare vår strømplot
ax.streamplot(
    X, Y, Ex, Ey, color="black", linewidth=1.5, density=3, arrowstyle="->", arrowsize=1
)
levels = np.linspace(-2.5, 5, 150)
# Edits the contour plots characteristics (intensity radius, point-like intensity, intensity points)

#################Definerer our colorbar på sida av plotens############################
cb = ax.contourf(X, Y, E_log, levels=levels, cmap="turbo")
fig.colorbar(cb)

plt.xlabel("X-coordinates")
plt.ylabel("Y-coordinates")
plt.title("Intensitets plot for flere ladninger")
plt.show()
