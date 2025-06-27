import numpy as np
import matplotlib.pyplot as plt
def F(x, y, z):
    return np.array([x**2, y**2, x*y])

def flux_plane(x_range, y_range, N):

    # Areal-element
    dx = (x_range[1] - x_range[0])/(N)
    dy = (y_range[1] - y_range[0])/(N)
    dA = dx*dy

    # Lag grid
    X_venstre = np.linspace(x_range[0], x_range[1]-dx, N)
    Y_venstre = np.linspace(y_range[0], y_range[1]-dy, N)
    X, Y = np.meshgrid(X_venstre, Y_venstre)
    Z = np.full_like(X,2)
    
    # Normalvektor (ut av planet)
    n_hat = np.array([0, 0, -1])
    
    
    
    # Summer fluksen
    total_flux = 0.0
    for i in range(N):
        for j in range(N):
            Fv =F(X[i,j], Y[i,j], Z[i,j])
            total_flux += np.dot(Fv, n_hat) * dA
    return total_flux

########################################################################################
########################################################################################
def flux_plane_midpoint(x_range, y_range, n_cells):
    dx = (x_range[1] - x_range[0]) / n_cells
    dy = (y_range[1] - y_range[0]) / n_cells
    dA = dx * dy

    # Midpoints of cells
    x_mid = np.linspace(x_range[0] + dx/2, x_range[1] - dx/2, n_cells)
    y_mid = np.linspace(y_range[0] + dy/2, y_range[1] - dy/2, n_cells)
    X, Y = np.meshgrid(x_mid, y_mid)
    Z = np.full_like(X, 2)

    n_hat = np.array([0, 0, -1])
    total_flux = 0.0
    for i in range(n_cells):
        for j in range(n_cells):
            Fv = F(X[i, j], Y[i, j], Z[i, j])
            total_flux += np.dot(Fv, n_hat) * dA
    return total_flux


phi_edge = flux_plane(x_range=[0,4], y_range=[0,4], N=500)
phi_mid  = flux_plane_midpoint( x_range=[0,4], y_range=[0,4], n_cells=500)

# Beregnet analytisk løsning for det nye området:
# ∬ -xy dA = - ∫(x fra 0 til 4) ∫(y fra 0 til 4) xy dy dx
# = - ∫[0,4] x dx * ∫[0,4] y dy 
# = - [ (1/2)x² |[0,4] ] * [ (1/2)y² |[0,4] ]
# = - [ (1/2)*16 ] * [ (1/2)*16 ] 
# = - [8] * [8] = -64
analytisk = -64.0

print(f"Analytisk løsning: {analytisk}\n")
print(f"Venstre sampling:     {phi_edge:.3f} |Feilestimat {abs((phi_edge-analytisk)*100/analytisk):2%}")
print(f"Midpunkt sampling: {phi_mid:.3f}|Feilestimat {abs((phi_mid-analytisk)*100/analytisk):2%} \n")

