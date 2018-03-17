from positionspossibles import *
from dessin_graphe import *
from math import *

# "presente" cherche si la position pos est déjà dans la listes des positions Lpos, et l'ajoute si elle n'y est pas et l'ajoute aussi à la file et renvoie son indice dans la liste Lpos
#def prise_inf(A,B): #ordre alphabétique avec l'ordonnée en premier, l'abscisse de deuxième
#    if A[1]<B[1]:
#        return(True)
#    elif A[1]>B[1]:
#        return(False)
#    else :
#        return(A[0]<B[0])

#def pos_inf(p,q): #ordre sur les positions : "ordre alphabétique" sur les ordonnées
#    trouve=False
#    i=0
#    while i<4 and (trouve==False):
#        if prise_inf(p[i],q[i]):
#            return(True)
#        elif prise_inf(q[i],p[i]):
#            return(False)
#        else :
#            i=i+1
#    return(False)

#def presente(pos,Lpos,file,dernier,courant): #celle qui marche :)    k=len(Lpos)-1
#    ajoute=False
#    while (k>=0) and (ajoute==False) and (pos_inf(pos,Lpos[k])):
#        k=k-1
#    if k==-1:
#        Lpos = [pos]+Lpos
#        ajoute = True
#        ajout_file(file, pos, dernier, courant)
#    if pos_inf(Lpos[k],pos):
#        Lpos = Lpos[:k+1]+[pos]+Lpos[k+1:]
#        ajoute = True
#        ajout_file(file, pos, dernier, courant)
#    return(ajoute, Lpos)

def echange_xy(L):
    for i in range(len(L)):
        L[i][1],L[i][0]=L[i][0],L[i][1]
    return(L)

def presente(pos,Lpos,file,courant): #Lpos pas ordonnée (OK sans "ajout_file")  Rq : ATTENTION ici pos est une vraie position !!! (pas un indice dans Lpos)
    j=len(Lpos)-1
    trouve=False
    while (j>=0) and (trouve==False):
        if pos==Lpos[j]:
            trouve=True
            ind=j
        else:
            j=j-1
    if j==-1:
        Lpos = Lpos + [pos]
        ind = len(Lpos) - 1
        file, courant = ajout_file(file, ind, courant)
    return(Lpos, ind, file,  courant)

    
# les voisins______________________________________________________________________________________________________________________________________
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

#def hash_prise(p,Lprises):
#    i=0
#    while Lprises[i]!=p:
#        i=i+1
#    return(i)
        
def bashaut4_m(Lprises,pos,Lpos):
    ph = max(Lprises[Lpos[pos][0]][0],Lprises[Lpos[pos][1]][0])
    hmax = Lprises[ph][1]+j+t+b
    i=ph
    while (i<=len(Lprises)-2) and (Lprises[i][1]<hmax):
        i=i+1
    return(ph,i-1)

def bashaut3_m(Lprises,pos,pied,Lpos):
    ph = Lprises[Lpos[pos][pied]][0]
    hmax = Lprises[ph][1]+j+t+b
    i=ph
    while (i<=len(Lprises)-2) and (Lprises[i][1]<hmax):
        i=i+1
    return(ph,i-1)
    
def bashaut4_p(Lprises,pos,Lpos):    
    mb = min(Lprises[Lpos[pos][2]][0],Lprises[Lpos[pos][3]][0])
    hmin = Lprises[mb][1]-b-t-j
    i=mb
    while (i>=0) and (Lprises[i][1]>hmin):
        i=i-1
    return(i+1,mb)

def bashaut3_p(Lprises,pos,main,Lpos):    
    mb = Lprises[Lpos[pos][main]][0]
    hmin = Lprises[mb][1]-b-t-j
    i=mb
    while (i>=0) and (Lprises[i][1]>hmin):
        i=i-1
    return(i+1,mb)


def voisins_de_pos_4prises(pos,Lprises,G,Lpos,file,courant):
    voisins = []
    a=Lpos[pos][0]
    b=Lpos[pos][1]
    c=Lpos[pos][2]
    d=Lpos[pos][3]
    pg=Lprises[a]
    pd=Lprises[b]
    mg=Lprises[c]
    md=Lprises[d]
#bashaut_m = indices dans Lprises de la prise la plus basse qu'on essaye d'attraper avec la main, et " " " la plus haute " " "
    pbas_m, phaut_m = bashaut4_m(Lprises,pos,Lpos)
    for i in range(pbas_m, phaut_m+1):
        I=Lprises[i]
    #md bouge -> pos 4 prises
        if I!=md:
            (possible,diff)=MDpeutatteindreD4(pg,pd,mg,I,Lprises) #A=pg, B=pd, C=mg
            if possible:
                v=[a,b,c,i,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #md bouge, mg pd posés, pg laché -> pos 3 prises
            (possible,diff)=MDpeutatteindreC3(pd,mg,1,I,Lprises,3)
            if possible:
                v=[-1,b,c,i,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #md bouge, mg pg posés, pd laché -> pos 3 prises
            (possible,diff)=MDpeutatteindreC3(pg,mg,I,0,Lprises,3)
            if possible:
                v=[a,-1,c,i,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
    #mg bouge -> pos 4 prises
        if I!= mg :
            (possible,diff)=MGpeutatteindreD4(pg,pd,md,I,Lprises) #A=pg, B=pd, C=md
            if possible:
                v=[a,b,i,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #mg bouge, md pd posés, pg laché -> pos 3 prises
            (possible,diff)=MGpeutatteindreC3(pd,md,I,1,Lprises,3)
            if possible:
                v=[-1,b,i,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #mg bouge, md pg posés, pd laché -> pos 3 prises
            (possible,diff)=MGpeutatteindreC3(pg,md,I,0,Lprises,3)
            if possible:
                v=[a,-1,i,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
#pbas_p = indice dans Lprises de la prise la plus basse qu'on essaye d'attraper avec le pied, phaut_p = " " " la plus haute " " "
    pbas_p, phaut_p = bashaut4_p(Lprises,pos,Lpos)
    for j in range(pbas_p, phaut_p+1):
        J=Lprises[j]
    #pd bouge -> pos 4 prises 
        if J != pd:
            (possible,diff)=PDpeutatteindreD4(pg,mg,md,J,Lprises) #A=pg, B=mg, C=md
            if possible:
                v=[a,j,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #pd bouge, pg mg posés, md lachée -> pos 3 prises
            (possible,diff)=PDpeutatteindreC3(pg, mg,J,2,Lprises,3)
            if possible:
                v=[a,j,c,-1,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #pd bouge, pg md posés, mg lachée -> pos 3 prises
            (possible,diff)=PDpeutatteindreC3(pg,md,J,3,Lprises,3)
            if possible:
                v=[a,j,-1,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
    #pg bouge -> pos 4 prises
        if J != pg:
            (possible,diff)=PGpeutatteindreD4(pd,mg,md,J,Lprises) #A=pd, B=mg, C=md
            if possible:
                v=[j,b,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #pg bouge, pd mg posés, md lachée -> pos 3 prises
            (possible,diff)=PGpeutatteindreC3(pd, mg, J,2,Lprises,3)
            if possible:
                v=[j,b,c,-1,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        #pg bouge, pd md posés, mg lachée -> pos 3 prises
            (possible,diff)=PGpeutatteindreC3(pd, md, J,3,Lprises,3)
            if possible:
                v=[j,b,-1,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
    return(voisins,Lpos,file)

def voisins_de_pos_31prises(pos,Lprises,main,G,Lpos,file,courant): #2 pieds, 1 main, main = 2 si mg, 3 si md
    voisins = [] 
    a=Lpos[pos][0]
    b=Lpos[pos][1]
    c=Lpos[pos][2]
    d=Lpos[pos][3]
    pg=Lprises[a]
    pd=Lprises[b]
    mg=Lprises[c]
    md=Lprises[d]   
    v=[a,b,d,c]+Lpos[pos][4:] #changement de main
    Lpos, k, file, courant=presente(v,Lpos,file,courant)
    cout=hmouvement(pos,k,Lprises,Lpos)
    voisins=voisins+[(k,cout)]
      #vers position 4 prises
    bas_m, haut_m = bashaut4_m(Lprises,pos,Lpos) 
    for i in range(bas_m,haut_m):
        I=Lprises[i]
        if main==2:
            (possible,diff)=MDpeutatteindreD4(pg,pd,mg,I,Lprises)
            if possible:
                v=[a,b,c,i,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        elif main==3:
            (possible,diff)=MGpeutatteindreD4(pg,pd,md,I,Lprises)
            if possible:
                v=[a,b,i,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
      #vers position 3 prises
    bas_p, haut_p = bashaut3_p(Lprises,pos,main,Lpos)
    for i in range(bas_p,haut_p):
        I=Lprises[i]
        if I != pd:
            (possible,diff)=PDpeutatteindreC3(pg,Lprises[Lpos[pos][main]],I,main,Lprises,3) #pd bouge
            if possible:
                v=[a,i,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        if I != pg:        
            (possible,diff)=PGpeutatteindreC3(pd,Lprises[Lpos[pos][main]],I,main,Lprises,3) #pg bouge
            if possible:
                v=[i,b,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
    # for i in range( ): #attention
    # Not sure at all what I am doing, check me !!
    for i in range(bas_m,haut_m):
        I=Lprises[i]
        if pg[1]>=pd[1]: #pd se lache
            if main==2:
                if I != mg:
                    (possible,diff)=MDpeutatteindreC3(pg,mg,I,2,Lprises,3) #md attrape
                    if possible:
                        v=[a,-1,c,i,diff]
                        Lpos, k, file, courant=presente(v,Lpos,file,courant)
                        cout=hmouvement(pos,k,Lprises,Lpos)
                        voisins=voisins+[(k,cout)]
            elif main==3:
                if I != md:
                    (possible,diff)=MGpeutatteindreC3(pg,md,I,2,Lprises,3) #mg attrape
                    if possible:
                        v=[a,-1,i,d,diff]
                        Lpos, k, file, courant=presente(v,Lpos,file,courant)
                        cout=hmouvement(pos,k,Lprises,Lpos)
                        voisins=voisins+[(k,cout)]
        elif pd[1]>=pg[1]: #pg se lache
            if main==2:
                if I != mg:
                    (possible,diff)=MDpeutatteindreC3(pd,mg,I,2,Lprises,3) #md attrape
                    if possible:
                        v=[-1,b,c,i,diff]
                        Lpos, k, file, courant=presente(v,Lpos,file,courant)
                        cout=hmouvement(pos,k,Lprises,Lpos)
                        voisins=voisins+[(k,cout)]
            elif main==3:
                if I != md:
                    (possible,diff)=MGpeutatteindreC3(pd,md,I,2,Lprises,3) #mg attrape
                    if possible:
                        v=[-1,b,i,d,diff]
                        Lpos, k, file, courant=presente(v,Lpos,file,courant)
                        cout=hmouvement(pos,k,Lprises,Lpos)
                        voisins=voisins+[(k,cout)]
    return(voisins,Lpos,file)

def voisins_de_pos_32prises(pos,Lprises,pied,G,Lpos,file,courant): #1 pied, 2 mains, pied=0 si pg, 1 si pied droit
    voisins = []
    a=Lpos[pos][0]
    b=Lpos[pos][1]
    c=Lpos[pos][2]
    d=Lpos[pos][3]
    pg=Lprises[a]
    pd=Lprises[b]
    mg=Lprises[c]
    md=Lprises[d]
    v=[b,a]+Lpos[pos][2:] #changement de pied
    Lpos, k, file, courant=presente(v,Lpos,file,courant)
    cout=hmouvement(pos,k,Lprises,Lpos)
    voisins=voisins+[(k,cout)]
      #vers poition 4 prises
    bas_p, haut_p = bashaut4_p(Lprises,pos,Lpos) 
    for i in range(bas_p,haut_p):
        I=Lprises[i]
        if pied==0:
            (possible,diff)=PDpeutatteindreD4(pg,mg,md,I,Lprises)
            if possible:
                v=[a,i,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        elif pied==1:
            (possible,diff)=PGpeutatteindreD4(pd,mg,md,I,Lprises)
            if possible:
                v=[i,b,c,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
      #vers position 3 prises
    bas_m, haut_m = bashaut3_m(Lprises,pos,pied,Lpos)
    for i in range(bas_m,haut_m):
        I=Lprises[i]
        if I != md:
            (possible,diff)=MDpeutatteindreC3(Lprises[Lpos[pos][pied]],mg,I,pied,Lprises,3) #md bouge
            if possible:
                v=[a,b,c,i,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
        if I != mg:
            (possible,diff)=MGpeutatteindreC3(Lprises[Lpos[pos][pied]],md,I,pied,Lprises,3) #mg bouge
            if possible:
                v=[a,b,i,d,diff]
                Lpos, k, file, courant=presente(v,Lpos,file,courant)
                cout=hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
    pbas_p, phaut_p = bashaut4_p(Lprises,pos,Lpos)
    for i in range(pbas_p, phaut_p+1):
        I=Lprises[i]    
        (possible,diff)=MGpeutatteindreC3(I,md,mg,pied,Lprises,3) #le pied bouge -> attention heuristique dynamique
        if possible:
            v=[i,b,c,d,diff]
            Lpos, k, file, courant=presente(v,Lpos,file,courant)
            cout=hmouvement(pos,k,Lprises,Lpos)
            voisins=voisins+[(k,cout)]
            w=[a,i,c,d,diff]
            Lpos, l, file, courant=presente(w,Lpos,file,courant)
            cout=hmouvement(pos,l,Lprises,Lpos)
            voisins=voisins+[(l,cout)]
    return(voisins,Lpos,file)

# gestion de la file_______________________________________________________________________________________________________________________________
#def ajout_file2(file,pos,dernier,courant):
#    long=len(file)
#    if dernier==long-1:
#        dernier=0
#    else:
#        dernier=dernier+1
#    if file[dernier] == -1:
#        file[dernier]=pos
#    else:
#        file=file+[-1]*long
#        for j in range(0,courant):
#            file[j+long]=file[j]
#            file[j]=-1
#        dernier = dernier + long
#        long=long*2
#        file[dernier]=pos
#    return(file,dernier,courant) 

def ajout_file(file,pos,courant):
    file=file+[pos]
    return(file,courant) 

#def retirer_file2(file, dernier, courant):
#    file[courant]=-1
#    if courant==len(file)-1:
#        courant=0
#    else:
#        courant = courant+1
#    return(file,dernier,courant)

def retirer_file(file, courant):
    file[courant]=-1
    if courant<len(file)-1:
        courant = courant+1
    return(file,courant)

#file, der, cou = ajout_file(file, 2, der, cou)
#print(file, der,cou)

#file, der, cou = retirer_file(file, der, cou)
#print(file, der,cou)

#heuristiques mouvement___________________________________________________________________________________________________________________________
#i est la position initiale, f la position finale. ce sont les vraies positions (celles de Lpos)
#i=a,b,c,d --- f=ap,bp,cp,dp

def bary(pos):
    a,b,c,d = pos[0],pos[1],pos[2],pos[3]
    tdp,m = type_de_pos([-1 if pos[i]==[] else 0 for i in range(4)])
    if tdp == 4:
        return([(a[0]+b[0]+c[0]+d[0])/4,(a[1]+b[1]+c[1]+d[1])/4])
    elif tdp == 3.1:
        return([(a[0]+b[0]+pos[m][0])/3,(a[1]+b[1]+pos[m][1])/3])
    elif tdp == 3.2:
        return([(c[0]+d[0]+pos[m][0])/3,(c[1]+d[1]+pos[m][1])/3])

def hgrandmouv(a,b,c,d,ap,bp,cp,dp):
    i = [a,b,c,d]
    f = [ap,bp,cp,dp]
    tdp1 = type_de_pos(i)[0]
    tdp2 = type_de_pos(f)[0]
    bi,bf = bary(i),bary(f)
    if tdp1 != tdp2:
        dist = distance([bi[0]*3,bi[1]*3],[bf[0]*4,bf[1]*4])
    if tdp1 == 4:
        dist = distance(bi,bf)*4
    else:
        dist = distance(bi,bf)*3
    return(dist/10*2) # 2 à changer
    
def htravailgrav(a,b,c,d,ap,bp,cp,dp):
    i = [a,b,c,d]
    f = [ap,bp,cp,dp]
    return( (bary(f)[1]-bary(i)[1])/10*1 )  #1 à changer

def hpetitappui(a,b,c,d,ap,bp,cp,dp, Lprises):
    p1=[a,b,c,d]
    p2=[ap,bp,cp,dp]
    tdp1 = type_de_pos(p1)
    tdp2 = type_de_pos(p2)
    somme_tailles = 0
    for i in range(4): #trouver les appuis
        if ((p1[i]==p2[i]) and (p1[i] != -1)):
            somme_tailles = somme_tailles + Lprises[p1[i]][3]
    return(somme_tailles)

def hdynamique(a,b,c,d,ap,bp,cp,dp):
    i = [a,b,c,d]
    f = [ap,bp,cp,dp]
    tdp1 = type_de_pos([a,b,c,d])[0]
    tdp2 = type_de_pos([ap,bp,cp,dp])[0]
    bi,bf = bary(i),bary(f)
    if (tdp1==3) and (tdp2==3):
        dist = d(bi,bf)*3
        return(dist/10*0.5) #0.5 à changer
    else :
        return(0)

def hadherence(a,b,c,d,ap,bp,cp,dp):
    p1 = [a,b,c,d]
    p2 = [ap,bp,cp,dp]
    tdp1 = type_de_pos(p1)
    tdp2 = type_de_pos(p2)
    if ((tdp1 == tdp2) and (tdp1[0]==3.2)):
        return(d(p1[tdp1[1]],p2[tdp1[1]])/10*3) #3 à changer
    else:
        return(0)

def hinst(a,b,c,d,ap,bp,cp,dp):
    
    return(1)

    
def hmouvement(i,f,Lprises,Lpos):
    a=Lprises[Lpos[i][0]]
    b=Lprises[Lpos[i][1]]
    c=Lprises[Lpos[i][2]]
    d=Lprises[Lpos[i][3]]
    ap=Lprises[Lpos[f][0]]
    bp=Lprises[Lpos[f][1]]
    cp=Lprises[Lpos[f][2]]
    dp=Lprises[Lpos[f][3]]
    return((hgrandmouv(a,b,c,d,ap,bp,cp,dp) + htravailgrav(a,b,c,d,ap,bp,cp,dp)
        + hinst(a,b,c,d,ap,bp,cp,dp) + hdynamique(a,b,c,d,ap,bp,cp,dp) +
        hadherence(a,b,c,d,ap,bp,cp,dp))/hpetitappui(*Lpos[i][0:4],
            *Lpos[f][0:4], Lprises))


# le graphe
def creegraphe(Lprises, ini):
    #Lprises=echange_xy(Lprises)
    G=[]
    Lpos=[ini]
    file=[0] #ce sont des indices des positions dans la liste "Lpos"
    courant=0 #ce sont des indices des positions dans la liste "file"
    #itérations....
    while file[courant] >= 0:
        nb,p_m= type_de_pos(Lpos[courant])
        if nb==4:
            voisins_de_courant,Lpos,file = voisins_de_pos_4prises(file[courant],Lprises,G,Lpos,file,courant)
        elif nb==3.1:
            voisins_de_courant,Lpos,file = voisins_de_pos_31prises(file[courant],Lprises,p_m,G,Lpos,file,courant)
        elif nb==3.2:
            voisins_de_courant,Lpos,file = voisins_de_pos_32prises(file[courant],Lprises,p_m,G,Lpos,file,courant)
        G=G+[voisins_de_courant]
        file, courant = retirer_file(file, courant)
    dessin_graphe(G, Lpos, Lprises)
    return(G,Lpos, len(G), len(Lpos))


## CHECK LIST
# dans "présente", ajouter les nouvelles positions trouvées à la file 
#voisins de pos 4 prises : ajouter 2 memebres en même temps
#les arguments de toutes les fonctions (Lprises, Lpos ? G?)
#arguments de voisin_de_pos3 : pied, main (modifier type_de_prise)
# mettre à jour le graphe après la recherche des voisins de chaque prise
# gestion de la file pour ajout dedans et retirer (cf papier)
#les heuristiques...
