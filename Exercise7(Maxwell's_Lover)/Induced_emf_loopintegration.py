# Pseudo-code
def calculate_emf(B_field, loop_path, velocity):
    """
    B_field: Function B(x,y,t) returning [Bx, By]
    loop_path: Array of [x,y] points defining a closed loop
    velocity: [vx, vy] of loop motion
    """
    emf = 0
    dt = 1e-3  # Time step
    for i in range(len(loop_path)):
        x, y = loop_path[i]
        # Time-rate of flux change
        dB_dt = (B_field(x, y, t+dt) - B_field(x, y, t)) / dt
        # Motional EMF term (v × B)·dl
        v_cross_B = velocity[0]*B_field(x,y,t)[1] - velocity[1]*B_field(x,y,t)[0]
        emf += np.dot([-dB_dt[1], dB_dt[0]], dl) + v_cross_B * dl_magnitude
    return emf

# Task: Simulate a square loop moving through B = (0, B0*exp(-x^2))
# Plot induced EMF vs loop position for different velocities