

import numpy as np
import matplotlib.pyplot as plt


import numpy as np
import matplotlib.pyplot as plt

def f(t, Vc, R, C, V0):
    return (V0 - Vc) / (R * C)

def rk4_timer(R, C, V0, V_threshold, h=0.01):
    Vc = 0.0
    t = 0.0
    t_history = [t]
    Vc_history = [Vc]
    
    while Vc < V_threshold:
        k1 =  f(t, Vc, R, C, V0)
        k2 =  f(t + h/2, Vc + h*k1/2, R, C, V0)
        k3 =  f(t + h/2, Vc + h*k2/2, R, C, V0)
        k4 =  f(t + h, Vc + h*k3, R, C, V0)
        
        Vc += h*(k1 + 2*k2 + 2*k3 + k4) / 6
        t += h
        t_history.append(t)
        Vc_history.append(Vc)
        
    
    plt.plot(t_history, Vc_history)
    plt.xlabel('Tid (s)')
    plt.ylabel('$V_C$ (V)')
    plt.grid(True)
    plt.show()
    return t, Vc

# Eksempelkjøring:
R = 1e3   # Ohm
C = 470e-6  # F
V0 = 5.0    # V
V_threshold = 3.0  # V

tid, spenning = rk4_timer(R, C, V0, V_threshold)
print(f"Lys slår på etter {tid:.2f} sekunder")

def analytical_time(R, C, V0, Vc):
    return -R * C * np.log(1 - Vc / V0)

analytisk_tid = analytical_time(R, C, V0, V_threshold)
print(f"Analytisk tid: {analytisk_tid:.2f} sekunder")
print(f"Feil: {abs(tid - analytisk_tid):.4f} sekunder")

def finn_komponenter(t_delay, V0, V_threshold, C=None, R=None):
    tau_required = t_delay / (-np.log(1 - V_threshold / V0))
    
    if C is None and R is not None:
        C = tau_required / R
        return f"Bruk C = {C * 1e6:.2f} μF"
    elif R is None and C is not None:
        R = tau_required / C
        return f"Bruk R = {R / 1000:.2f} kΩ"
    else:
        return "Spesifiser enten R eller C"

# Eksempel: Ønsket forsinkelse på 10 sekunder
print(finn_komponenter(t_delay=10, V0=5, V_threshold=3.0, C=470e-6))








#########################################################################################################
def simuler_med_toleranse(R_nom, C_nom, toleranse=0.2):
    R_vals = [R_nom * (1 + toleranse), R_nom, R_nom * (1 - toleranse)]
    C_vals = [C_nom * (1 + toleranse), C_nom, C_nom * (1 - toleranse)]
    
    for R in R_vals:
        for C in C_vals:
            t = analytical_time(R, C, V0=5, Vc=3.15)  # 63% av 5V = 3.15V
            print(f"R={R/1000:.1f}kΩ, C={C*1e6:.0f}μF: t={t:.1f}s")

# Valgte komponenter for tau=10s (f.eks. R=10kΩ, C=1000μF)
simuler_med_toleranse(R_nom=10e3, C_nom=1000e-6, toleranse=0.2)

# Energiforbruk per time
def energi_per_time(R, C, V0=5):
    antall_cykler_per_time = 3600 / (R * C)  # Antall fullstendige ladingssykluser
    energi_per_syklus = 0.5 * C * V0**2 * 2  # Dissipasjon i både R og C
    return antall_cykler_per_time * energi_per_syklus

print(f"Energiforbruk: {energi_per_time(10e3, 1000e-6):.2f} J/time")