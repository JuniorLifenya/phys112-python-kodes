import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#################################################################################################

#----------Oppgave tekst------------------------------------------------------------------------#
"To statiske ladninger i vakuum. Den ene lokalisert på (1/2,0) [m], ladning 5*10^-17 C"
"Den andre lokalisert på (-1/2,0) [m], ladning -5*10^-17 C"
"Modifiser koden fra løsningsforslaget til eksempeloppgaven (tidligere) slik at den også viser"
"Nivåkurvene til det elektriske potensialet satt oppp av de to ladningene ."
"Lurt å ta logaritmen av absoluttverdien til det elektriske potensialet for å få et bedre bilde"

#----------Konstanter og variabler---------------------------------------------------------------#

EPSILON_ZERO = 8.854e-12 #F/m
K = 1/(4*np.pi*EPSILON_ZERO)
q1, q2 = 5e-17, -5e-17 #C
x1, y1 = 0.5, 0 #m
x2, y2 = -0.5, 0 #m

#----------Oppsett av plan-----------------------------------------------------------------------#

x = y = np.linspace(-1,1,200)
X , Y = np.meshgrid(x,y)
# U,V = np.zeros_like(X), np.zeros_like(Y) # An alternative way to create and fill up the fields.
 
#-------Felt-styrke Funksjonen-------------------------------------------------------------------#

def  E(q, xq, yq, X, Y):
    """ Returnerer feltstyrken i x- og y-retning i (0,0) fra ladningene """
    dx = X - xq
    dy = Y - yq

    r = np.sqrt(dx**2 + dy**2)
    r[r==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner 

    Ex = (K*q)/(r**3)*dx
    Ey = (K*q)/(r**3)*dy

    return Ex,Ey
Ex1,Ey1 = E(q1, x1, y1, X, Y) # Since the function returns two values, we need to call it twice for each charge
Ex2,Ey2 = E(q2, x2, y2, X, Y)


Ex = Ex1 + Ex2
Ey = Ey1 + Ey2
U, V = Ex, Ey

#----------- Potensial Funksjonen----------------------------------------------------------------#
def P(q, xq, yq, X, Y):
    """ Returnerer potensialet i (X,Y) fra ladningene """
    dx = X - xq
    dy = Y - yq

    r = np.sqrt(dx**2 + dy**2)
    r[r==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner 

    Px = K*q/r
    Py = K*q/r

    return Px,Py

Px1,Py1 = P(q1, x1, y1, X, Y) # Since the function returns two values, we need to call it twice for each charge
Px2,Py2 = P(q2, x2, y2, X, Y)

Px = Px1 + Px2
Py = Py1 + Py2

M,N = Px, Py

f = np.log(np.abs(M)) # Tar logaritmen av absoluttverd
g = np.log(np.abs(N))

ftot = np.log(np.abs(M+N)) # Tar logaritmen av absoluttverd

#----------Plotting-------------------------------------------------------------------------------#

fig , (ax1, ax2) = plt.subplots(figsize=(2,2), ncols=2)
Nivåkurvene = ax1.contourf(X, Y, ftot, levels=50, cmap="viridis") # type: ignore # Viser nivåkurvene til potensialet


E_Retnings_felt= ax2.streamplot(X,Y,U,V, color="black", density=1, arrowsize=1) # Trengs egentlig ikke siden oppgaven ber om nivåkurver

plt.scatter(x1,y1,color = "red", s=200) #Positiv ladning
plt.scatter(x2,y2,color = "blue", s=200) #Negativ ladning
plt.plot(x1,y1,'ro', markersize=15) #Positiv ladning
plt.plot(x2,y2,'bo', markersize=15) #Negativ ladning

plt.gca().set_aspect('equal', adjustable="box") #Setter like skala på begge aksene

plt.xlim(-1,1)
plt.ylim(-1,1)

#----------Plot labels----------------------------------------------------------------------------#

plt.title("Elektrisk felt fra to punktladninger")
plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.grid()
plt.show()


#----------FINISHED -------------------------------------------------------------------------------#