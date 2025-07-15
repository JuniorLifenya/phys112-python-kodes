
import numpy as np
def discharging_current(t, Q0, R, C):
    return (Q0 / (R * C)) * np.exp(-t / (R * C))

def forward_difference(t_end, h, Q0, R, C):
    n = int(t_end / h)
    q = Q0
    for _ in range(n):
        dq = - (q / (R * C)) * h
        q += dq
    return q / (R * C)  # i = q / (R*C)

