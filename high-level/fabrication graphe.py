## "presente" cherche si la position pos est déjà dans la listes des positions Lpos, et l'ajoute si elle n'y est pas et l'ajoute aussi à la file et renvoie son indice dans la liste Lpos
def prise_inf(A,B): #ordre alphabétique avec l'ordonnée en premier, l'abscisse de deuxième
    if A[1]<B[1]:
        return(True)
    elif A[1]>B[1]:
        return(False)
    else :
        return(A[0]<B[0])

def pos_inf(p,q): #ordre sur les positions : "ordre alphabétique" sur les ordonnées
    trouve=False
    i=0
    while i<4 and (trouve==False):
        if prise_inf(p[i],q[i]):
            return(True)
        elif prise_inf(q[i],p[i]):
            return(False)
        else :
            i=i+1
    return(False)

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

def presente(pos,Lpos,file,dernier,courant): #Lpos pas ordonnée (OK sans "ajout_file")
    k=len(Lpos)-1
    trouve=False
    while (k>=0) and (trouve==False):
        if pos==Lpos[k]:
            trouve=True
            ind=k
        else:
            k=k-1
    if k==-1:
        Lpos = Lpos + [pos]
        file, dernier, courant = ajout_file(file, pos, dernier, courant)
        ind = len(Lpos) - 1
    return(ind, file, dernier, courant)

    
# les voisins______________________________________________________________________________________________________________________________________
def type_de_pos(pos):
    if pos[0]==[]:
        return(3.2,1)
    elif pos[1]==[]:
        return(3.2,0)
    else:
        if pos[2]==[]:
            return(3.1,3)
        elif pos[3]==[]:
            return(3.1,2)
        else:
            return(4,"")

def hash_prise(p,Lprises):
    i=0
    while Lprsies[i]!=p:
        i=i+1
    return(i)
        
def bashaut4_m(Lprises,pos):
    ph = max(hash_prise(pos[0]),hash_prise(pos[1]))
    hmax = Lprises[ph][1]+j+t+b
    i=ph
    while Lprises[i][1]<hmax:
        i=i+1
    return(ph,i-1)

def bashaut3_m(Lprises,pos,pied):
    ph = hash_prise(pos[pied])
    hmax = Lprises[ph][1]+j+t+b
    i=ph
    while Lprises[i][1]<hmax:
        i=i+1
    return(ph,i-1)
    
def bashaut4_p(Lprises,pos):    
    mb = min(hash_prises(pos[2]),hash_prises(pos[3]))
    hmin = Lprises[mb][1]-b-t-j
    i=mb
    while (i>=0) and (Lprises[i][1]>hmin):
        i=i-1
    return(i+1,mb)

def bashaut3_p(Lprises,pos,main):    
    mb = hash_prises(pos[main])
    hmin = Lprises[mb][1]-b-t-j
    i=mb
    while (i>=0) and (Lprises[i][1]>hmin):
        i=i-1
    return(i+1,mb)


def voisins_de_pos_4prises(pos,Lprises,G):
    voisins = []
#bashaut_m = indices dans Lprises de la prise la plus basse qu'on essaye d'attraper avec la main, et " " " la plus haute " " "
    pbas_m, phaut_m = bashaut4_m(Lprises,pos)
    for i in range(pbas_m, phaut_m+1):
    #md bouge -> pos 4 prises
        MDpeutatteindreD4(pos[0],pos[1],pos[2],i)=(possible,diff) #A=pg, B=pd, C=mg
        if possible:
            v=[pos[0],pos[1],pos[2],i,diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #md bouge, mg pd posés, pg laché -> pos 3 prises
        MDpeutatteindreC3(pos[1],pos[2],i)=(possible,diff)
        if possible:
            v=[[],pos[1],pos[2],i,diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #md bouge, mg pg posés, pd laché -> pos 3 prises
        MDpeutatteindreC3(pos[0],pos[2],i)=(possible,diff)
        if possible:
            v=[pos[0],[],pos[2],Lprises[i],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
    #mg bouge -> pos 4 prises
        MGpeutatteindreD4(pos[0],pos[1],pos[3],i)=(possible,diff) #A=pg, B=pd, C=md
        if possible:
            v=[pos[0],pos[1],i,pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #mg bouge, md pd posés, pg laché -> pos 3 prises
        MGpeutatteindreC3(pos[1],pos[3],i)=(possible,diff)
        if possible:
            v=[[],pos[1],i,pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #mg bouge, md pg posés, pd laché -> pos 3 prises
        MGpeutatteindreC3(pos[0],pos[3],i)=(possible,diff)
        if possible:
            v=[pos[0],[],i,pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
#pbas_p = indice dans Lprises de la prise la plus basse qu'on essaye d'attraper avec le pied, phaut_p = " " " la plus haute " " "
    pbas_p, phaut_p = bashaut4_p(Lprises,pos)
    for j in range(pbas_p, phaut_p+1):
    #pd bouge -> pos 4 prises 
        PDpeutatteindreD4(pos[0],pos[2],pos[3],j)=(possible,diff) #A=pg, B=mg, C=md
        if possible:
            v=[pos[0],j,pos[2],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #pd bouge, pg mg posés, md lachée -> pos 3 prises
        PDpeutatteindreC3(pos[0], pos[2], j)=(possible,diff)
        if possible:
            v=[pos[0],j,pos[2],[],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #pd bouge, pg md posés, mg lachée -> pos 3 prises
        PDpeutatteindreC3(pos[0], pos[3], j)=(possible,diff)
        if possible:
            v=[pos[0],j,[],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
    #pg bouge -> pos 4 prises
        PGpeutatteindreD4(pos[1],pos[2],pos[3],j)=(possible,diff) #A=pd, B=mg, C=md
        if possible:
            v=[j,pos[1],pos[2],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #pg bouge, pd mg posés, md lachée -> pos 3 prises
        PGpeutatteindreC3(pos[1], pos[2], j)=(possible,diff)
        if possible:
            v=[j,pos[1],pos[2],[],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        #pg bouge, pd md posés, mg lachée -> pos 3 prises
        PGpeutatteindreC3(pos[1], pos[3], j)=(possible,diff)
        if possible:
            v=[j,pos[1],[],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
    return(voisins)

def voisins_de_pos_31prises(pos,Lprises,main,G): #2 pieds, 1 main, main = 2 si mg, 3 si md
    voisins = []    
    v=[pos[0],pos[1],pos[3],pos[2]]+pos[4:] #changement de main
    k=presente(v,Lposfile,dernier,courant)
    voisins=voisins+(k,cout)
      #vers position 4 prises
    bas_m, haut_m = bashaut4_m(Lprises,pos) 
    for i in range(bas_m,haut_m):
        if main==2:
            MDpeutatteindreD4(pos[0],pos[1],pos[2],i)=(possible,diff)
            if possible:
                v=[pos[0],pos[1],pos[2],i,diff]
                k=presente(v,Lpos,file,dernier,courant)
                voisins=voisins+(k,cout)
        elif main==3:
            MGpeutatteindreD4(pos[0],pos[1],pos[3],i)=(possible,diff)
            if possible:
                v=[pos[0],pos[1],i,pos[3],diff]
                k=presente(v,Lpos,file,dernier,courant)
                voisins=voisins+(k,cout)
      #vers position 3 prises
    bas_p, haut_p = bashaut3_p(Lprises,pos,main)
    for i in range(bas_p,haut_p):
        PDpeutatteindreC3(pos[0],pos[main],i)=(possible,diff) #pd bouge
        if possible:
            v=[pos[0],i,pos[2],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        PGpeutatteindreC3(pos[1],pos[main],i)=(possible,diff) #pg bouge
        if possible:
            v=[i,pos[1],pos[2],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
    return(voisins)

def voisins_de_pos_32prises(pos,Lprises,pied,G): #1 pied, 2 mains, pied=0 si pg, 1 si pied droit
    voisins = []
    v=[pos[1],pos[0]]+pos[2:] #changement de pied
    k=presente(v,Lposfile,dernier,courant)
    voisins=voisins+(k,cout)
      #vers poition 4 prises
    bas_p, haut_p = bashaut4_p(Lprises,pos) 
    for i in range(bas_p,haut_p):
        if pied==0:
            PDpeutatteindreD4(pos[0],pos[2],pos[3],i)=(possible,diff)
            if possible:
                v=[pos[0],i,pos[2],pos[3],diff]
                k=presente(v,Lpos,file,dernier,courant)
                voisins=voisins+(k,cout)
        elif pied==1:
            PGpeutatteindreD4(pos[1],pos[2],pos[3],i)=(possible,diff)
            if possible:
                v=[i,pos[1],pos[2],pos[3],diff]
                k=presente(v,Lpos,file,dernier,courant)
                voisins=voisins+(k,cout)
      #vers position 3 prises
    bas_m, haut_m = bashaut3_m(Lprises,pos,pied)
    for i in range(bas_m,haut_m):
        MDpeutatteindreC3(pos[pied],pos[2],i)=(possible,diff) #md bouge
        if possible:
            v=[pos[0],pos[1],pos[2],i,diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        MGpeutatteindreC3(pos[pied],pos[3],i)=(possible,diff) #mg bouge
        if possible:
            v=[pos[0],pos[1],i,pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
        MGpeutatteindreC3(i,pos[3],pos[2])=(possible,diff) #le pied bouge -> attention peut-être à enlever (peu utilisé)
        if possible:
            v=[i,pos[1],pos[2],pos[3],diff]
            k=presente(v,Lpos,file,dernier,courant)
            voisins=voisins+(k,cout)
            w=[pos[0],i,pos[2],pos[3],diff]
            l=presente(w,Lpos,file,dernier,courant)
            voisins=voisins+(l,cout)
    return(voisins)

## gestion de la file
def ajout_file(file,pos,dernier,courant):
    long=len(file)
    if dernier==long-1:
        dernier=0
    else:
        dernier=dernier+1
    if file[dernier] == -1:
        file[dernier]=pos
    else:
        file=file+[-1]*long
        for j in range(0,courant):
            file[j+long]=file[j]
            file[j]=-1
        dernier = dernier + long
        long=long*2
        file[dernier]=pos
    return(file,dernier,courant)    

def retirer_file(file, dernier, courant):
    file[courant]=-1
    if courant==len(file)-1:
        courant=0
    else:
        courant = courant+1
    return(file,dernier,courant)

#file, der, cou = ajout_file(file, 2, der, cou)
#print(file, der,cou)

#file, der, cou = retirer_file(file, der, cou)
#print(file, der,cou)

## le graphe
def creegraphe(Lprises, ini):
    G=[]
    Lpos=[ini]
    file=[0] #ce sont des indices des positions dans la liste "Lpos"
    courant=0 #ce sont des indices des positions dans la liste "file"
    dernier=0 #jusqu'à où la file est remplie
    #itérations....
    while file[courant]>=0:
        nb,p_m= type_de_pos(courant)
        if nb==4:
            voisins_de_courant = voisins_de_pos_4prises(courant,Lprises,G)
        elif nb==3.1:
            voisins_de_courant = voisins_de_pos_31prises(courant,Lprises,p_m,G)
        elif nb==3.2:
            voisins_de_courant = voisins_de_pos_32prises(courant,Lprises,p_m,G)
        G=G+voisins_de_courant
        file, dernier, courant = retirer_file(file, dernier, courant)
    return(G,Lpos,Lprises)


## CHECK LIST
# dans "présente", ajouter les nouvelles positions trouvées à la file 
voisins de pos 4 prises : ajouter 2 memebres en même temps
les arguments de toutes les fonctions (Lprises, Lpos ? G?)
#arguments de voisin_de_pos3 : pied, main (modifier type_de_prise)
# mettre à jour le graphe après la recherche des voisins de chaque prise
# gestion de la file pour ajout dedans et retirer (cf papier)
les heuristiques...
