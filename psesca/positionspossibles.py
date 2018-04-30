#variables globales : 
#Lprises la listes des prises (cf Noémie)
#j,t,b les longueurs des jambes, tronc, bras(+épaule)
#alpha l'angle max de grand écart

from math import *

"""FIX ME
à voir avec morphology : 
 
"""

b=0.6
t=0.55
j=1
alpha=1.8 #environ 103 degrés
dmin=0.50
dloin=0.15
dsouple=0.20
d2pieds=0.12
d2mains=0.12
dproche=0.5


#fontion distance
def d(A,B):
    return(sqrt((A[0]-B[0])**2+(A[1]-B[1])**2))
# naming conflict-fre version
distance = d

#Fonction produit scalaire AB.CD
def sc(A,B,C,D):
    return((B[0]-A[0])*(D[0]-C[0])+(B[1]-A[1])*(D[1]-C[1]))

#fonction projection parallèle de CD sur le vect unitaire dans la direction de AB
def ppara(A,B,C,D):
    return(((B[0]-A[0])*sc(A,B,C,D)/d(A,B)**2),(B[1]-A[1])*sc(A,B,C,D)/d(A,B)**2)
    
#fonction projection perpendiculaire au vect unitaire dans la direction de AB de CD 
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
def PGpeutatteindreC3(A,B,C,main,Lprises,n):
    return(PDpeutatteindreC3(C,B,A, main, Lprises,n))

#fonction PIED DROIT bouge. A=Pied Gauche, B=l'une des mains (main = 2 ou 3), C=prise potentielle Pied Droit
def PDpeutatteindreC3(A,B,C,main,Lprises,n): 
    if C[1]>=B[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if A==C:                  # !!!!!!!!!!!!!!!!!!!!!!!!!! ATTENTION CHANGER HCH_P !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #if A[3]<=d2pieds:
                #hch_p=6*(10/A[3]-10/d2pieds)/B[3] #/b3 car c'est plus dur de changer de pied quand la prise de main est petite, 6 à changer
            return((True,5))   #hch_p)) 
        elif dab>=b+t:
            return(PDcas1(A,B,C,main,dab,Lprises,n))
        elif dab>=j:
            return(PDcas2(A,B,C,main,dab,j,Lprises,n))
        elif dab>=dmin:
            return(PDcas2(A,B,C,main,dab,dab,Lprises,n))

def PDcas1(A,B,C,main,dab,Lprises,n):
    h=0
    hloin=0
    hcroisé=0
    hinst=0
    hsouple=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cossc(E,B,C)<=-cos(alpha):
                possible=True
                G = rot(E,A,cos(alpha))
                L=d(pper(E,G,E,C),(0,0))
                hloin=h_loin(L)
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            L=2*j*sin(alpha/2)-d(A,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)
        if cossc(B,A,C)>=cosAlK(dab,b+t,j):
            possible=(d(B,C)<=b+t+j)
        else:
            D=rotinv(A,E,cosAlK(dab,j,b+t))
            L=j-d(D,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)
    else: #mauvais côté
        hcroisé=1 #1 à modifier ?
        F=((A[0]-B[0])*(b+t)/dab+B[0],(A[1]-B[1])*(b+t)/dab+B[1])
        if cossc(F,B,C)<=0:
            L=j-d(F,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)
        L=j-d(pper(A,B,A,C),(0,0))
        M=j-d(ppara(A,B,A,C),(0,0))
        if ((L>=0) and (M>=0)):
            possible=True
            hloin=h_loin(L) + h_loin(M)
    if possible:
        hinst = abs(B[0]-(A[0]+C[0])/2)/distance(B,[(C[0]+A[0])/2,(C[1]+A[1])/2])*7 #7 à modifier ?
        L=dsouple-abs(d(pper(A,B,A,C),(0,0)))
        if L>=0:
            hsouple=L/10*(d(A,B)/(j+t+b))**2*7 # 7 à modifier ?
        if n==3:
            h = (hcroisé+hloin+hsouple+hinst + hmm3(A,B,C,main) + hproche31(A,C,B))/htailleprises(A,B,C,main)  #  /(A[3]+B[3]+C[3])
        elif n==4:
            h=hcroisé+hloin+hsouple
    return(possible, h)

def PDcas2(A,B,C,main,dab,l,Lprises,n):
    h=0
    hloin=0
    hcroisé=0
    hinst=0
    hsouple=0
    possible=False
    if adroite(A,B,C): #bon côté
        E=((B[0]-A[0])*j/dab+A[0],(B[1]-A[1])*j/dab+A[1])
        if cossc(A,B,C)>cos(alpha/2):
            if cossc(E,B,C)<=-cos(alpha):
                possible=True
                G = rot(E,A,cos(alpha))
                L=d(pper(E,G,E,C),(0,0))
                hloin=h_loin(L)
        if cossc(A,B,C)>=cos(acos(cosAlK(dab,j,b+t))+pi/2-alpha/2):
            L=2*j*sin(alpha/2)-d(A,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)
        if d(A,C)<=j:
            possible=True
        else:
            D=rotinv(A,E,cosAlK(dab,j,b+t))
            L=j-d(D,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)          
    else: #mauvais côté
        hcroisé=2 # 2 à changer ?
        if cossc(A,B,C)<=0:
            L=j-d(A,C)
            if L>=0 :
                possible=True
                hloin=h_loin(L)
        L=j-d(pper(A,B,A,C),(0,0))
        M=l-d(ppara(A,B,A,C),(0,0))
        if ((L>=0) and (M>=0)):
            possible=True
            hloin=h_loin(L) + h_loin(M)                
    if possible:
        hinst = abs(B[0]-(A[0]+C[0])/2)/distance(B,[(C[0]+A[0])/2,(C[1]+A[1])/2])*7 #7 à modifier ?
        L=dsouple-abs(d(pper(A,B,A,C),(0,0)))
        if L>=0:
            hsouple=L/10*(d(A,B)/(j+t+b))**2*7 #7 à modifier ?
        if n==3:
            #h =  (hcroisé+hloin+hsouple+hinst )/htailleprises(A,B,C,main)
            h =  (hcroisé+hloin+hsouple+hinst + hmm3(A,B,C,main) + hproche31(A,C,B))/htailleprises(A,B,C,main) # /(A[3]+B[3]+C[3])
        elif n==4:
            h =  hcroisé+hloin+hsouple
    return(possible, h)

#fonction MAIN GAUCHE bouge. A=l'un des pieds (pied = 0 ou 1), B=main droite. C=prise potentielle Main Gauche
def MGpeutatteindreC3(A,B,C,pied,Lprises,n):
    return(MDpeutatteindreC3(A,C,B, pied, Lprises,n))
    
#fonction MAIN DROITE bouge. A=l'un des pieds, B=main gauche. C=prise potentielle Main Droite
def MDpeutatteindreC3(A,B,C,pied,Lprises,n):
    if C[1]<=A[1]:
        return((False,0)) #attention à l'ordre des arguments
    else:
        dab=d(A,B)
        if ((dab>b+t+j)or(dab<dmin)):
            return((False,0))
        if B==C:                                       # !!!!!!!!!!!!!!!!!!!!! ATTENTION CHANGER HCH_M !!!!!!!!!!!!!!!!!
            #if B[3]<=d2mains:
                #hch_m=4*(10/B[3]-10/d2mains)/A[3] #/b3 car c'est plus dur de changer de main quand la prise de pied est petite, 4 à changer
            return((True,5)) # hch_m)) 
        elif dab>=j+t-b:
            return(MDcas1(A,B,C,pied,dab,Lprises,n))
        elif dab>=dmin:
            return(MDcas2(A,B,C,pied,dab,Lprises,n))

def MDcas1(A,B,C,pied,dab,Lprises,n):
    h=0
    hloin=0
    hcroisé=0
    hinst=0
    possible=False
    E=((A[0]-B[0])*b/dab+B[0],(A[1]-B[1])*b/dab+B[1])
    if cossc(B,A,C)>=cosAlK(dab,b,t+j):
        L=2*b-d(B,C)
        if L>=0 :
            possible=True
            hloin=h_loin(L)
    D=rot(B,E,cosAlK(dab,b,j+t))
    if cossc(D,B,C)<=-cosAlK(b,t+j,dab):
        L=b-d(D,C)
        if L>=0 :
            possible=True
            hloin=h_loin(L)
    else:
        L=j+t+b-d(A,C)
        if L>=0 :
            possible=True
            hloin=h_loin(L)
    if possible:
        hinst = abs(A[0]-(C[0]+B[0])/2)/distance(A,[(C[0]+B[0])/2,(C[1]+B[1])/2])*8 #8 à modifier ?
        if n==3:
            h = (hcroisé+hloin+hinst + hmp3(A,B,C,pied) + hproche32(A,B,C))/htailleprises(A,B,C,pied)  # /(A[3]+B[3]+C[3])
        elif n==4:
            h=hcroisé+hloin
        if not(adroite(A,B,C)): #mauvais côté
            hcroise=3*(1+cossc(B,A,C))**2 #3 à changer #1 à changer ?
    return(possible, h)
        
"""        if cossc(E,A,C)>=0:
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
"""

def MDcas2(A,B,C,pied,dab,Lprises,n):
    h=0
    hloin=0
    hcroisé=0
    hinst=0
    possible=False
    L=2*b-d(B,C)
    if L>=0 :
        possible=True
        hloin=h_loin(L)
    if not(adroite(A,B,C)):
        hcroise=3*(1+cossc(B,A,C))**2 #3 à changer
    if possible:
        hinst = abs(A[0]-(C[0]+B[0])/2)/distance(A,[(C[0]+B[0])/2,(C[1]+B[1])/2])*8 # 8 à modifier ?
        if n==3:
            h = (hcroisé+hloin+hinst + hmp3(A,B,C,pied)+hproche32(A,B,C))/htailleprises(A,B,C,pied)   # /(A[3]+B[3]+C[3])
        elif n==4:
            h=hcroisé+hloin
    return(possible, h)
    
#    if adroite(A,B,C): #bon côté
#        L=2*b-d(B,C)
#        if L>=0 :
#            possible=True
#            if L<dloin :
#                hloin=(dloin-L)*5/dloin 
#    else: #mauvais côté
#        hcroisé = 1 #1 à changer ?
#        if cossc(B,A,C)<=0:
#            L=b-d(B,C)
#            if L>=0 :
#                possible=True
#                if L<dloin :
#                    hloin=(dloin-L)*5/dloin
#        F=((B[0]-A[0])*(t+j)/dab+A[0],(B[1]-A[1])*(t+j)/dab+A[1])
#        if cossc(F,B,C)<=0:
#            L=b-d(B,C)
#            if L>=0 :
#                possible=True
#                if L<dloin :
#                    hloin=(dloin-L)*5/dloin
#        else:
#            L=b-d(pper(A,B,A,C),(0,0))
#            if L>=0 :
#                possible=True
#                if L<dloin :
#                    hloin=(dloin-L)*5/dloin
    

#def hlibre(pos):

#A,B,C des codes *peutatteindre*
def mp(A,B,C):
    return(abs(A[0]-(B[0]+C[0])/2)/10*20) #20 à changer
    
"""    t1=(B[0]-A[0])/d(A,B)
    t2=(C[0]-A[0])/d(A,C)
    hmp=abs(t1+t2)/2*40 #40 à changer
    return(hmp) """

def hmp3(A,B,C,pied):
    if pied==0:
        if A[0]>=(B[0]+C[0])/2:
            return(mp(A,B,C))
        else:
            return(0)
    elif pied==1:
        if A[0]<=(B[0]+C[0])/2:
            return(mp(A,B,C))
        else:
            return(0)

def h_loin(L):
    if L<dloin :
        return((dloin-L)*2/dloin) #1 à changer
    else:
        return(0)

def mm(A,B,C):
    return(abs(B[0]-(A[0]+C[0])/2)/10*15) #15 à changer ?
    
"""    t1=(B[0]-A[0])/d(A,B)
    t2=(B[0]-C[0])/d(C,B)
    hmm=abs(t1+t2)/2*15 #15 à changer
    return(hmm)  """
    
def hmm3(A,B,C,main):
    if main==2 :
        if B[0]<=(A[0]+C[0])/2:
            return(mm(A,B,C))
        else:
            return(0)
    elif main==3 :
        if B[0]>=(A[0]+C[0])/2:
            return(mm(A,B,C))
        else:
            return(0)

def hproche31(pg,pd,m): #les arguments sont des vraies prises
    hp=0
    dmin = min(distance(pg,m),distance(pd,m))
    if dmin<dproche:
        hp=(1-dmin/dproche)*2 #2 à changer
    return(hp)

def hproche32(p,mg,md): #les arguments sont des vraies prises
    hp=0
    dmin = min(distance(p,mg),distance(p,md))
    if dmin<dproche:
        hp=(1-dmin/dproche)*2 #2 à changer
    return(hp)

def hproche4(a,b,c,d): #a=pg, b=pd, c=mg, d=md
    if a[0]<=b[0]:
        gp,dp=a,b
    else:
        gp,dp=b,a
    if c[0]<=d[0]:
        gm,dm=c,d
    else:
        gm,dm=d,c
    dmax = max(distance(gm,gp),distance(dm,dp))
    return(3*dproche/dmax) # 3 à changer

def hinstable(a,b,c,d): #a=pg, b=pd, c=mg, d=md
    E = [(a[0]+b[0])/2,(a[1]+b[1])/2]
    F = [(c[0]+d[0])/2,(c[1]+d[1])/2]
    sina = abs(F[0]-E[0])/distance(E,F) #inclinaison
    #g = [(a[0]+b[0]+c[0]+d[0])/4,(a[1]+b[1]+c[1]+d[1])/4] #barycentre des prises
    #cdg = abs(g[0]-E[0])/10
    #return((sina/3+2/3*cdg)*7) # 7 à changer
    return(sina*1) # 1 à changer

def htailleprises(a,b,c,d):   #   /!\ ATTENTION CHANGER L'HEURISTIQUE
    return(1)

    
def MDpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=pd, C=mg
    b1,h1 = MGpeutatteindreC3(a,c,d, 0, Lprises,4)
    b2,h2 = PDpeutatteindreC3(a,d,b, 3,Lprises,4) 
    b3,h3 = MDpeutatteindreC3(b,c,d, 1,Lprises,4)
    b4,h4 = PDpeutatteindreC3(a,c,b, 2,Lprises,4)
    if (b1 and b2 and b3 and b4):
        hpr = hproche4(a,b,c,d)
        hinst = hinstable(a,b,c,d)
        h = (max(h1,h2,h3,h4) + hpr + hinst)/htailleprises(a,b,c,d)  # /(a[3]+b[1]+c[2]+d[3])
        return(True,h)
    else :
        return(False, 0)

def MGpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=pd, C=md
    b1,h1 = MGpeutatteindreC3(a,c,d, 0,Lprises,4)
    b2,h2 = PDpeutatteindreC3(a,d,b, 3,Lprises,4)
    b3,h3 = MDpeutatteindreC3(b,c,d, 1,Lprises,4)
    if (b1 and b2 and b3):
        hpr = hproche4(a,b,d,c)
        hinst = hinstable(a,b,d,c)
        h = (max(h1,h2,h3) + hpr + hinst)/htailleprises(a,b,c,d)   # /(a[3]+b[1]+c[2]+d[3])
        return(True,h)
    else :
        return(False, 0)

def PDpeutatteindreD4(a,b,c,d,Lprises): #A=pg, B=mg, C=md
    b1,h1 = PDpeutatteindreC3(a,c,d, 3,Lprises,4)
    b2,h2 = MDpeutatteindreC3(d,b,c, 1,Lprises,4)
    b3,h3 = PDpeutatteindreC3(a,b,d, 2,Lprises,4)
    b4,h4 = MDpeutatteindreC3(a,b,c, 0,Lprises,4)
    if (b1 and b2 and b3 and b4):
        hpr = hproche4(a,d,b,c)
        hinst = hinstable(a,d,b,c)
        h = (max(h1,h2,h3,h4) + hpr + hinst)/htailleprises(a,b,c,d)  #  /(a[3]+b[1]+c[2]+d[3])
        return(True,h)
    else :
        return(False, 0)

def PGpeutatteindreD4(a,b,c,d,Lprises): #A=pd, B=mg, C=md
    b1,h1 = PGpeutatteindreC3(a,c,d, 3,Lprises,4)
    b2,h2 = MDpeutatteindreC3(d,b,c, 0,Lprises,4)
    b3,h3 = PGpeutatteindreC3(a,b,d, 2,Lprises,4)
    b4,h4 = MDpeutatteindreC3(a,b,c, 1,Lprises,4)
    if (b1 and b2 and b3 and b4):
        hpr = hproche4(d,a,b,c)
        hinst = hinstable(d,a,b,c)
        h = (max(h1,h2,h3,h4) + hpr + hinst)/htailleprises(a,b,c,d)  #  /(a[3]+b[1]+c[2]+d[3])
        return(True,h)
    else :
        return(False, 0)
    

""" questions pour Etienne
comment accéder à la tailles des prises donnée par le traitement de photo ?
comment tester tout avec une autre voie (par ex la 6b orange ?

questions pour Noémie :
ajouter à la fin de djikstra le schéma de la montée de la voie ("dessin_escalade")
renverser la liste des positions (du bas vers le haut
"""
