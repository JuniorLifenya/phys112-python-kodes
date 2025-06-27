import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Konstanter
R = 3.0
rho0 = 5e-6
epsilon0 = 8.85e-12
Q_analytic = np.pi * rho0 * R**3 / 3  # Analytisk ladning
################################################################################
################################################################################

# Funksjoner
def electric_field(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    if r < 0.0001:  # Hvis veldig nær origo, unngå problemer med å dele med 0
        return 0.0, 0.0, 0.0
    E_magnitude = (rho0 / epsilon0) * (r/3 - r**2/(4*R)) # Magnituden på feltet
    Ex = E_magnitude * x/r
    Ey = E_magnitude * y/r
    Ez = E_magnitude * z/r
    return Ex, Ey, Ez

def charge_density(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    return rho0 * (1 - r/R) * (r <= R)

################################################################################
################################################################################
# Del C(1)
def calculate_flux(N_theta, N_phi):

    dtheta = np.pi / N_theta
    dphi = 2 * np.pi / N_phi

    flux = 0.0
    for i in range(N_theta):
        theta = (i + 0.5) * dtheta  # Midtpunkt
        for j in range(N_phi):
            phi = (j + 0.5) * dphi

            # Posisjon på kuleflaten
            x = R * np.sin(theta) * np.cos(phi)
            y = R * np.sin(theta) * np.sin(phi)
            z = R * np.cos(theta)
            
            # Felt og normalvektor
            Ex, Ey, Ez = electric_field(x, y, z)
            n_hat = np.array([x, y, z]) / R  # Enhetsnormal
            
            # Flateelement (dA = R² sinθ dθ dφ)
            dA = R**2 * np.sin(theta) * dtheta * dphi
            
            flux += (Ex*n_hat[0] + Ey*n_hat[1] + Ez*n_hat[2]) * dA

    Q_flux = flux * epsilon0  # Gauss' lov: Φ = Q_enclosed / ε₀
    return Q_flux

################################################################################
################################################################################
# Del C(2)
def calculate_charge_volume(N_r, N_theta, N_phi):
    
    dr = R / N_r
    dtheta = np.pi / N_theta
    dphi = 2 * np.pi / N_phi

    Q_vol = 0.0
    for i in range(N_r):
        r = (i + 0.5) * dr  # Midtpunkt
        for j in range(N_theta):
            theta = (j + 0.5) * dtheta
            for k in range(N_phi):
                phi = (k + 0.5) * dphi

                # Volumelement dV = r² sinθ dr dθ dφ
                dV = r**2 * np.sin(theta) * dr * dtheta * dphi
                
                # Kartesiske koordinater
                x = r * np.sin(theta) * np.cos(phi)
                y = r * np.sin(theta) * np.sin(phi)
                z = r * np.cos(theta)
                
                Q_vol += charge_density(x, y, z) * dV
    return Q_vol

################################################################################
################################################################################

# Beregn for en gitt oppløsning (f.eks. 20 segmenter)
segmenter = int(input(" Enter segmenter: "))
Q_flux = calculate_flux(segmenter, segmenter)
Q_vol = calculate_charge_volume(segmenter,segmenter,segmenter)

print(f"Analytisk Q: {Q_analytic:.6e} C \n")
print(f"Fra fluks:   {Q_flux:.6e} C | Feil: {abs(Q_flux - Q_analytic)*100/Q_analytic:.2%}")
print(f"Fra volum:   {Q_vol:.6e} C | Feil: {abs(Q_vol - Q_analytic)*100/Q_analytic:.2%} \n")