# Pseudo-code for FDTD
def fdtd_update(Ez, Hy, Hx, epsilon, sigma, dt, dx):
    # Update H from E curl
    Hx[1:-1,1:-1] -= dt/(μ*dx) * (Ez[1:-1,2:] - Ez[1:-1,:-2])
    Hy[1:-1,1:-1] += dt/(μ*dx) * (Ez[2:,1:-1] - Ez[:-2,1:-1])
    
    # Update E from H curl (with anisotropic epsilon)
    curlH = (Hy[1:,1:-1] - Hy[:-1,1:-1]) - (Hx[1:-1,1:] - Hx[1:-1,:-1])
    Ez[1:-1,1:-1] += dt/(ε[1:-1,1:-1]*dx) * curlH
    
    return Ez, Hy, Hx

# Task: Propagate polarized wave through birefringent crystal
# Visualize polarization rotation vs crystal orientation