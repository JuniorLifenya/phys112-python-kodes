
# Lim in helt til slutt av oppgaven # 
fig, ax = plt.subplots(figsize=(10, 5))
# Moving animation man 
from matplotlib.animation import FuncAnimation
line, = ax.plot([], [], '-', color="green")
def animate(i):
    line.set_data(r_vals[:i,0], r_vals[:i,1])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_vals), 
                    interval=30, blit=True)

ax.plot(x_vals, y_vals, '-', linewidth=1.5, label='Trajectory', color  = "green")
ax.scatter([r0[0]], [r0[1]],c='red', s=50, label='Start')
ax.scatter([x_vals[-1]], [y_vals[-1]], c='b', s=50, label='End')
ax.legend()

plt.plot(x_vals, y_vals,color= "orange") # type: ignore
plt.title(f" Partikkel-varierende Bane med (h= {h}) etter {tf} sekunder")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(True)
plt.savefig("Partikkel-drag_Bane(50s).png", dpi=300, bbox_inches='tight')
plt.show()