from .stancegraph import StanceGraph

from .positionspossibles import *
from .dessin_graphe import *
#from math import 

class RouteStanceGraph(StanceGraph):
    def __init__(self, route):
        super().__init__(route)
        Lprises = route.getHolds()

        ini = self.trouve_ini(Lprises)

        #Lprises=self.echange_xy(Lprises)
        G=[]
        Lpos=[ini]
        file=[0] #ce sont des indices des positions dans la liste "Lpos"
        courant=0 #ce sont des indices des positions dans la liste "file"
        #itérations....
        while file[courant] >= 0:
            nb,p_m= self.type_de_pos(Lpos[courant])
            if nb==4:
                voisins_de_courant,Lpos,file = self.voisins_de_pos_4prises(file[courant],Lprises,G,Lpos,file,courant)
            elif nb==3.1:
                voisins_de_courant,Lpos,file = self.voisins_de_pos_31prises(file[courant],Lprises,p_m,G,Lpos,file,courant)
            elif nb==3.2:
                voisins_de_courant,Lpos,file = self.voisins_de_pos_32prises(file[courant],Lprises,p_m,G,Lpos,file,courant)
            G=G+[voisins_de_courant]
            file, courant = self.retirer_file(file, courant)
        dessin_graphe(G, Lpos, Lprises)
        #return(G,Lpos, len(G), len(Lpos))

    def trouve_ini(self, Lprises):
        #trouver les pieds possibles pour ini :
        p=0 
        while ((p<len(Lprises)) and (Lprises[p][1] <= j+t/2)):
            p=p+1
        #trouver les mains possibles pour ini :
        m=0
        while ((m<len(Lprises)) and (Lprises[m][1] <= j+t+b)):
            m=m+1
        #cherche la positiond e départ la plus facile
        coutmin = 1000000000
        p_ini = [0,0,1,1]
        for i in range(p):
            for k in range(i+1, m):
        #position du 2ème pied
                pied2 = [(Lprises[i][0]+Lprises[k][0])/2, 0]
                if Lprises[i][0]<Lprises[k][0]:
                    bool,cout=PDpeutatteindreC3(Lprises[i],Lprises[k],pied2,3,Lprises,3)
                    if (bool and (cout<=coutmin)):
                        coutmin=cout
                        p_ini = [i,-1,k,k,cout]
                else :
                    bool,cout=PGpeutatteindreC3(Lprises[i],Lprises[k],pied2,2,Lprises,3)
                    if (bool and (cout<=coutmin)):
                        coutmin=cout
                        p_ini = [-1,i,k,k,cout]
        return(p_ini)

    def echange_xy(self, L):
        for i in range(len(L)):
            L[i][1],L[i][0]=L[i][0],L[i][1]
        return(L)

    def presente(self, pos,Lpos,file,courant): #Lpos pas ordonnée (OK sans "self.ajout_file")  Rq : ATTENTION ici pos est une vraie position !!! (pas un indice dans Lpos)
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
            file, courant = self.ajout_file(file, ind, courant)
        return(Lpos, ind, file,  courant)


    # les voisins__________________________________________________________________________________________________________________________________
    def type_de_pos(self, pos): #rq: ici c'est une vraie position
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

# dans tous les programmes suivants, pos est l'indice d'une position dans Lpos

    def bashaut4_m(self, Lprises,pos,Lpos):
        pg, pd = Lpos[pos][0], Lpos[pos][1]
        ph = pg if Lprises[pg][1] > Lprises[pd][1] else pd
        hmax = Lprises[ph][1] +j+t+b
        i=ph
        while (i<=len(Lprises)-2) and (Lprises[i][1]<hmax):
            i=i+1
        return(ph,i-1)

    def bashaut3_m(self, Lprises,pos,pied,Lpos):
        ph = Lpos[pos][pied]
        hmax = Lprises[ph][1] +j+t+b
        i=ph
        while (i<=len(Lprises)-2) and (Lprises[i][1]<hmax):
            i=i+1
        return(ph,i-1)

    def bashaut4_p(self, Lprises,pos,Lpos):    
        mg, md = Lpos[pos][2], Lpos[pos][3]
        mb = mg if Lprises[mg].y < Lprises[md].y else md
        hmin = Lprises[mb].y -b-t-j
        i=mb
        while (i>=0) and (Lprises[i][1]>hmin):
            i=i-1
        return(i+1,mb)

    def bashaut3_p(self, Lprises,pos,main,Lpos):    
        mb = Lpos[pos][main]
        hmin = Lprises[mb][1] -b-t-j
        i=mb
        while (i>=0) and (Lprises[i][1]>hmin):
            i=i-1
        return(i+1,mb)


    def voisins_de_pos_4prises(self, pos,Lprises,G,Lpos,file,courant):
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
        pbas_m, phaut_m = self.bashaut4_m(Lprises,pos,Lpos)
        for i in range(pbas_m, phaut_m+1):
            I=Lprises[i]
        #md bouge -> pos 4 prises
            if I!=md:
                (possible,diff)=MDpeutatteindreD4(pg,pd,mg,I,Lprises) #A=pg, B=pd, C=mg
                if possible:
                    v=[a,b,c,i,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #md bouge, mg pd posés, pg laché -> pos 3 prises
                (possible,diff)=MDpeutatteindreC3(pd,mg,I,1,Lprises,3)
                if possible:
                    v=[-1,b,c,i,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #md bouge, mg pg posés, pd laché -> pos 3 prises
                (possible,diff)=MDpeutatteindreC3(pg,mg,I,0,Lprises,3)
                if possible:
                    v=[a,-1,c,i,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
        #mg bouge -> pos 4 prises
            if I!= mg :
                (possible,diff)=MGpeutatteindreD4(pg,pd,md,I,Lprises) #A=pg, B=pd, C=md
                if possible:
                    v=[a,b,i,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #mg bouge, md pd posés, pg laché -> pos 3 prises
                (possible,diff)=MGpeutatteindreC3(pd,md,I,1,Lprises,3)
                if possible:
                    v=[-1,b,i,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #mg bouge, md pg posés, pd laché -> pos 3 prises
                (possible,diff)=MGpeutatteindreC3(pg,md,I,0,Lprises,3)
                if possible:
                    v=[a,-1,i,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
    #pbas_p = indice dans Lprises de la prise la plus basse qu'on essaye d'attraper avec le pied, phaut_p = " " " la plus haute " " "
        pbas_p, phaut_p = self.bashaut4_p(Lprises,pos,Lpos)
        for j in range(pbas_p, phaut_p+1):
            J=Lprises[j]
        #pd bouge -> pos 4 prises 
            if J != pd:
                (possible,diff)=PDpeutatteindreD4(pg,mg,md,J,Lprises) #A=pg, B=mg, C=md
                if possible:
                    v=[a,j,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #pd bouge, pg mg posés, md lachée -> pos 3 prises
                (possible,diff)=PDpeutatteindreC3(pg, mg,J,2,Lprises,3)
                if possible:
                    v=[a,j,c,-1,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #pd bouge, pg md posés, mg lachée -> pos 3 prises
                (possible,diff)=PDpeutatteindreC3(pg,md,J,3,Lprises,3)
                if possible:
                    v=[a,j,-1,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
        #pg bouge -> pos 4 prises
            if J != pg:
                (possible,diff)=PGpeutatteindreD4(pd,mg,md,J,Lprises) #A=pd, B=mg, C=md
                if possible:
                    v=[j,b,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #pg bouge, pd mg posés, md lachée -> pos 3 prises
                (possible,diff)=PGpeutatteindreC3(pd, mg, J,2,Lprises,3)
                if possible:
                    v=[j,b,c,-1,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            #pg bouge, pd md posés, mg lachée -> pos 3 prises
                (possible,diff)=PGpeutatteindreC3(pd, md, J,3,Lprises,3)
                if possible:
                    v=[j,b,-1,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
        return(voisins,Lpos,file)

    def voisins_de_pos_31prises(self, pos,Lprises,main,G,Lpos,file,courant): #2 pieds, 1 main, main = 2 si mg, 3 si md
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
        Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
        cout=self.hmouvement(pos,k,Lprises,Lpos)
        voisins=voisins+[(k,cout)]
          #vers position 4 prises
        bas_m, haut_m = self.bashaut4_m(Lprises,pos,Lpos) 
        for i in range(bas_m,haut_m+1):
            I=Lprises[i]
            if main==2:
                (possible,diff)=MDpeutatteindreD4(pg,pd,mg,I,Lprises)
                if possible:
                    v=[a,b,c,i,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            elif main==3:
                (possible,diff)=MGpeutatteindreD4(pg,pd,md,I,Lprises)
                if possible:
                    v=[a,b,i,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
          #vers position 3 prises
        bas_p, haut_p = self.bashaut3_p(Lprises,pos,main,Lpos)
        for i in range(bas_p,haut_p+1):
            I=Lprises[i]
            if I != pd:
                (possible,diff)=PDpeutatteindreC3(pg,Lprises[Lpos[pos][main]],I,main,Lprises,3) #pd bouge
                if possible:
                    v=[a,i,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            if I != pg:        
                (possible,diff)=PGpeutatteindreC3(pd,Lprises[Lpos[pos][main]],I,main,Lprises,3) #pg bouge
                if possible:
                    v=[i,b,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
        for i in range(bas_m,haut_m+1):
            I=Lprises[i]
            if pg[1]>=pd[1]: #pd se lache, pg reste
                if main==2:
                    if I != mg:
                        (possible,diff)=MDpeutatteindreC3(pg,mg,I,0,Lprises,3) #md attrape
                        if possible:
                            v=[a,-1,c,i,diff]
                            Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                            cout=self.hmouvement(pos,k,Lprises,Lpos)
                            voisins=voisins+[(k,cout)]
                elif main==3:
                    if I != md:
                        (possible,diff)=MGpeutatteindreC3(pg,md,I,0,Lprises,3) #mg attrape
                        if possible:
                            v=[a,-1,i,d,diff]
                            Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                            cout=self.hmouvement(pos,k,Lprises,Lpos)
                            voisins=voisins+[(k,cout)]
            elif pd[1]>=pg[1]: #pg se lache, pd reste
                if main==2:
                    if I != mg:
                        (possible,diff)=MDpeutatteindreC3(pd,mg,I,1,Lprises,3) #md attrape
                        if possible:
                            v=[-1,b,c,i,diff]
                            Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                            cout=self.hmouvement(pos,k,Lprises,Lpos)
                            voisins=voisins+[(k,cout)]
                elif main==3:
                    if I != md:
                        (possible,diff)=MGpeutatteindreC3(pd,md,I,1,Lprises,3) #mg attrape
                        if possible:
                            v=[-1,b,i,d,diff]
                            Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                            cout=self.hmouvement(pos,k,Lprises,Lpos)
                            voisins=voisins+[(k,cout)]
        return(voisins,Lpos,file)

    def voisins_de_pos_32prises(self, pos,Lprises,pied,G,Lpos,file,courant): #1 pied, 2 mains, pied=0 si pg, 1 si pied droit
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
        Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
        cout=self.hmouvement(pos,k,Lprises,Lpos)
        voisins=voisins+[(k,cout)]
          #vers poition 4 prises
        bas_p, haut_p = self.bashaut4_p(Lprises,pos,Lpos) 
        for i in range(bas_p,haut_p+1):
            I=Lprises[i]
            if pied==0:
                (possible,diff)=PDpeutatteindreD4(pg,mg,md,I,Lprises)
                if possible:
                    v=[a,i,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            elif pied==1:
                (possible,diff)=PGpeutatteindreD4(pd,mg,md,I,Lprises)
                if possible:
                    v=[i,b,c,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
          #vers position 3 prises
        bas_m, haut_m = self.bashaut3_m(Lprises,pos,pied,Lpos)
        for i in range(bas_m,haut_m+1):
            I=Lprises[i]
            if I != md:
                (possible,diff)=MDpeutatteindreC3(Lprises[Lpos[pos][pied]],mg,I,pied,Lprises,3) #md bouge
                if possible:
                    v=[a,b,c,i,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
            if I != mg:
                (possible,diff)=MGpeutatteindreC3(Lprises[Lpos[pos][pied]],md,I,pied,Lprises,3) #mg bouge
                if possible:
                    v=[a,b,i,d,diff]
                    Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                    cout=self.hmouvement(pos,k,Lprises,Lpos)
                    voisins=voisins+[(k,cout)]
        pbas_p, phaut_p = self.bashaut4_p(Lprises,pos,Lpos)
        for i in range(pbas_p, phaut_p+1):
            I=Lprises[i]    
            (possible,diff)=MGpeutatteindreC3(I,md,mg,pied,Lprises,3) #le pied bouge -> attention heuristique dynamique
            if possible:
                v=[i,b,c,d,diff]
                Lpos, k, file, courant=self.presente(v,Lpos,file,courant)
                cout=self.hmouvement(pos,k,Lprises,Lpos)
                voisins=voisins+[(k,cout)]
                w=[a,i,c,d,diff]
                Lpos, l, file, courant=self.presente(w,Lpos,file,courant)
                cout=self.hmouvement(pos,l,Lprises,Lpos)
                voisins=voisins+[(l,cout)]
        return(voisins,Lpos,file)

    # gestion de la file_______________________________________________________________________________________________________________________________
    

    def ajout_file(self, file,pos,courant):
        file=file+[pos]
        return(file,courant) 


    def retirer_file(self, file, courant):
        file[courant]=-1
        if courant<len(file)-1:
            courant = courant+1
        return(file,courant)


    #heuristiques mouvement___________________________________________________________________________________________________________________________
    #i est la position initiale, f la position finale. ce sont les vraies positions (celles de Lpos)
    #i=a,b,c,d --- f=ap,bp,cp,dp

    def bary(self, pos):
        a,b,c,d = pos[0],pos[1],pos[2],pos[3]
        tdp,m = self.type_de_pos([-1 if pos[i]==[] else 0 for i in range(4)])
        if tdp == 4:
            return([(a[0]+b[0]+c[0]+d[0])/4,(a[1]+b[1]+c[1]+d[1])/4])
        elif tdp == 3.1:
            return([(a[0]+b[0]+pos[m][0])/3,(a[1]+b[1]+pos[m][1])/3])
        elif tdp == 3.2:
            return([(c[0]+d[0]+pos[m][0])/3,(c[1]+d[1]+pos[m][1])/3])

        
    def hgrandmouv(self,a,b,c,d,ap,bp,cp,dp):
        i = [a,b,c,d]
        f = [ap,bp,cp,dp]
        tdp1 = self.type_de_pos(i)[0]
        tdp2 = self.type_de_pos(i)[0]
        bi,bf = self.bary(i),self.bary(f)
        dist = distance(bi,bf)/10
        if tdp2==4:
            if tdp1==3.2:
                L=1#L est à changer, c'est en L/4 que c'est minimum
                h = L/(4*dist) + (4*dist)/L
            else:
                h=4*dist
        elif tdp1==tdp2:
            h=3*dist
        elif tdp1==3.1 and tdp2==3.2:
            h=2*dist
        else :
            h=2*dist
        return(h)#voir s'il ne faut pas multiplier par un préfacteur

    def htravailgrav(self, a,b,c,d,ap,bp,cp,dp):
        i = [a,b,c,d]
        f = [ap,bp,cp,dp]
        return( (self.bary(f)[1]-self.bary(i)[1])/10*1 )  #1 à changer

    def hpetitappui(self, a,b,c,d,ap,bp,cp,dp, Lprises):
        p1=[a,b,c,d]
        p2=[ap,bp,cp,dp]
        tdp1 = self.type_de_pos(p1)
        tdp2 = self.type_de_pos(p2)
        somme_tailles = 0
        for i in range(4): #trouver les appuis
            if ((p1[i]==p2[i]) and (p1[i] != -1)):
                if i<2:
                    somme_tailles+=10
                else :
                    somme_tailles+=1
        return(somme_tailles)

    def hdynamique(self, a,b,c,d,ap,bp,cp,dp):
        i = [a,b,c,d]
        f = [ap,bp,cp,dp]
        tdp1 = self.type_de_pos([a,b,c,d])[0]
        tdp2 = self.type_de_pos([ap,bp,cp,dp])[0]
        bi,bf = self.bary(i), self.bary(f)
        if (tdp1!=4) and (tdp2!=4):
            dist = d(bi,bf)*3
            return(dist/10*0.5) #0.5 à changer
        else :
            return(0)

    def hadherence(self, a,b,c,d,ap,bp,cp,dp):
        p1 = [a,b,c,d]
        p2 = [ap,bp,cp,dp]
        tdp1 = self.type_de_pos(p1)
        tdp2 = self.type_de_pos(p2)
        if ((tdp1 == tdp2) and (tdp1[0]==3.2)):
            return(d(p1[tdp1[1]],p2[tdp1[1]])/10*3) #3 à changer
        else:
            return(0)

    def hinsta(self, a,b,c,d,ap,bp,cp,dp):
        p1=[a,b,c,d]
        p2=[ap,bp,cp,dp]
        tdp1 = self.type_de_pos(p1)
        tdp2 = self.type_de_pos(p2)
        appuisX = []
        appuisY = []
        membre = []
        hinst = 0
        for i in range(4): #trouver les appuis
            if ((p1[i]==p2[i]) and (p1[i] != -1)):
                appuisX = appuisX + [p1[i][0]]
                appuisY = appuisY + [p1[i][1]]
                membre = membre + [i]
        cdg = [sum(appuisX),sum(appuisY)]
        if membre[0]==0 :
            if membre[1]==1 :
                hinst = abs(cdg[0]-(p1[0][0]+p1[1][0])/2) /10 *5 # 5 à changer
            else:
                hinst = abs(cdg[0]-p1[0][0]) /10 *8 # 8 à changer
        elif membre[0]==1 :
            hinst = abs(cdg[0]-p1[1][0]) /10 *8 # 8 à changer
        return(hinst)


    def hmouvement(self, i,f,Lprises,Lpos):
        a=Lprises[Lpos[i][0]]
        b=Lprises[Lpos[i][1]]
        c=Lprises[Lpos[i][2]]
        d=Lprises[Lpos[i][3]]
        ap=Lprises[Lpos[f][0]]
        bp=Lprises[Lpos[f][1]]
        cp=Lprises[Lpos[f][2]]
        dp=Lprises[Lpos[f][3]]
        return((self.hgrandmouv(a,b,c,d,ap,bp,cp,dp) + self.htravailgrav(a,b,c,d,ap,bp,cp,dp)
            + self.hinsta(a,b,c,d,ap,bp,cp,dp) + self.hdynamique(a,b,c,d,ap,bp,cp,dp) +
            self.hadherence(a,b,c,d,ap,bp,cp,dp))/self.hpetitappui(a,b,c,d,ap,bp,cp,dp, Lprises))



## CHECK LIST
# dans "présente", ajouter les nouvelles positions trouvées à la file 
#voisins de pos 4 prises : ajouter 2 memebres en même temps
#les arguments de toutes les fonctions (Lprises, Lpos ? G?)
#arguments de voisin_de_pos3 : pied, main (modifier type_de_prise)
# mettre à jour le graphe après la recherche des voisins de chaque prise
# gestion de la file pour ajout dedans et retirer (cf papier)
#les heuristiques...

