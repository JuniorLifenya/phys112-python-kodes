import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Gauss-systemet: k = 1
k = 1
q = 1  # statC

# Definer rutenett (feltområde)
xrange = [-10, 10]
yrange = [-10, 10]
step = 200
Xlist = np.linspace(xrange[0], xrange[1], step)
Ylist = np.linspace(yrange[0], yrange[1], step)
X, Y = np.meshgrid(Xlist, Ylist)

# Felt-funksjon for én punktladning i 2D
def point_charge_field(X, Y, x0, y0, q):
    dx = X - x0
    dy = Y - y0
    r2 = dx**2 + dy**2
    r2[r2 == 0] = 1e-10  # Unngå deling på null
    Ex = q * dx / r2
    Ey = q * dy / r2
    E_log = np.log(np.sqrt(Ex**2 + Ey**2))
    return Ex, Ey, E_log

# Oppsett for animasjon
fig, ax = plt.subplots()
stream = None
contour = None

# Bevegelsesbane: sirkel
def get_position(t):
    R = 3  # radius
    omega = 2 * np.pi / 50  # vinkelhastighet
    return R * np.cos(omega * t), R * np.sin(omega * t)

# Init-funksjon
def init():
    ax.set_xlim(xrange)
    ax.set_ylim(yrange)
    ax.set_title("Elektrisk felt fra en ladning i bevegelse")
    return []

# Oppdatering for hvert steg
def update(t):
    global stream, contour
    ax.clear()
    x0, y0 = get_position(t)
    Ex, Ey, E_log = point_charge_field(X, Y, x0, y0, q)
    stream = ax.streamplot(X, Y, Ex, Ey, color="black", density=1.5, arrowsize=1)
    levels = np.linspace(np.min(E_log), np.max(E_log), 200)
    contour = ax.contourf(X, Y, E_log, levels=levels, cmap="turbo")
    ax.plot(x0, y0, 'ro')  # selve ladningen
    ax.set_title(f"Ladningens posisjon: ({x0:.2f}, {y0:.2f})")
    ax.set_aspect('equal')
    return []

ani = FuncAnimation(fig, update, frames=60, init_func=init, interval=100)
plt.show()

# "I denne animasjonen flytter vi ladningen gradvis, og feltet oppdateres momentant i hvert bilde. 
# Men i virkeligheten ville endringen i feltet spre seg med lysets hastighet – feltet 'vet' ikke umiddelbart at ladningen har flyttet seg."
#"Akkurat som Zenons pil – som ser ut til å stå stille i hvert øyeblikk – simulerer vi bevegelse gjennom en serie stillbilder. 
# Det gir en illusjon av dynamikk, men det mangler den fysiske 'limet' som er tid, hastighet og signalpropagasjon."
#"Dette er grunnen til at vi trenger elektrodynamikk og Maxwells ligninger – for å modellere felt som virkelig beveger seg i rom og tid."
# Så egentlig når du vil vite feltet E ved et punkt r og tid t, så må du vite hva den gjorde på et tidligere tidspunkt t_ret = t-abs(r-r'(t_ret))/c
# Når ladningen akselererer → feltet rundt endres → feltet får bølger som sprer seg utover: