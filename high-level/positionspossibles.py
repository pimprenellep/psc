#variables globales : 
#Lprises la listes des prises (cf Noémie)
#j,t,b les longueurs des jambes, tronc, bras(+épaule)
#alpha l'angle max de grand écart

from math import *

b=80
t=50
j=100
alpha=1.8
dmin=50
dloin=20
dsouple=20


#fontion distance
def d(A,B):
    return(sqrt((A[0]-B[0])**2+(A[1]-B[1])**2))

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
    x=cost*(B[0]-A[0])-sint*(B[1]-A[1])+A[0]
    y=sint*(B[0]-A[0])+cost*(B[1]-A[1])+A[1]
    return((x,y))
    
def rotinv(A,B,cost):
    sint=sqrt(1-cost**2)
    x=cost*(B[0]-A[0])+sint*(B[1]-A[1])+A[0]
    y=-sint*(B[0]-A[0])+cost*(B[1]-A[1])+A[1]
    return((x,y))

#fonction cos d'après al-kachi entre cotés de longueurs a et b, le 3eme de longueur c
def cosAlK(a,b,c):
    return((a**2+b**2-c**2)/2/a/b)

# ATTENTION ces fonctions prennent en argument les prises elles-mêmes!
#fonction PIED GAUCHE bouge. A=Pied Droit, B=l'une des mains. C=prise potentielle Pied Gauche
def PGpeutatteindreC3(A,B,C,Lprises):
    return(PDpeutatteindreC3(C,B,A,Lprises))

#fonction PIED DROIT bouge. A=Pied Gauche, B=l'une des mains. C=prise potentielle Pied Droit
def PDpeutatteindreC3(A,B,C,Lprises):
    if C[1]>=B[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if A==C:
            if A[3]<=d2pieds:
                hch_p=6*(10/A[3]-10/d2pieds)/B[3] #/b3 car c'est plus dur de changer de pied quand la prise de main est petite, 6 à changer
            return((True,hch_p)) 
        elif dab>=b+t:
            return(PDcas1(A,B,C,dab,Lprises))
        elif dab>=j:
            return(PDcas2(A,B,C,dab,j,Lprises))
        elif dab>=dmin:
            return(PDcas2(A,B,C,dab,dab,Lprises))

def PDcas1(A,B,C,dab,Lprises):
    hloin=0
    hcroisé=0
    hinstable=0
    hmm=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cossc(E,B,C)<=-cos(alpha):
                possible=True
                G = rot(E,A,cos(alpha))
                L=d(pper(E,G,E,C),(0,0))
                if L<dloin:
                    hloin=(dloin-L)*5/dloin
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            L=2*j*sin(alpha/2)-d(A,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        if cossc(B,A,C)>=cosAlK(dab,b+t,j):
            possible=(d(B,C)<=b+t+j)
        else:
            D=rotinv(A,E,cosAlK(dab,j,b+t))
            L=j-d(D,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
    else: #mauvais côté
        hcroisé=2 #2 à modifier ?
        F=((A[0]-B[0])*(b+t)/dab+B[0],(A[1]-B[1])*(b+t)/dab+B[1])
        if cossc(F,B,C)<=0:
            L=j-d(F,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        L=j-d(pper(A,B,A,C),(0,0))
        M=j-d(ppara(A,B,A,C),(0,0))
        if ((L>=0) and (M>=0)):
            possible=True
            if L<dloin :
                hloin=hloin + (dloin-L)*5/dloin
            if M<dloin :
                hloin=hloin + (dloin-M)*5/dloin
    if possible:
        hinstable = abs(B[0]-(A[0]+C[0])/2)*7/10 #10=10cm, 7 à modifier ?
        L=dsouple-abs(pper(A,B,A,C))
        if L>=0:
            hsouple=L/10*(d(A,B)/(j+t+b))**2*10
    return(possible, hcroisé+hloin+hinstable+hsouple)

def PDcas2(A,B,C,dab,l,Lprises):
    hloin=0
    hcroisé=0
    hinstable=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cossc(E,B,C)<=-cos(alpha):
                possible=True
                G = rot(E,A,cos(alpha))
                L=d(pper(E,G,E,C),(0,0))
                if L<dloin:
                    hloin=(dloin-L)*5/dloin
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            L=2*j*sin(alpha/2)-d(A,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        if d(A,C)<=j:
            possible=True
        else:
            D=rotinv(A,E,cosAlK(dab,j,b+t))
            L=j-d(D,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin           
    else: #mauvais côté
        hcroisé=2
        if cossc(A,B,C)<=0:
            L=j-d(A,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        L=j-d(pper(A,B,A,C),(0,0))
        M=l-d(ppara(A,B,A,C),(0,0))
        if ((L>=0) and (M>=0)):
            possible=True
            if L<dloin :
                hloin=hloin + (dloin-L)*5/dloin
            if M<dloin :
                hloin=hloin + (dloin-M)*5/dloin
    if possible:
        hinstable = abs(B[0]-(A[0]+C[0])/2)*7/10 #10=10cm, 7 à modifier ?
        L=dsouple-abs(pper(A,B,A,C))
        if L>=0:
            hsouple=L/10*(d(A,B)/(j+t+b))**2*10
    return(possible, hcroisé+hloin+hinstable+hsouple)

#fonction MAIN GAUCHE bouge. A=l'un des pieds, B=main droite. C=prise potentielle Main Gauche
def MGpeutatteindreC3(A,B,C,Lprises):
    return(MDpeutatteindreC3(A,C,B,Lprises))
    
#fonction MAIN DROITE bouge. A=l'un des pieds, B=main gauche. C=prise potentielle Main Droite
def MDpeutatteindreC3(A,B,C,Lprises):
    if C[1]<=A[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if B==C:
            if B[3]<=d2mains:
                hch_m=4*(10/B[3]-10/d2mains)/A[3] #/b3 car c'est plus dur de changer de main quand la prise de pied est petite, 4 à changer
            return((True,hch_m)) 
        elif dab>=b+t-b:
            return(MDcas1(A,B,C,dab,Lprises))
        elif dab>=dmin:
            return(MDcas2(A,B,C,dab,Lprises))

def MDcas1(A,B,C,dab,Lprises):
    hloin=0
    hcroisé=0
    hinstable=0
    possible=False
    E=((A[0]-B[0])*b/dab+B[0],(A[1]-B[1])*b/dab+B[1])
    if adroite(A,B,C): #bon côté
        if cossc(B,A,C)>=cosAlK(dab,b,t+j):
            L=2*b-d(B,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        D=rot(B,E,cosAlK(dab,b,j+t))
        if cossc(D,B,C)<=-cosAlK(b,t+j,dab):
            L=b-d(D,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        else:
            L=j+t+b-d(A,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
    else: #mauvais côté
        if cossc(E,A,C)>=0:
            L=b-d(E,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        F=((B[0]-A[0])*(t+j)/dab+A[0],(B[1]-A[1])*(t+j)/dab+A[1])
        if cossc(F,A,C)<=0:
            L=b-d(F,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
            elif cossc(A,B,C)>=cosAlK(dab,t+j,b):
                L=b+t+j-d(A,C)
                if L>=0 :
                    possible=True
                    if L<dloin :
                        hloin=(dloin-L)*5/dloin
        else:
            L=b-d(pper(A,B,A,C),(0,0))
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
    if possible:
        hinstable = abs(A[0]-(C[0]+B[0])/2)*7/10 #10=10cm, 7 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

def MDcas2(A,B,C,dab,Lprises):
    hloin=0
    hcroisé=0
    hinstable=0
    possible=False
    if adroite(A,B,C): #bon côté
        L=2*b-d(B,C)
        if L>=0 :
            possible=True
            if L<dloin :
                hloin=(dloin-L)*5/dloin 
    else: #mauvais côté
        if cossc(B,A,C)<=0:
            L=b-d(B,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        F=((B[0]-A[0])*(t+j)/dab+A[0],(B[1]-A[1])*(t+j)/dab+A[1])
        if cossc(F,B,C)<=0:
            L=b-d(B,C)
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
        else:
            L=b-d(pper(A,B,A,C),(0,0))
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
    if possible:
        hinstable = abs(A[0]-(C[0]+B[0])/2)*7/10 #10=10cm, 7 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

def hlibre(pos):
    if (pos[0]==[] or pos[1]==[]): #un pied libre
        h=2
    if (pos[2]==[] or pos[3]==[]): #une main libre
        h=h+2
    return(h)

def mp(A,B,C):
    Bp=[A[0],B[1]]
    Cp=[A[0],C[1]]
    t1=d(Bp,B)/d(A,B)
    t2=d(Cp,C)/d(A,C)
    hmp=(t1+t2)/2*40 #40 à changer
    return(hmp)

def hmp3(pos):
    if pos[0]==-1 :
        A,B,C=pos[1],pos[2],pos[3]
        if A[0]<=min(B[0],C[0]):
            return(mp(A,B,C))
    elif pos[1]==-1 :
        A,B,C=pos[0],pos[2],pos[3]
        if A[0]>=max(B[0],C[0]):
            return(mp(A,B,C))
    
def mm(A,B,C):
    Ap=[B[0],A[1]]
    Cp=[B[0],C[1]]
    t1=d(Ap,A)/d(A,B)
    t2=d(Cp,C)/d(C,B)
    hmm=(t1+t2)/2*20 #20 à changer
    return(hmm)
    
def hmm3(pos):
    if pos[2]==-1 :
        A,C,B=pos[0],pos[1],pos[3]
        if B[0]<=min(A[0],C[0]):
            return(mp(A,B,C))
    elif pos[3]==-1 :
        A,C,B=pos[0],pos[1],pos[2]
        if B[0]>=max(A[0],C[0]):
            return(mp(A,B,C))
    
#def htailleprises(pos):

#def hch_p(pos): #(2p sur la m prise)
    

#def hch_m(pos): #(2m sur la même prise)
    
def hsouplesse(pos):
    if type_de_pos(pos)[0]==3.1:
        L=dsouple-abs(pper(A,B,A,C))
        if L>=0:
            hsouple=L/10*(d(A,B)/(j+t+b))**2*10
    return(hsouple)
            


#Atention : le booléen renvoyé est bon, mais pas l'heuristique
    
def MDpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=pd, C=mg
    return(MDpeutatteindreC3(a,c,d,Lprises) and PDpeutatteindreC3(a,d,b,Lprises) and MDpeutatteindreC3(b,c,d,Lprises))

def MGpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=pd, C=md
    return(MGpeutatteindreC3(a,c,d,Lprises) and PDpeutatteindreC3(a,d,b,Lprises) and MGpeutatteindreC3(b,c,d,Lprises))

def PDpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=mg, C=md
    return(PDpeutatteindreC3(a,c,d,Lprises) and MDpeutatteindreC3(d,b,c,Lprises) and PDpeutatteindreC3(a,b,d,Lprises))

def PGpeutatteindreD4(a,b,c,d,Lprises): #A=pd, B=mg, C=md
    return(PGpeutatteindreC3(a,c,d,Lprises) and MDpeutatteindreC3(d,b,c,Lprises) and PDpeutatteindreC3(a,b,d,Lprises))

