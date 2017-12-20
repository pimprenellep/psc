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
    x=cost*(B[0]-A[0])+sint*(B[1]-A[1])+A[0]
    y=-sint*(B[0]-A[0])+cost*(B[1]-A[1])+A[1]
    return((x,y))

#fonction cos d'après al-kachi entre cotés de longueurs a et b, le 3eme de longueur c
def cosAlK(a,b,c):
    return((a**2+b**2-c**2)/2/a/b)

#fonction PIED DROIT bouge. A=Pied Gauche, B=l'une des mains. C=prise potentielle Pied Droit
def PDpeutatteindreC(A,B,C,alpha):
    if C[1]>=B[1]:
        return(False) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return(False)
        if dab>=b+t:
            return(PDcas1(A,B,C,alpha))
        if dab>=j:
            return(PDcas2(A,B,C,alpha,dab,j))
        if dab>=dmin:
            return(PDcas2(A,B,C,alpha,dab,dab))

def PDcas1(A,B,C,alpha,dab):
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            return(cos(E,B,C)<=-cos(alpha))
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            return(d(A,C)<=2*j*sin(alpha/2))
        if cossc(B,A,C)>=cosAlK(dab,b+t,j):
            return(d(B,C)<=b+t+j)
        else:
            D=rot(A,E,cosAlK(dab,j,b+t))
            return(d(D,C)<=j)
    else: #mauvais côté
        F=((A[0]-B[0])*(b+t)/dab+B[0],(A[1]-B[1])*(b+t)/dab+B[1])
        if cossc(F,B,C)<=0:
            return(d(F,C)<=j)
        return((d(pper(A,B,A,C),0)<=j)and(d(ppara(A,B,A,C),0)<=j))

def PDcas2(A,B,C,alpha,dab,l):
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            return(cossc(E,B,C)<=-cos(alpha))
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            return(d(A,C)<=2*j*sin(alpha/2))
        else:
            return(d(A,C)<=j)
    else: #mauvais côté
        if cossc(A,B,C)<=0:
            return(d(F,C)<=j)
        return((d(pper(A,B,A,C),0)<=j)and(d(ppara(A,B,A,C),0)<=l))
        


        
    
    
     


    
