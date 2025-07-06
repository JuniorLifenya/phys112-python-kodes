import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Fysiske konstanter
q = 1.6e-19  # Elementærladning [C]
m = 1.67e-27  # Protonmasse [kg]
mu_0 = 4 * np.pi * 1e-7  # Permeabilitet i vakuum [T·m/A]

## Del A: Konstant magnetfelt (analytisk løsning)
def analytisk_sirkelbevegelse(t, q, m, B, v0, r0):
    """
    Beregner analytisk posisjon for partikkel i konstant B-felt
    
    Args:
        t: Tid [s]
        q: Ladning [C]
        m: Masse [kg]
        B: Magnetfelt i z-retning [T]
        v0: Initial hastighet i xy-planet [m/s]
        r0: Startposisjon [m]
    
    Returns:
        Posisjon som numpy array [x, y, z]
    """
    omega = abs(q) * B / m
    v_perp = np.linalg.norm(v0[:2])  # Hastighet vinkelrett på B-felt
    R = v_perp / omega
    
    # Beregn vinkelen
    theta = omega * t
    
    # Beregn posisjon (sirkelbane i xy-planet)
    x = R * np.sin(theta) + r0[0]
    y = R * (1 - np.cos(theta)) + r0[1]  # Justert for å starte i origo
    z = r0[2]
    
    return np.array([x, y, z])

# Parametere for simulering
B_z = 0.5  # Magnetfeltstyrke [T]
v0 = np.array([1e6, 0, 0])  # Initialhastighet [m/s]
r0 = np.array([0, 0, 0])  # Startposisjon [m]
t_max = 10e-6  # Simulasjonstid [s] (10 mikrosekunder)
dt = 1e-8  # Tidssteg [s]

# Beregn analytisk bane
t_analytisk = np.linspace(0, t_max, 500)
bane_analytisk = np.array([analytisk_sirkelbevegelse(t, q, m, B_z, v0, r0) for t in t_analytisk])

# Plott resultat
plt.figure(figsize=(8, 6))
plt.plot(bane_analytisk[:, 0], bane_analytisk[:, 1], 'b-', label='Analytisk løsning')
plt.xlabel('x [m]', fontsize=12)
plt.ylabel('y [m]', fontsize=12)
plt.title('Protonbane i konstant magnetfelt', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axis('equal')
plt.legend()
plt.show()

## Del B: Numerisk simulering med Lorentz-kraften
def simuler_bane(q, m, B_funksjon, r0, v0, t_max, dt):
    """
    Simulerer partikkelbane numerisk
    
    Args:
        q: Ladning [C]
        m: Masse [kg]
        B_funksjon: Funksjon som returnerer B-felt ved posisjon (x,y,z)
        r0: Startposisjon [m]
        v0: Starthastighet [m/s]
        t_max: Simulasjonstid [s]
        dt: Tidssteg [s]
    
    Returns:
        t_verdier: Tidsverdier
        posisjoner: Posisjoner ved hvert tidssteg
        hastigheter: Hastigheter ved hvert tidssteg
    """
    antall_steg = int(t_max / dt)
    t_verdier = np.linspace(0, t_max, antall_steg)
    posisjoner = np.zeros((antall_steg, 3))
    hastigheter = np.zeros((antall_steg, 3))
    
    posisjoner[0] = r0
    hastigheter[0] = v0
    
    for i in range(1, antall_steg):
        # Beregn akselerasjon fra Lorentz-kraft
        B = B_funksjon(posisjoner[i-1])
        a = (q / m) * np.cross(hastigheter[i-1], B)
        
        # Oppdater hastighet (Euler-Cromer)
        hastigheter[i] = hastigheter[i-1] + a * dt
        posisjoner[i] = posisjoner[i-1] + hastigheter[i] * dt
        
    return t_verdier, posisjoner, hastigheter

# Konstant B-felt funksjon
def konstant_B(r, B0=0.5):
    return np.array([0, 0, B0])

# Kjør numerisk simulering
t, pos_num, v_num = simuler_bane(q, m, konstant_B, r0, v0, t_max, dt)

# Sammenlign med analytisk løsning
plt.figure(figsize=(10, 8))
plt.plot(bane_analytisk[:, 0], bane_analytisk[:, 1], 'b-', label='Analytisk løsning')
plt.plot(pos_num[:, 0], pos_num[:, 1], 'r--', label='Numerisk løsning')
plt.xlabel('x [m]', fontsize=12)
plt.ylabel('y [m]', fontsize=12)
plt.title('Sammenligning av analytisk og numerisk løsning', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axis('equal')
plt.legend()
plt.show()

# Feilanalyse
feil = np.linalg.norm(pos_num[-1] - bane_analytisk[-1])
print(f"Posisjonsfeil ved t = {t_max:.1e} s: {feil:.4e} m")

## Del C: Varierende magnetfelt
def varierende_B(r, B0=0.5, k=0.1):
    """
    Magnetfelt med lineær avhengighet av x
    """
    x, y, z = r
    return np.array([0, 0, B0 * (1 + k * x)])

# Simuler for ulike k-verdier
k_verdier = [0, 0.1, -0.1]
farger = ['b', 'g', 'r']

plt.figure(figsize=(10, 8))
for k, farge in zip(k_verdier, farger):
    def B_func(r):
        return varierende_B(r, B0=B_z, k=k)
    
    t, pos, v = simuler_bane(q, m, B_func, r0, v0, t_max, dt)
    plt.plot(pos[:, 0], pos[:, 1], farge + '-', label=f'k = {k}')

plt.xlabel('x [m]', fontsize=12)
plt.ylabel('y [m]', fontsize=12)
plt.title('Partikkelbaner for varierende magnetfelt', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()

## Del D: Visualisering i 2D og 3D
def animer_2d_bane(posisjoner, lagre_sti="partikkel_2d.gif"):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(np.min(posisjoner[:,0])-0.1, np.max(posisjoner[:,0])+0.1)
    ax.set_ylim(np.min(posisjoner[:,1])-0.1, np.max(posisjoner[:,1])+0.1)
    ax.set_xlabel("x [m]", fontsize=12)
    ax.set_ylabel("y [m]", fontsize=12)
    ax.grid(True)
    ax.set_title('2D-animasjon av partikkelbane', fontsize=14)

    def oppdater(ramme):
        x = posisjoner[:ramme,0]
        y = posisjoner[:ramme,1]
        linje.set_data(x, y)
        # Fiks: Bruk lister for punktdata
        punkt.set_data([posisjoner[ramme,0]], [posisjoner[ramme,1]])
        return linje, punkt,
    
    linje, = ax.plot([], [], 'b-', lw=2)
    punkt, = ax.plot([], [], 'ro', markersize=8)
    
    def init():
        linje.set_data([], [])
        punkt.set_data([], [])
        return linje, punkt,
    
    def oppdater(ramme):
        x = posisjoner[:ramme,0]
        y = posisjoner[:ramme,1]
        linje.set_data(x, y)
        punkt.set_data(posisjoner[ramme,0], posisjoner[ramme,1])
        return linje, punkt,
    
    ani = animation.FuncAnimation(
        fig, oppdater, frames=len(posisjoner), 
        init_func=init, blit=True, interval=20
    )
    # Lagre animasjon
    ani.save(lagre_sti, writer='pillow', fps=30)
    return ani

# Generer animasjon for konstant felt
t, pos_konstant, _ = simuler_bane(q, m, konstant_B, r0, v0, t_max, dt)
animer_2d_bane(pos_konstant, "konstant_felt.gif")

def animer_3d_bane(posisjoner, lagre_sti="partikkel_3d.gif"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Beregn grenser
    maks_rekkevidde = np.max(np.abs(posisjoner))
    
    ax.set_xlim(-maks_rekkevidde, maks_rekkevidde)
    ax.set_ylim(-maks_rekkevidde, maks_rekkevidde)
    ax.set_zlim(-maks_rekkevidde, maks_rekkevidde)
    ax.set_xlabel("x [m]", fontsize=12)
    ax.set_ylabel("y [m]", fontsize=12)
    ax.set_zlabel("z [m]", fontsize=12)
    ax.set_title('3D-animasjon av partikkelbane', fontsize=14)

    def oppdater(ramme):
        x = posisjoner[:ramme,0]
        y = posisjoner[:ramme,1]
        z = posisjoner[:ramme,2]
        linje.set_data(x, y)
        linje.set_3d_properties(z)
        # Fiks: Bruk lister for punktdata
        punkt.set_data([posisjoner[ramme,0]], [posisjoner[ramme,1]])
        punkt.set_3d_properties([posisjoner[ramme,2]])
        return linje, punkt,
    
    linje, = ax.plot([], [], [], 'b-', lw=2)
    punkt, = ax.plot([], [], [], 'ro', markersize=8)
    
    def init():
        linje.set_data([], [])
        linje.set_3d_properties([])
        punkt.set_data([], [])
        punkt.set_3d_properties([])
        return linje, punkt,
    
    def oppdater(ramme):
        x = posisjoner[:ramme,0]
        y = posisjoner[:ramme,1]
        z = posisjoner[:ramme,2]
        linje.set_data(x, y)
        linje.set_3d_properties(z)
        punkt.set_data([posisjoner[ramme,0]], [posisjoner[ramme,1]])
        punkt.set_3d_properties([posisjoner[ramme,2]])
        return linje, punkt,
    
    ani = animation.FuncAnimation(
        fig, oppdater, frames=len(posisjoner), 
        init_func=init, blit=True, interval=20
    )
    # Lagre animasjon
    ani.save(lagre_sti, writer='pillow', fps=30)
    return ani

# Generer animasjon for spiralbane
v0_spiral = np.array([1e6, 0, 1e6])  # Hastighet med z-komponent
t, pos_spiral, _ = simuler_bane(q, m, konstant_B, r0, v0_spiral, t_max, dt)
animer_3d_bane(pos_spiral, "spiralbane.gif")

## Del E: Magnetisk speil
def magnetisk_speil_B(r, B0=0.5, k=0.01):
    x, y, z = r
    return np.array([0, 0, B0 * (1 + k*(z**2 - x**2 - y**2))])

# Simuler magnetisk speil
v0_speil = np.array([0, 1e6, 2e6])  # Hastighet med z-komponent
t_max_speil = 20e-6  # Lengre simuleringstid

def B_func_speil(r):
    return magnetisk_speil_B(r, B0=0.5, k=0.01)

t, pos_speil, v_speil = simuler_bane(q, m, B_func_speil, r0, v0_speil, t_max_speil, dt)

# Plott resultat
plt.figure(figsize=(10, 8))
plt.plot(t, pos_speil[:, 2], 'b-')
plt.xlabel('Tid [s]', fontsize=12)
plt.ylabel('z-posisjon [m]', fontsize=12)
plt.title('Magnetisk speil: Partikkelbevegelse langs z-aksen', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# 3D-animasjon av magnetisk speil
animer_3d_bane(pos_speil, "magnetisk_speil.gif")

# Øk simuleringstiden for magnetisk speil
t_max_speil = 50e-6  # Fra 20e-6 til 50e-6
t, pos_speil, v_speil = simuler_bane(q, m, B_func_speil, r0, v0_speil, t_max_speil, dt) 