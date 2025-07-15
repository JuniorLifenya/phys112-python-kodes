import numpy as np
import matplotlib.pyplot as plt
##########################################################################################################

### Initial Verdier og betingelser for RC-kretsen #
R = 1e3 # Motstand i ohm
C = 470e-6   # Kapasitans i farad
V0= 5.0 # Spenning i volt
tau = R * C
t0 = 0.0 # Starttidspunkt i sekunder
t_slutt = 8.0 # Sluttidspunkt i sekunder

h = 0.01 # Steglengde i sekunder / discretisering
n = int((t_slutt - t0) / h) # Antall tidspunkter
Vc0 = 0.0 # Startspenning i kondensatoren i volt
V_thresh = 3.0  
t_vals = np.linspace(0, t_slutt, n)
##########################################################################################################

def f(t,Vc): # Vår dydx = (Vin-Vc)/RC = f(t,Vc)
    y = (- Vc) / (tau) 
    return y
##########################################################################################################

### Runge-Kutta 2. Dette er egentlig et midpunkt-metode ##################################################
def RK2_metode(f,t0,y0,h,n): # Det er ingen fysiske forflytninger her i y og x , men bare t 

    # Initierer arrays for tid og spenning der vi lagrer resultatene
    
    t = np.zeros(n+1) # Instead of including them as vector-arguments in the functions
    y = np.zeros(n+1) # This is how YOU INITIALIZE EMPTY ARRAYS in python , they become filled later

    t[0] = t0
    y[0] = y0 

    for i in range(0,n,1): # Could have just written range(n) also hehe 
        ti = t[i]
        yi = y[i]

        k1 = f(ti, yi)
        k2 = f(ti + h, yi + k1*h/2)
        k3 = f(ti + h, yi + k2*h)
    
        y[i+1] = yi + h*(k1 + 4*k2 + k3)/6.0  
        t[i+1] = ti + h
        
    return t,y
###########################################################################################################
# --- Analytisk løsning for lading ---
def V_eksakt(t):
    return V0 * (1 - np.exp(-t / (tau)))

###########################################################################################################

# --- Kjøring av Runge-Kutta 2 ---
t , V_rk2 = RK2_metode(f,t0,Vc0,h,n) # This returns a two things vector like stuff like v = (t,y)

V_korrekt = V_eksakt(t) # Beregner den eksakte løsningen for sammenligning


#####################################################################################################
# --- Plot ---
plt.figure(figsize=(10,6))
plt.plot(t, V_rk2, label="RK2-løsning", color="blue")
plt.plot(t, V_korrekt, '--', label="Analytisk løsning", color="black")
plt.title("Lading av kondensator i RC-krets med RK2")
plt.xlabel("Tid (s)")
plt.ylabel("Spenning over kondensator (V)")
plt.grid(True)
plt.legend()
plt.show()