#variables globales : 
#Lprises la listes des prises (cf Noémie)
#j,t,b les longueurs des jambes, tronc, bras(+épaule)
#alpha l'angle max de grand écart

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

# ATTENTION ces fonctions doivent prendre en argument les indices des prises dans Lprises (et non les prises elles-mêmes)
#fonction PIED GAUCHE bouge. A=Pied Droit, B=l'une des mains. C=prise potentielle Pied Gauche
def PGpeutatteindreC3(a,b,c):
    return(PDpeutatteindreC3(c,b,a))

#fonction PIED DROIT bouge. A=Pied Gauche, B=l'une des mains. C=prise potentielle Pied Droit
def PDpeutatteindreC3(a,b,c):
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    if C[1]>=B[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if dab>=b+t:
            return(PDcas1(A,B,C,dab))
        if dab>=j:
            return(PDcas2(A,B,C,dab,j))
        if dab>=dmin:
            return(PDcas2(A,B,C,dab,dab))

def PDcas1(A,B,C,dab):
    hloin=0
    hcroisé=0
    hinstable=0
    hmm=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cos(E,B,C)<=-cos(alpha):
                possible=True
                L=d(pper(E,C,E,3),(0,0))
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
        hinstable = abs(B[0]-(A[0]+C[0])/2)*4/10 #10=10cm, 4 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

def PDcas2(A,B,C,dab,l):
    hloin=0
    hcroisé=0
    hinstable=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cos(E,B,C)<=-cos(alpha):
                possible=True
                L=d(pper(E,C,E,3),(0,0))
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
        hinstable = abs(B[0]-(A[0]+C[0])/2)*4/10 #10=10cm, 4 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

#fonction MAIN GAUCHE bouge. A=l'un des pieds, B=main droite. C=prise potentielle Main Gauche
def MGpeutatteindreC3(a,b,c):
    return(MDpeutatteindreC3(a,c,b))
    
#fonction MAIN DROITE bouge. A=l'un des pieds, B=main gauche. C=prise potentielle Main Droite
def MDpeutatteindreC3(a,b,c):
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    if C[1]<=A[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if dab>=b+t-b:
            return(MDcas1(A,B,C,dab))
        if dab>=dmin:
            return(MDcas2(A,B,C,dab))

def MDcas1(A,B,C,dab):
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
        if cossc(F,B,C)>=0:
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
            L=d(b-pper(A,B,A,C),(0,0))
            if L>=0 :
                possible=True
                if L<dloin :
                    hloin=(dloin-L)*5/dloin
    if possible:
        hinstable = abs(A[0]-(C[0]+B[0])/2)*4/10 #10=10cm, 4 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

def MDcas2(A,B,C,dab):
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
        if cos(F,B,C)<=0:
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
        hinstable = abs(A[0]-(C[0]+B[0])/2)*4/10 #10=10cm, 4 à modifier ?
    return(possible, hcroisé+hloin+hinstable)

def hlibre(pos):
    if (pos[0]==[] or pos[1]==[]): #un pied libre
        h=2
    if (pos[2]==[] or pos[3]==[]): #une main libre
        h=h+2
    return(h)

#def hmm3(pos):
    
#def hmp3(pos):
    
#def htailleprises(pos):

#def hch_p(pos): (2p sur la m prise)

#def hch_m(pos): (2m sur la même prise)
    
#def hsouplesse(pos):
    
def MDpeutatteindreD4(a,b,c,d): #A=pg, B=pd, C=mg
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    D=Lprises[d]
    return(MDpeutatteindreC3(a,c,d) and PDpeutatteindreC3(a,d,b) and MDpeutatteindreC3(b,c,d))

def MGpeutatteindreD4(a,b,c,d): #A=pg, B=pd, C=md
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    D=Lprises[d]
    return(MGpeutatteindreC3(a,c,d) and PDpeutatteindreC3(a,d,b) and MGpeutatteindreC3(b,c,d))

def PDpeutatteindreD4(a,b,c,d): #A=pg, B=mg, C=md
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    D=Lprises[d]
    return(PDpeutatteindreC3(a,c,d) and MDpeutatteindreC3(d,b,c) and PDpeutatteindreC3(a,b,d))

def PGpeutatteindreD4(a,b,c,d): #A=pd, B=mg, C=md
    A=Lprises[a]
    B=Lprises[b]
    C=Lprises[c]
    D=Lprises[d]
    return(PGpeutatteindreC3(a,c,d) and MDpeutatteindreC3(d,b,c) and PDpeutatteindreC3(a,b,d))

