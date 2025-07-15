

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametre
V0 = 5.0             # Startspenning
C = 470e-6           # Kapasitans
R = 1000             # Motstand
V_thresh = 3.0       # Terskelspenning
h = 0.01             # Tidssteg
t_max = 5.0
n = int(t_max / h)
t_vals = np.linspace(0, t_max, n)
tau = R * C

# Beregn spenning over tid (analytisk oppladning)
V_vals = V0 * (1 - np.exp(-t_vals / tau))
print("Analytisk Spenning V_C(t) over tid:", V_vals)
# Finn tidspunkt hvor terskelen nås
above_thresh_idx = np.where(V_vals >= V_thresh)[0]
t_trigger = t_vals[above_thresh_idx[0]] if len(above_thresh_idx) > 0 else None

# Sett opp plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2, label="V_C(t)")
dot, = ax.plot([], [], 'ro', label="Nåværende punkt")
ax.set_xlim(0, t_max)
ax.set_ylim(0, V0 + 0.5)
ax.set_xlabel("Tid (s)")
ax.set_ylabel("Spenning V_C(t) (V)")
ax.set_title("RC-oppladning med terskel")

# Tekst-elementer
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', edgecolor='black'))
threshold_text = ax.text(0.5, 0.7, "", transform=ax.transAxes, fontsize=14,
                         ha='center', color='green', weight='bold')

ax.legend(loc="lower right")

# Variabel for å kontrollere én gang-visning
triggered = False

# Init
def init():
    line.set_data([], [])
    dot.set_data([], [])
    time_text.set_text("")
    threshold_text.set_text("")
    global triggered
    triggered = False
    return line, dot, time_text, threshold_text

# Oppdateringsfunksjon
def update(frame):
    global triggered
    t = t_vals[:frame]
    V = V_vals[:frame]
    current_t = t_vals[frame]
    current_V = V_vals[frame]

    line.set_data(t, V)
    dot.set_data([current_t], [current_V])

    time_text.set_text(f"Tid: {current_t:.2f} s")

    # Dersom terskelen nås og vi ikke har vist meldingen ennå
    if not triggered and current_V >= V_thresh:
        threshold_text.set_text(f"Terskel nådd etter {current_t:.2f} sekunder")
        triggered = True

    return line, dot, time_text, threshold_text

ani = FuncAnimation(fig, update, frames=len(t_vals), init_func=init,
                    interval=30, blit=False)

plt.tight_layout()
plt.show()
