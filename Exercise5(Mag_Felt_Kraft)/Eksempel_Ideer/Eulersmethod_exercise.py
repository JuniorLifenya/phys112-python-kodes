import numpy as np
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################
# Same start as the Other codes
# Define the functions for the system of ODEs

# Constants
m1 = 0.45    # mass

# Initial values
r0 = np.array([0.0, 0.0]) 
v0 = np.array([5.0, 5.0])
t0 , tf , h = 0.0 ,8.0
h = 0.1 # Gir Antall sekunder mellom hver tidspunkt, bestemmer diskretisering
n = int((tf - t0) / h) #Eksakt antall tidspunkter
#############################################################################################

#Måten vi skriver difflikningene som flervariable funksjoner hjelper for senere kompleksitet#
def f(t, r, v):  # dv/dt = -g, alternativ : dv/dt = -(Gm2)/(r21)^3
    simpel_gravity = np.array([0.0,-9.81])
    return simpel_gravity 

def g(t, r, v): #dr/dt = v
    return v

def Euler_system(t0,r0,v0,h,n):
    
    # Initierer arrays der vi skal lagre resultatene i avhengig av dere størrelse
    t = np.zeros(n+1)
    r = np.zeros((n+1,2)) # Definerer størrelsen på r slik at vi kan lagre alle tidspunkter
    v = np.zeros((n+1,2)) # Igjen fordi vi jobber med 2D vektorer v = [vx,vy]

    t[0],r[0],v[0] = t0 , r0, v0
    
    for i in range (n):
        ti = t[i]
        ri = r[i]
        vi = v[i]

        #Definert slik for å kunne se likheter med runge kutta metoden
        K1 = f(ti,ri,vi) # Egentlig akselerasjonen a = dvdt
        G1 = g(ti,ri,vi) # Egentlig hastigheten v = drdt

        # Hver eneste tilstands variabel øker med dens deriverte multiplisert med h 
        # Bare tiden øker med h self 
        t[i+1] = t[i] + h
        r[i+1] = r[i] + h*G1 # r = r + v*h
        v[i+1] = v[i] + h*K1 # v = v + a*h

        # Generelt for en størrelse L øker den med L[i+1] = L[i] + h*L'[i]
        # Hvilken deriverte er avhenglig av initial verdi problemet , for eksempel L'=L , L(0) = 1
        
    return t,r,v


################################################################################################
t_vals,r_vals,v_vals = Euler_system(t0,r0,v0,h,n)


# Hent verdier for projeksjonen : husk at de ser slik ut
# r_vals = [[x0, y0],[x1, y1],[x2, y2], ...] , så verdiene våre er inni disse listene

# Derfor henter vi slik, ved slicing 
x_vals = r_vals[:, 0]
y_vals = r_vals[:, 1]

# Nå ser de slik ut :
# x_vals = [x0, x1, x2, ...] 
# y_vals = [y0, y1, y2, ...] 

x_analytic = 5.0 * 8
y_analytic = 5.0 * 8 - 0.5 * 9.81 * 8**2
print(f"For h = {h}\n")
print(f"analytisk x(8), y(8): ({x_analytic:.3f}{y_analytic:.3f}) m")

x_estimert=r_vals[-1][0]
y_estimert=r_vals[-1][1]
print(f"Slutt-posisjon (x,y) etter 8 sekunder: ({x_estimert:.3f},{y_estimert:.3f}) m \n")

###############################################################################################
# Plotting og animasjon

# Moving animation man 
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-')

ax.set_xlim(-1, 10)
ax.set_ylim(-5, 5)

def animate(i):
    line.set_data(r_vals[:i,0], r_vals[:i,1])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_vals), 
                    interval=20, blit=True)

# Beregn kinetisk energi

def kinetic_energy(v):
    return 0.5 * m1 * np.dot(v, v)
print("Slutthastighet (vx,vy) etter 8 sekunder:", v_vals[-1], "m/s ")
print("Initial KE:", kinetic_energy(v0))
print("Final KE:", kinetic_energy(v_vals[-1]))


plt.plot(x_vals, y_vals,color= "red")
plt.gca().set_aspect('equal')
plt.title("Partikkelbane i gravitasjonsfelt Euler (h=0.1)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
ani.save("Euler_h.1_Kast.gif" , writer='pillow', fps=20)
plt.show()



















plt.plot(x_vals, y_vals,color= "g")
plt.gca().set_aspect('equal')
plt.title("Partikkelbane i gravitasjonsfelt Euler (h=0.1)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
ani.save("Euler_h.1_Kast.gif" , writer='pillow', fps=20)
plt.show()

#####################################################################################