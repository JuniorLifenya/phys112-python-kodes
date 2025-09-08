import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#################################################################################################

#----------Oppgave tekst-------------------------------------------------------------------------#

"Du er gitt samme CSV-fil (ladninger.csv) som i oppgave 1 "
"Vi antar permitiviteten i vakuum, ε0 = 8.854 x 10^-12 F/m"
"Lag et plot som viser alle de 12 ladningene i et plottet som prikker (rød for positiv, blå for negativ)"
"På plottet skal det også tegnes inn feltlinjene til det elektriske feltet satt opp av de 12 ladningene"
"Sammenlign plottet med resultatet fra eksempeloppgaven om elektrisk felt og kraft. "
"Stemmer retningen til kraften partikkelen opplever med  feltlinjene i dette plottet?"
"Legg ved en liten kommentar på slutten som svarer på dette"


#----------Konstanter og variabler---------------------------------------------------------------#

EPSILON_ZERO = 8.854e-12 #F/m
K = 1/(4*np.pi*EPSILON_ZERO)
q1, q2 = 5e-17, -5e-17 #C
x1, y1 = 0.5, 0 #m
x2, y2 = -0.5, 0 #m

#----------Oppsett av plan-----------------------------------------------------------------------#
Q = pd.read_csv("ladninger.csv")
q = Q["charge"].to_numpy()*1e-9 # Ladningene er oppgitt i nC , så nå har vi C
x = Q["x"].to_numpy()
y = Q["y"].to_numpy()

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
def ø(q, xq, yq, X, Y):
    """ Returnerer potensialet i (X,Y) fra ladningene """
    dx = X - xq
    dy = Y - yq

    r = np.sqrt(dx**2 + dy**2)
    r[r==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner 

    ø = K*q/r

    return ø

#----------- Beregning av potensialet------------------------------------------------------------#
V_tot = ø(q1, x1, y1, X, Y) + ø(q2, x2, y2, X, Y)
V_plot = np.log(np.abs(V_tot))

#----------Plotting------------------------------------------------------------------------------#

fig , ax = plt.subplots(figsize=(6,6))
Nivåkurvene = ax.contour(X, Y, V_plot, levels=20, cmap = "turbo" , linestyles=["solid", "dashed", "dotted", "dashdot"] ) # cycles through) # type: ignore # Viser nivåkurvene til potensialet

E_Retnings_felt = ax.streamplot(X,Y,U,V, color="black", density=1, arrowsize=1) # Trengs egentlig ikke siden oppgaven ber om nivåkurver

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

#----------FINISHED ------------------------------------------------------------------------------#