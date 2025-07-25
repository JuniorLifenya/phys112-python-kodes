import numpy as np 
import matplotlib.pyplot as plt 
import math as m
import pandas as pd

#######################################################################################################
#######################################################################################################

epsilon_0 = 8.85e-12
K = 1/(4*np.pi*epsilon_0)

df = pd.read_csv("ladninger.csv")
q_numb = df["charge"][0]
q_tot = df["charge"][1]*10e-9