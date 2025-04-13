import numpy as np
import matplotlib.pyplot as plt

###############################################################################
# Definerer variabler for detaljer

x_range = y_range = [-4, 4]  # Definerer x,y,z aksen
step = 100  # Definer eksakt antall punkter på området
###############################################################################

# Definerer hele X,Y planet
Xlist = Ylist = np.linspace(x_range[0], x_range[1], step)
X, Y = np.meshgrid(Xlist, Ylist)
Z = 2 * np.ones_like(X)


###############################################################################
###############################################################################
# Funksjon for å beregne numerisk fluks
def F(x, y, z):
    return np.array([2 * x, 7 * y, z])


###############################################################################

n_hat = np.array([0, 0, -1])


def calculate_flux(X, Y, Z):
    dx = dy = (x_range[1] - x_range[0]) / (
        step - 1
    )  # Definerer antall intervaller/steg
    dA = dx * dy  # Totale området
    flux = 0
    for i in range(step):
        for j in range(step):
            F_verdi = F(X[i, j], Y[i, j], Z[i, j])
            F_dot_n = np.dot(F_verdi, n_hat)
            flux += (F_dot_n) * dA  # Legger til fluksverdien til totalt fluxet
    return flux


###############################################################################
###############################################################################
# Beregn fluks for ulike antall segmenter

flux_values = calculate_flux(X, Y, Z)

###############################################################################
###############################################################################
# Print resultater
print(f"Flux through the plane z = 2: {flux_values:.3}")
