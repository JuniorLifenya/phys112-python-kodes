import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#################################################################################################

#----------Oppgave tekst------------------------------------------------------------------------#

"Du er gitt samme CSV-fil (ladninger.csv) som i oppgave 1 "
"Vi antar permitiviteten i vakuum, ε0 = 8.854 x 10^-12 F/m"
"Lag et plot som viser alle de 12 ladningene plottet som prikker (rød for positiv, blå for negativ)"
"På plottet skal det også tegnes inn feltlinjene til det elektriske feltet satt opp av de 12 ladningene"
"Sammenlign plottet med resultatet fra eksempeloppgaven om elektrisk felt og kraft. "
"Stemmer retningen til kraften partikkelen opplever med  feltlinjene i dette plottet?"
"Legg ved en liten kommentar på slutten som svarer på dette"


#----------Konstanter og variabler--------------------------------------------------------------#

EPSILON_ZERO = 8.854e-12 #F/m
K = 1/(4*np.pi*EPSILON_ZERO)

xrange = np.linspace(-20,30,200)
yrange = np.linspace(-30,20,200)

#----------Oppsett av plan----------------------------------------------------------------------#

Q = pd.read_csv("ladninger_3.csv")
q = Q["charge"].to_numpy()*1e-9 # Ladningene er oppgitt i nC , så nå har vi C
x = Q["pos_x"].to_numpy()
y = Q["pos_y"].to_numpy()
zip_info = list(zip(q,x,y))

# U,V = np.zeros_like(X), np.zeros_like(Y) # An alternative way to create and fill up the fields.
 
#-------Felt-styrke Funksjonen------------------------------------------------------------------#
def E(X, Y):
        """ Returnerer feltstyrken i x- og y-retning i (0,0) fra ladningene """
        Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
        for qi,xi,yi in zip_info:
            dx = X - xi
            dy = Y - yi
            rq = np.sqrt(dx**2 + dy**2)
            rq[rq==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner

            Ex += (K*qi)/(rq**3)*dx
            Ey += (K*qi)/(rq**3)*dy

        return Ex,Ey

#-------Beregning av feltstyrken----------------------------------------------------------------#

X , Y = np.meshgrid(xrange,yrange) 
U, V = E(X, Y)

#----------- Potensial Funksjonen---------------------------------------------------------------#
def ø(X, Y):
    """ Returnerer potensialet i (X,Y) fra ladningene """
    ø = np.zeros_like(X)
    for qi,xi,yi in zip_info:
        dx = X - xi
        dy = Y - yi
        r = np.sqrt(dx**2 + dy**2) # Unngå dele på 0 , sette
        r[r==0 ]= 1e-10 # Unngå dele på 0 , setter d opp for gøy, og gode vaner 

        ø += K*qi/r

    return ø

V_tot = ø( X, Y)
V_plot = np.log(np.abs(V_tot))

#----------Plotting-----------------------------------------------------------------------------#

fig , ax = plt.subplots(figsize=(8,8))
Nivåkurvene = ax.contourf(X, Y, V_plot, levels=300, cmap = "turbo_r" ) # cycles through) # type: ignore # Viser nivåkurvene til potensialet

E_Retnings_felt = ax.streamplot(X,Y,U,V, color="black", density=1, arrowsize=1) # Trengs egentlig ikke siden oppgaven ber om nivåkurver

for qi,xi,yi in zip_info:
    if qi > 0:
        ax.plot(xi, yi, "ro", markersize=10)  # rød for positiv
    if qi < 0:
        ax.plot(xi, yi, "bo", markersize=10)  # blå for negativ



plt.gca().set_aspect('equal') #Setter like skala på begge aksene


#----------Plot labels--------------------------------------------------------------------------#

plt.title("Elektrisk felt fra to punktladninger")
plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.grid()
plt.show()

#----------FINISHED ----------------------------------------------------------------------------#