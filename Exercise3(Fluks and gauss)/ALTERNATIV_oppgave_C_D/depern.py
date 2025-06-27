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

################################################################################
################################################################################

# ALTRENATIV METODE: Beregn for en gitt oppløsning (f.eks. 20 segmenter) #######

################################################################################
################################################################################

import math
import numpy as np

# Fysiske konstanter
R = 3.0           # Kulens radius [m]
rho0 = 5e-6       # Ladningstetthet [C/m³]
epsilon0 = 8.85e-12  # Vakuumpermittivitet [C²/N·m²]

def elektrisk_felt(x, y, z):
    """Beregner elektrisk felt for en gitt posisjon"""
    # Beregn avstand fra origo
    r = math.sqrt(x**2 + y**2 + z**2)
    
    # Spesiell håndtering for origo (r=0)
    if r < 0.000001:  # Veldig liten verdi istedenfor 0
        return 0.0, 0.0, 0.0
    
    # Beregn størrelsen på feltet
    E_storrelse = (rho0 / epsilon0) * (r/3 - r**2/(4*R))
    
    # Beregn retning (enhetsvektor)
    retning_x = x / r
    retning_y = y / r
    retning_z = z / r
    
    # Beregn feltkomponenter
    Ex = E_storrelse * retning_x
    Ey = E_storrelse * retning_y
    Ez = E_storrelse * retning_z
    
    return Ex, Ey, Ez

def ladningstetthet(x, y, z):
    """Beregner ladningstetthet for en gitt posisjon"""
    r = math.sqrt(x**2 + y**2 + z**2)
    if r > R:
        return 0.0  # Utenfor kulen
    return rho0 * (1 - r/R)

def beregn_fluks(antall_theta, antall_phi):
    """Beregner fluksen gjennom kulen ved numerisk integrasjon"""
    fluks = 0.0
    dtheta = math.pi / antall_theta
    dphi = 2 * math.pi / antall_phi
    
    for i in range(antall_theta):
        theta = (i + 0.5) * dtheta  # Midt i intervallet
        for j in range(antall_phi):
            phi = (j + 0.5) * dphi
            
            # Posisjon på kuleoverflaten
            x = R * math.sin(theta) * math.cos(phi)
            y = R * math.sin(theta) * math.sin(phi)
            z = R * math.cos(theta)
            
            # Beregn feltet
            Ex, Ey, Ez = elektrisk_felt(x, y, z)
            
            # Beregn normalvektor (retning ut fra kulen)
            n_x = x / R
            n_y = y / R
            n_z = z / R
            
            # Beregn flateelement
            dA = R**2 * math.sin(theta) * dtheta * dphi
            
            # Legg til bidraget til fluksen
            fluks += (Ex * n_x + Ey * n_y + Ez * n_z) * dA
    
    return fluks

def beregn_ladning(antall_r, antall_theta, antall_phi):
    """Beregner total ladning ved numerisk integrasjon"""
    ladning = 0.0
    dr = R / antall_r
    dtheta = math.pi / antall_theta
    dphi = 2 * math.pi / antall_phi
    
    for i in range(antall_r):
        r = (i + 0.5) * dr  # Midt i radialintervallet
        for j in range(antall_theta):
            theta = (j + 0.5) * dtheta
            for k in range(antall_phi):
                phi = (k + 0.5) * dphi
                
                # Beregn volumselement
                dV = r**2 * math.sin(theta) * dr * dtheta * dphi
                
                # Posisjon i kartesiske koordinater
                x = r * math.sin(theta) * math.cos(phi)
                y = r * math.sin(theta) * math.sin(phi)
                z = r * math.cos(theta)
                
                # Legg til ladningen i dette volumselementet
                ladning += ladningstetthet(x, y, z) * dV
    
    return ladning

# Beregn analytisk ladning for sammenligning
analytisk_ladning = (math.pi * rho0 * R**3) / 3

# Beregn med numeriske metoder
fluks = beregn_fluks(segmenter, segmenter)
ladning_fra_fluks = fluks * epsilon0  # Fra Gauss' lov: Φ = Q/ε₀

ladning_fra_volum = beregn_ladning(segmenter,segmenter,segmenter)

print(f"Analytisk ladning  {analytisk_ladning:.6e}", "C")
print(f"Ladning fra fluksberegning {ladning_fra_fluks:.6e}", "C")
print(f"Ladning fra volumintegrasjon {ladning_fra_volum:.6e}", "C")

#########################################################################
#########################################################################
#D nøyaktighet for segmenter

resolutions = [5, 10, 50]
errors_flux = []
errors_vol = []

for N in resolutions:
    Q_flux = calculate_flux(N, N)
    Q_vol = calculate_charge_volume(N, N, N)
    
    errors_flux.append(abs(Q_flux - Q_analytic) / Q_analytic)
    errors_vol.append(abs(Q_vol - Q_analytic) / Q_analytic)

# Plot feilutvikling
plt.figure(figsize=(10, 6))
plt.loglog(resolutions, errors_flux, 'o-', label='Fluksmetode')
plt.loglog(resolutions, errors_vol, 's-', label='Volummetode')
plt.xlabel('Antall segmenter')
plt.ylabel('Relativ feil')
plt.title('Konvergens av numeriske metoder')
plt.legend()
plt.grid(True, which="both", ls="-")
plt.show()