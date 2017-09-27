n=5
M=[[0,0,1,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,0,0],[1,1,1,1,0]]
Liste_barycentres=[]
for i in range(n):
    for j in range(n):
        if M[i][j]==1:
            haut_max=i
            bas_max=i
            gauche_max=j
            droite_max=j
            M[i][j]=2
            nb_pixel=1
            #on parcourt les cases adjacentes
            dejavues = [[False]*n for i in range(n)]
            p=[]
            p.append((i,j))
            dejavues[i][j]=True
            while len(p)>0:
                case=p.pop()
                x,y=case
                if x==0 :
                    indicesAdjacentes = [(x + 1, y), (x, y - 1), (x, y + 1)]
                else :
                    indicesAdjacentes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                adjacentes = []
                for (i, j) in indicesAdjacentes:
                     if i >= 0 and j >= 0 and i < n and j < n and M[i][j]==1 and not dejavues[i][j]:
                         adjacentes += [(i, j)]
                for (i, j) in adjacentes:
                    if j>droite_max:
                        droite_max=j
                    if j<gauche_max:
                        gauche_max=j
                    if haut_max<i:
                        haut_max=i
                    if bas_max>i:
                        bas_max=i
                    nb_pixel+=1
                    dejavues[i][j] = True
                    M[i][j]=2
                    p.append((i,j))
            Liste_barycentres.append([floor((haut_max+bas_max)/2),floor((gauche_max+droite_max)/2), haut_max - bas_max, droite_max - gauche_max, nb_pixel])
