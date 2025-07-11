import numpy as np
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################

# Define the functions for the system of ODEs


# Constants
m1 = 0.45   
g_acc= 9.81

# Initial values
r0 = np.array([0.0, 0.0]) 
v0 = np.array([5.0, 5.0])
t0 , tf = 0.0 , 8.0
h = 0.3 # Gir Antall sekunder mellom hver tidspunkt, bestemmer diskretisering
n = int((tf - t0) / h) #Eksakt antall tidspunkter
#############################################################################################
def f(t, r, v):  # dv/dt = -(Gm2)/(r21)^3
    simpel_gravity = np.array([0.0,-g_acc])
    return simpel_gravity 

def g(t, r, v): #drdt really 
    return v

#############################################################################################
#############################################################################################


def Runge_Kutta_system(f,g,t0,r0,v0,h,n):
    
    t = np.zeros(n+1)
    r = np.zeros((n+1,2)) # Because we have 2 dimensions
    v = np.zeros((n+1,2)) # Because we have v = [vx,vy]

    t[0],r[0],v[0] = t0 , r0, v0

    for i in range (n):
        ti = t[i]
        ri = r[i]
        vi = v[i]

        K1 = f(ti,ri,vi)
        G1 = g(ti,ri,vi)

        K2 = f(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        G2 = g(ti + h/2, ri + h*G1/2, vi + h*K1/2)

        K3 = f(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        G3 = g(ti + h/2, ri + h*G2/2, vi + h*K2/2)

        K4 = f(ti + h , ri + h*G3, vi + h*K3)
        G4 = g(ti + h , ri + h*G3, vi + h*K3)

        t[i+1] = t[i] + h 
        v[i+1] = v[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        r[i+1] = r[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        
    return t,r,v

#############################################################################################
#############################################################################################

#For watching EVERY step(like teacher wanted)

# For perfect sircle motion ##################################################################

#period = 2 * np.pi / (q * B0 / m)  # 2*pi / omega_c
#tf = period * 1  # for one full circle
#h = 0.01
#n = int(tf / h)

#############################################################################################

# Run simulation
t_vals, r_vals, v_vals = Runge_Kutta_system(f,g,t0, r0, v0,h,n)


#############################################################################################

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
plt.title("Partikkelbane i gravitasjonsfelt RK4 (h=0.1)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
ani.save("RK4_h.1_Kast.gif" , writer='pillow', fps=20)
plt.show()

#############################################################################################

