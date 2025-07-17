
import numpy as np


def f(x,y): #dydx = (3x-2y)/(x+2y)
    return (3*x+y)/(x+2*y)

def runge_kutta_calc(x0,y0,x1 ,h ): # Her definerer vi metoden som skal brukes

    n = int ((x1-x0)/h)
    
    y = y0 
    for i in range(n) : 
    
        k1 = f(x0,y)
        k2 = f(x0 + h/2, y + h*k1/2)
        
        y += (h/2.0)*(k1 + k2 )
        x0 +=  h # Siden vi ikke har en x-variabel i arrayet, så må vi oppdatere den manuelt,
        #I tillegg fordi antall steg n er definert av x1-x0/h så må x oppdateres
    return y
    
# Nå tester vis

print(runge_kutta_calc(0.3,5.0,0.9,0.1))
