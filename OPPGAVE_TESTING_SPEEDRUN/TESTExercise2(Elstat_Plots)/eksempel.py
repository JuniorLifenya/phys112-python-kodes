import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#################################################################################################

#----------Oppgave tekst------------------------------------------------------------------------#
"To statiske ladninger i vakuum. Den ene lokalisert på (1/2,0) [m], ladning 5*10^-17 C"
"Den andre lokalisert på (-1/2,0) [m], ladning -5*10^-17 C"
"Plot de elektriske feltlinjene i området x = [-1,1] og y = [-1,1]"
"Samt illustrere hvor ladningene er med synlige fargede sirkler."
"Rød sirkel for positiv ladning, blå for negativ"

#----------Konstanter og variabler---------------------------------------------------------------#

EPSILON_ZERO = 8.854e-12 #F/m
K = 1/(4*np.pi*EPSILON_ZERO)
q1, q2 = 5e-17, -5e-17 #C
x1, y1 = 0.5, 0 #m
x2, y2 = -0.5, 0 #m

#----------Oppsett av plan------------------------------------------------------------------------#

x = y = np.linspace(-1,1,200)
X , Y = np.meshgrid(x,y)
# U,V = np.zeros_like(X), np.zeros_like(Y) # An alternative way to create and fill up the fields.
 
#----------Funksjoner-----------------------------------------------------------------------------#

def  E(q, xq, yq, X, Y):
    """ Returnerer feltstyrken i x- og y-retning i (0,0) fra ladningene """
    dx = X - xq
    dy = Y - yq

    r = np.sqrt(dx**2 + dy**2)
    r[r==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner 

    Ex = (K*q)/(r**3)*dx
    Ey = (K*q)/(r**3)*dy

    return Ex,Ey

Ex1, Ey1 = E(q1, x1, y1, X, Y) # Since the function returns two values, we need to call it twice for each charge
Ex2, Ey2 = E(q2, x2, y2, X, Y)

Ex = Ex1 + Ex2
Ey = Ey1 + Ey2

U, V = Ex, Ey

#----------Plot settings---------------------------------------------------------------------------#

fig,ax = plt.subplots(figsize=(7,7))
plt.streamplot(X,Y,U,V, color="black", density=1, arrowsize=1)


plt.scatter(x1,y1,color = "red", s=200) #Positiv ladning
plt.scatter(x2,y2,color = "blue", s=200) #Negativ ladning
plt.plot(0,0,'go', markersize=5) #Origo

plt.gca().set_aspect('equal', adjustable="box") #Setter like skala på begge aksene

plt.xlim(-1,1)
plt.ylim(-1,1)

#----------Plot labels----------------------------------------------------------------------------#

plt.title("Elektrisk felt fra to punktladninger")
plt.xlabel("x [m]")
plt.ylabel("y [m]")

#plt.grid()
plt.show()


#----------FINISHED -------------------------------------------------------------------------------#