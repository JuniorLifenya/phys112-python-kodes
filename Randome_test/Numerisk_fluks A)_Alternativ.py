import numpy as np

# Define the range and step size
x_range = y_range = [-4, 4]  # Define x and y range
step = 100  # Number of points along each axis

# Create a 2D grid for the plane z = 2
x = y = np.linspace(x_range[0], x_range[1], step)
X, Y = np.meshgrid(x, y)
Z = 2 * np.ones_like(X)  # z = 2 for all points


# Define the vector field F(x, y, z)
def F(x, y, z):
    return np.array([2 * x, 7 * y, z])  # Vector field


# Define the normal vector for the plane z = 2
n_hat = np.array([0, 0, -1])  # Normal vector


# Calculate the flux
def calculate_flux(X, Y, Z):
    # Compute the area element (dA)
    dx = dy = (x_range[1] - x_range[0]) / (step - 1)
    dA = dx * dy

    # Compute the vector field at all grid points
    F_verdi = np.array(
        [F(X[i, j], Y[i, j], Z[i, j]) for i in range(step) for j in range(step)]
    )
    F_dot_n = np.dot(F_verdi, n_hat)
    flux = np.sum(F_dot_n) * dA
    return flux


# Compute the flux
flux_value = calculate_flux(X, Y, Z)
print(f"Flux through the plane z = 2: {flux_value:.3}")
