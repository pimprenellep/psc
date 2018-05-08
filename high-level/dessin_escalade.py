from math import *
import matplotlib.pyplot as plt

#fontion distance
def d(A,B):
    return(sqrt((A[0]-B[0])**2+(A[1]-B[1])**2))
    
def type_de_pos(pos): #rq: ici c'est une vraie position
    if pos[0]==-1:
        return(3.2,1)   #3.2 = avec les 2 mains
    elif pos[1]==-1:
        return(3.2,0)
    else:
        if pos[2]==-1:
            return(3.1,3)  #3.1 = avce les 2 pieds
        elif pos[3]==-1:
            return(3.1,2)
        else:
            return(4,"")

def dessinvoie(Lprises):
    X=[Lprises[i][0] for i in range(len(Lprises)-1)]
    Y=[Lprises[i][1] for i in range(len(Lprises)-1)]
    plt.plot(X,Y, "gs", markersize = 5) #prises
    plt.axis('equal')
   
def dessin31(pos, Lprises):
    dessinvoie(Lprises)
    n, main = type_de_pos(pos)
    A=Lprises[pos[0]]
    B=Lprises[pos[1]]
    C=Lprises[pos[main]]
    #plt.axis([min(A[0],B[0],C[0])-1, max(A[0],B[0],C[0])+1, min(A[1],B[1],C[1])-1, max(A[1],B[1],C[1])+1]) #taille
    I=((A[0]+B[0])/2, (A[1]+B[1])/2)
    T=((I[0]-C[0])/4+C[0],(I[1]-C[1])/4+C[1]) #tete
    plt.plot([C[0],T[0],T[0],A[0]],[C[1],T[1],T[1]-(T[1]-I[1])*2/3,A[1]],"b", linewidth = 2)
    plt.plot([T[0]],[T[1]], "r", marker = 'o', markersize=10) #tête
    plt.plot([B[0],T[0]],[B[1],T[1]-(T[1]-I[1])*2/3], "b", linewidth = 2)
    plt.text(A[0], A[1], "PG")
    plt.text(C[0], C[1], "M")
    plt.text(B[0], B[1], "PD")
    plt.axis('equal')
    #plt.show()

def dessin32(pos, Lprises):
    dessinvoie(Lprises)
    n, pied = type_de_pos(pos)
    A=Lprises[pos[pied]]
    B=Lprises[pos[2]]
    C=Lprises[pos[3]]
    #plt.axis([min(A[0],B[0],C[0])-1, max(A[0],B[0],C[0])+1, min(A[1],B[1],C[1])-1, max(A[1],B[1],C[1])+1]) #taille
    I=((C[0]+B[0])/2, (C[1]+B[1])/2)
    T=((I[0]-A[0])/4+A[0],(I[1]-A[1])/4+A[1]) 
    J=(T[0],T[1]-(T[1]-I[1])*2/3)
    plt.plot([A[0],T[0],J[0],C[0]],[A[1],T[1],J[1],C[1]],"b", linewidth = 2)
    plt.plot([B[0],J[0]],[B[1],J[1]], "b", linewidth = 2)
    plt.plot([J[0]],[J[1]], "r", marker = 'o', markersize=10) #tête
    plt.text(A[0], A[1], "P")
    plt.text(C[0], C[1], "MD")
    plt.text(B[0], B[1], "MG")
    plt.axis('equal')
   # plt.show()

def dessin4(pos, Lprises):
    dessinvoie(Lprises)
    A=Lprises[pos[0]]
    B=Lprises[pos[1]]
    C=Lprises[pos[2]]
    D=Lprises[pos[3]]
   # plt.axis([min(A[0],B[0],C[0],D[0])-1, max(A[0],B[0],C[0],D[0])+1, min(A[1],B[1],C[1],D[1])-1, max(A[1],B[1],C[1],D[1])+1]) #taille
    E=[(A[0]+B[0])/2,(A[1]+B[1])/2]
    F=[(C[0]+D[0])/2,(C[1]+D[1])/2]
    I=[(E[0]-F[0])/4+F[0],(E[1]-F[1])/4+F[1]]
    J=[(F[0]-E[0])/4+E[0],(F[1]-E[1])/4+E[1]]
    plt.plot([A[0],J[0],I[0],C[0]],[A[1],J[1],I[1],C[1]],"b", linewidth = 2)
    plt.plot([B[0],J[0],I[0],D[0]],[B[1],J[1],I[1],D[1]],"b", linewidth = 2)
    plt.plot([I[0]],[I[1]], "r", marker = 'o', markersize=10) #tête
    plt.text(A[0], A[1], "PG")
    plt.text(B[0], B[1], "PD")
    plt.text(C[0], C[1],"MG")
    plt.text(D[0], D[1],"MD")
    plt.axis('equal')
    #plt.show()

def dessin_escalade(Lprises, Lmouv): #Lmouv est le liste des positions successives
    l = len(Lmouv)
    q = l//4
    for i in range(q+1):
        for j in range(4):
            if (4*i+j)<l:
                pos=Lmouv[4*i+j]
                plt.subplot(q+1,4,4*i+j+1)
                n,mp=type_de_pos(pos)
                if n==4:
                    dessin4(pos, Lprises)
                elif n==3.1:
                    dessin31(pos, Lprises)
                elif n==3.2:
                    dessin32(pos, Lprises)
    plt.show()
    
#Fonction produit scalaire AB.CD
def sc(A,B,C,D):
    return((B[0]-A[0])*(D[0]-C[0])+(B[1]-A[1])*(D[1]-C[1]))

#fonction projection parallèle de CD sur AB
def ppara(A,B,C,D):
    return(((B[0]-A[0])*sc(A,B,C,D)/d(A,B)**2),(B[1]-A[1])*sc(A,B,C,D)/d(A,B)**2)
    
#fonction projection perpendiculaire à AB de CD 
def pper(A,B,C,D):
    return(D[0]-C[0]-ppara(A,B,C,D)[0],D[1]-C[1]-ppara(A,B,C,D)[1])

#fonction à droite : true si C est à droite de la droite AB (A en bas, B en haut)
def adroite(A,B,C):
    return(pper(A,B,A,C)[0]>=0)

#fonction cosinus cos(a,b,c)=cos de l'angle entre ab et ac
def cossc(A,B,C):
    return(sc(A,B,A,C)/d(A,B)/d(A,C))

#fonction rotation d'un vecteur AB de l'angle t autour de A (donne les coordonnées de B')
#ATTENTION argument = cos(t) et non t
def rot(A,B,cost):
    sint=sqrt(1-cost**2)
    x=cost*(B[0]-A[0])+sint*(B[1]-A[1])+A[0]
    y=-sint*(B[0]-A[0])+cost*(B[1]-A[1])+A[1]
    return((x,y))

#fonction cos d'après al-kachi entre cotés de longueurs a et b, le 3eme de longueur c
def cosAlK(a,b,c):
    return((a**2+b**2-c**2)/2/a/b)

