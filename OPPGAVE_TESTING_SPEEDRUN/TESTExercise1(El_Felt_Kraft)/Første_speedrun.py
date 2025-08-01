import numpy as np 
import matplotlib.pyplot as plt 
import math as m
import pandas as pd

#######################################################################################################
#######################################################################################################

epsilon_0 = 8.85e-12
K = 1/(4 * np.pi * epsilon_0)

df = pd.read_csv("ladninger.csv")
q_C = df["charge"].to_numpy()*1e-9 # List of the charge number
q_xpos = df["pos_x"].to_numpy() # List of all charges 
q_ypos = df["pos_y"].to_numpy()

# The total field strength in x direction is Ex = K(Qq)/r^2cos(theta) , sine for y direction 
# I want to use that the theta will be the arctan of y/x positions
def E(q,x,y):
    Ex = 0 
    Ey = 0 
    ri0 = 0
    for i in range (len(q)):

        qi , xi , yi = q[i] , x[i] , y[i]
        r0 = [0,0] # To avoid directly deviding by 0 
        
        ri0 += np.sqrt((xi-r0[0])**2 + (yi-r0[1])**2) + 1e-12 # Include a small epsilon here 
        øi = np.arctan2(-yi,-xi) # arctan2 takes two arguments, and dont accumalte charges with +=

        Ex += K*np.cos(øi)* (qi)/ri0**3
        Ey += K*np.sin(øi)* (qi)/ri0**3
    Etot = np.sqrt((Ex)**2+ (Ey)**2)

    return f" Ex = {np.sum(Ex)}\n Ey = {np.sum(Ey)}\n E = {np.sum(Etot)}"

print(E(q_C,q_xpos,q_ypos))
##################################################################################################

