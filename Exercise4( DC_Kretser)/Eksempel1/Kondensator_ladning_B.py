import numpy as np 
import matplotlib.pyplot as plt
##########################################################################################################

### Initial Verdier og betingelser for RC-kretsen #
R = 1e3 # Motstand i ohm
C = 100e-6 # Kapasitans i farad
V0= 5.0 # Spenning i volt
t0 = 0.0 # Starttidspunkt i sekunder
tf = 0.4 # Sluttidspunkt i sekunder

h = 0.1 # Steglengde i sekunder / discretisering
n = int((tf - t0) / h) # Antall tidspunkter
Vc0 = 0.0 # Startspenning i kondensatoren i volt
##########################################################################################################

def f(t,Vc): # Vår dydx = (Vin-Vc)/RC = f(t,Vc)
    y = (V0- Vc) / (R * C) 
    return y
##########################################################################################################

### Runge-Kutta 2. Dette er egentlig et midpunkt-metode ##################################################
def RK3_metode(f,t0,tf,y0,h,n): # Det er ingen fysiske forflytninger her i y og x , men bare t 

    # Initierer arrays for tid og spenning der vi lagrer resultatene
    
    t = np.zeros(n+1) # Instead of including them as vector-arguments in the functions
    y = np.zeros(n+1) # This is how YOU INITIALIZE EMPTY ARRAYS in python , they become filled later

    t[0] = t0
    y[0] = y0 

    for i in range(n): # Could have just written range(n) also hehe 
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
    return V0 * (1 - np.exp(-t / (R*C)))

###########################################################################################################

# --- Kjøring av Runge-Kutta 2 ---
t , V_rk3 = RK3_metode(f,t0,tf,Vc0,h,n) # This returns a two things vector like stuff like v = (t,y)

V_korrekt = V_eksakt(t) # Beregner den eksakte løsningen for sammenligning

print(f"V_c(t) etter {tf} sekunder: {V_rk3[-1]:.2f} V")

#####################################################################################################
# --- Plot ---
plt.figure(figsize=(10,6))
plt.plot(t, V_rk3, label="RK2-løsning", color="blue")
plt.plot(t, V_korrekt, '--', label="Analytisk løsning", color="orange" , marker ='o', markersize=3)
plt.title("Lading av kondensator i RC-krets med RK2")
plt.xlabel("Tid (s)")
plt.ylabel("Spenning over kondensator (V)")
plt.grid(True)

plt.legend()
plt.savefig("kondensator_lading_rk3.png")
plt.show()