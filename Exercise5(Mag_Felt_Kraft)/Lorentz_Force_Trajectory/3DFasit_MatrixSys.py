import math as m 
import numpy as np 
import matplotlib.pyplot as plt

#############################################################################################
#############################################################################################

## Now ULTIMATELY we look at SYSTEMS of vector ode #############

# This code solves a system of ordinary differential equations using the Runge-Kutta method.
# For systems like this one here :
# dx/dt = f(t,x,y,z) = x + 2 * y
# dy/dt = g(t,x,y,z) = 3*x+2*y

#############################################################################################
#############################################################################################

q = 1.0
m = 1.0
B0 = 1.0

#############################################################################################
#############################################################################################
# Define the functions for the system of ODEs

def B_felt(t,r):
    x, y = r
    const_B = [0.0, 0.0, B0]
    var_B= [0.0,0.0,1 + 0.5 * np.sin(x) + 0.3 * np.cos(y)]
    return np.array(var_B)  # Constant B in z
def f(t, r, v):  # dv/dt = (q/m) * v x B
    B = B_felt(t, r)
    v3d = np.array([v[0], v[1], 0.0])  # pad v to 3D
    cross = np.cross(v3d, B)
    return (q / m) * cross  # return only x,y parts (2D vector)

#############################################################################################
#############################################################################################

def g(t, r, v): #drdt really 
    return v

def Runge_Kutta_system(t0,r0,v0,h,n):

    #t0,tf = 0.0 , 20.0
    #n= int((tf - t0) / h) #Alternative 
    
    t = np.zeros(n+1)
    r = np.zeros((n+1,3))
    v = np.zeros((n+1,3))

    t[0] = t0
    r[0] = r0 
    v[0] = v0
    for i in range (n):
        ti = t[i]
        ri = r[i]
        vi = v[i]

        K1 = f(ti,ri,vi)
        G1 = g(ti,ri,vi)

        K2 = f(ti + h/2, ri + h*G1/2, vi + h*K1/2)
        G2 = g(ti + h/2, ri + h*G1/2, vi + h*K1/2)

        K3 = f(ti + h/2, ri + h*G2/2, vi + h*K2/2)
        G3 = g(ti + h/2, ri + h*K2/2, vi + h*G2/2)

        K4 = f(ti + h , ri + h*G3, vi + h*K3)
        G4 = g(ti + h , ri + h*G3, vi + h*K3)

        t[i+1] = t[i] + h 
        v[i+1] = v[i] + h/6 * (K1 + 2*K2 + 2*K3 + K4)
        r[i+1] = r[i] + h/6 * (G1 + 2*G2 + 2*G3 + G4)
        
    return t,r,v

#############################################################################################
#############################################################################################


n = int (input ( " Please enter number of iterations ")) #For watching EVERY step(like teacher wanted)

# For perfect sircle motion #####################################

#period = 2 * np.pi / (q * B0 / m)  # 2*pi / omega_c
#tf = period * 1  # for one full circle
#h = 0.01
#n = int(tf / h)
#################################################################

# Initial values
v0 = np.array([0.0, 1.0,1.0])  # vx0, vy0
r0 = np.array([0.0, 0.0])  # x0, y0
t0 = 0.0
h = 0.01
# Run simulation
t_vals, r_vals, v_vals = Runge_Kutta_system(t0, r0, v0, h,n)

# Plot trajectory
x_vals = r_vals[:, 0]
y_vals = r_vals[:, 1]

def kinetic_energy(v):
    return 0.5 * m * np.dot(v, v)

print("Initial KE:", kinetic_energy(v0))
print("Final KE:", kinetic_energy(v_vals[-1]))

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
plt.plot(x_vals, y_vals,color= "orange")
plt.gca().set_aspect('equal')
plt.title("Charged Particle in Magnetic Field")
plt.xlabel("r")
plt.ylabel("v")
plt.grid(True)
plt.show()

# At 627 iterations, the particle makes a perfect circle revolution, But Ek_0 != EK_f still decimals
#############################################################################################
#############################################################################################