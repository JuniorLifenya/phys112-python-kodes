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