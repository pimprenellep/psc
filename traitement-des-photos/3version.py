from colorthief import ColorThief
from PIL import Image
import numpy as np
img=Image.open('image3.bmp')
color_thief = ColorThief('image3.bmp')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=5)
print(dominant_color)
print(palette)
l,c=img.size
r=dominant_color[0]
b=dominant_color[1]
g=dominant_color[2]


imgN=Image.new(img.mode,img.size)
imgNN=Image.new(img.mode,img.size)

L=np.zeros((l,c))

for i in range(l):
    for j in range(c):
        
        pixel=img.getpixel((i,j))
        if abs(pixel[0]-r)<=30 and abs(pixel[1]-b)<=30 and abs(pixel[2]-g)<=30:
            ##imgN.putpixel((i,j),dominant_color)
            imgN.putpixel((i,j),(256,256,256))
        else:
            imgN.putpixel((i,j),pixel)
            L[i][j]=1
imgN.save('imgN.png')

##parcours matrice cases adjacentes
#n=l/l5
n=5
M=[[0,0,1,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,0,0],[1,1,1,1,0]]
Liste_barycentres=[]
for i in range(l):
    for j in range(c):
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
                case=p.pop
                print(case)
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
            Liste_barycentres.append([(haut_max+bas_max)/2,(gauche_max+droite_max)/2, haut_max - bas_max, droite_max - gauche_max])
            
'''color_thief = ColorThief('imgN.png')
palette = color_thief.get_palette(color_count=5)
dominant_color = color_thief.get_color(quality=1)'''

'''N=len(palette)
L=[[] for i in range(N)]
for i in range(l):
    for j in range(c):
        pixel=imgN.getpixel((i,j))
        for k in range(0,N):
            if abs(pixel[0]-palette[k][0])<=30 and abs(pixel[1]-palette[k][1])<=30 and abs(pixel[2]-palette[k][2])<=30:
                imgNN.putpixel((i,j),palette[k])
                L[k].append((i,j))
        if abs(pixel[0]-r)<=30 and abs(pixel[1]-b)<=30 and abs(pixel[2]-g)<=30:
            imgNN.putpixel((i,j),dominant_color)


def voie(p):
    voie=Image.new(img.mode,img.size)
    for i in range(l):
        for j in range(c):
            voie.putpixel((i,j),(256,256,256))
    for i in range(len(L[p])):
            voie.putpixel(L[p][i], palette[p+1])
    voie.show()
    return voie  '''  

