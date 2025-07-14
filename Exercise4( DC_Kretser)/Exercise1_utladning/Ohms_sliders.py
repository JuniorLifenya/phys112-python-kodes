


def Ohms_law_current(V, R):
    """Calculate current using Ohm's law: I = V / R"""
    if R < 0:
        raise ValueError("Resistance cannot be negative")
    return V / R if R != 0 else float('inf')  # Avoid division by zero

def Ohms_law_voltage(I, R):
    """Calculate voltage using Ohm's law: V = I * R"""
    if R < 0:
        raise ValueError("Resistance cannot be negative")
    return I * R

