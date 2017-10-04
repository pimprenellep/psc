#essayer de régler le problème des ombres grises

from colorthief import ColorThief
from PIL import Image
import numpy as np
from math import*
img=Image.open('copiedelespoir.bmp')
color_thief = ColorThief('copiedelespoir.bmp')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=5)
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
n=l
#n=5
#M=[[0,0,1,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,0,0],[1,1,1,1,0]]
Liste_barycentres=[]
for i in range(l-1):
    for j in range(c-1):
        if L[i][j]==1:
            haut_max=i
            bas_max=i
            gauche_max=j
            droite_max=j
            L[i][j]=2
            nb_pixel=1
            #on parcourt les cases adjacentes
            dejavues = [[False]*(n+1) for i in range(n+1)]
            p=[]
            p.append((i,j))
            dejavues[i][j]=True
            while len(p)>0:
                case=p.pop()
                x,y=case
                if x==0 and y==0:
                    indicesAdjacentes = [(x + 1, y),(x, y + 1)]
                elif x==0 :
                    indicesAdjacentes = [(x + 1, y), (x, y - 1), (x, y + 1)]
                elif y==0 :
                    indicesAdjacentes = [(x + 1, y), (x - 1, y), (x, y + 1)]

                else :
                    indicesAdjacentes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                adjacentes = []
                for (i, j) in indicesAdjacentes:
                     if i >= 0 and j >= 0 and i < l-1 and j < c-1 and L[i][j]==1 and not dejavues[i][j]:
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
                    L[i][j]=2
                    p.append((i,j))
            if(nb_pixel>100):        
                Liste_barycentres.append([int(floor((haut_max+bas_max)/2)),int(floor((gauche_max+droite_max)/2)), int(floor((haut_max - bas_max)/2)), int(floor((droite_max - gauche_max)/2)), nb_pixel])


def distance(pixel1, pixel2):
    return sqrt((pixel1[0]-pixel2[0])**2+(pixel1[1]-pixel2[2])**2+(pixel1[1]-pixel2[2])**2)
def proche_gris(pixel1):
    return sqrt((pixel[0]-pixel[1])**2+(pixel[0]-pixel[2])**2+(pixel[2]-pixel[1])**2)<50
def teinte(pixel):
    R=pixel[0]
    G=pixel[1]
    B=pixel[2]
    M=max(R,G,B)
    m=min(R,G,B)
    C=M-m
    if C==0:
        return 0
    if M==R:
        return (G-B)/C % 6
    if M==G:
        return (B-R)/C +2 %6
    if M==B:
        return (R-G)/C +4 % 6
    
    
    

## lissage prises

Liste_voies=[]
for m in range(len(Liste_barycentres)):
#for m in range(10,20):
    image=Image.new(img.mode,(2*Liste_barycentres[m][2],2*Liste_barycentres[m][3]))
    imgNtemp=Image.new(img.mode,(2*Liste_barycentres[m][2],2*Liste_barycentres[m][3]))
    for i in range(2*Liste_barycentres[m][2]-2):
        for j in range(2*Liste_barycentres[m][3]-2):
            image.putpixel((i,j),imgN.getpixel((Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1,Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1)))  
    image.save('image.png')
    color_thief_temp = ColorThief('image.png')
    dominant_color = color_thief_temp.get_color(quality=1)
    palette = color_thief_temp.get_palette(color_count=2, quality=1)
    if proche_gris(palette[0]):
        dominant_color=palette[1]
    r=dominant_color[0]
    b=dominant_color[1]
    g=dominant_color[2]
    '''for i in range(2*Liste_barycentres[m][2]-1):
        for j in range(2*Liste_barycentres[m][3]-1):
            pixel=image.getpixel((i,j))
            if abs(pixel[0]-r)<40 and abs(pixel[1]-b)<=40 and abs(pixel[2]-g)<=40:
                imgNtemp.putpixel((i,j),pixel)
            else :
                imgNtemp.putpixel((i,j),(256,256,256))'''
    #print(dominant_color)
    #imgNtemp.show()
    a=True
    for n in range(len(Liste_voies)):
        if a==True and (abs(Liste_voies[n][0][0]-r)+ abs(Liste_voies[n][0][1]-b) + abs(Liste_voies[n][0][2]-g))<=60:
            Liste_voies[n].append(Liste_barycentres[m])
            a=False
    if a==True :
        Liste_voies.append([dominant_color, Liste_barycentres[m]])                                                                              
                                                                                        
#sélection voies
def print_voie(p):
    if len(Liste_voies[p])<=4:
        return None
    else :
        imgNN=Image.new(img.mode, img.size)
        for i in range(l):
            for j in range(c):
                imgNN.putpixel((i,j),(256,256,256))
        dominant_color=Liste_voies[p][0]
        r=dominant_color[0]
        b=dominant_color[1]
        g=dominant_color[2]
        for m in range(1,len(Liste_voies[p])):
            Liste_barycentres= Liste_voies[p][m]
            #image=Image.new(img.mode,(2*Liste_barycentres[2],2*Liste_barycentres[3]))
            print(Liste_barycentres)
            '''for i in range(2*Liste_barycentres[2]-2):
                for j in range(2*Liste_barycentres[3]-2):
                    image.putpixel((i,j),imgN.getpixel((Liste_barycentres[0]+i-Liste_barycentres[2]+1,Liste_barycentres[1]+j-Liste_barycentres[3]+1)))'''  
            for i in range(2*Liste_barycentres[2]-1):
                for j in range(2*Liste_barycentres[3]-1):
                    pixel=imgN.getpixel((Liste_barycentres[0]+i-Liste_barycentres[2]+1,Liste_barycentres[1]+j-Liste_barycentres[3]+1))
                    if abs(256-r)>30 and abs(256-b)>=30 and abs(256-g)>=30:
                        imgNN.putpixel((Liste_barycentres[0]+i-Liste_barycentres[2]+1,Liste_barycentres[1]+j-Liste_barycentres[3]+1), pixel)
        imgNN.save('voie_p.png')
        imgNN.show()
    
## pour afficher toutes les voies
for i in range(len(Liste_voies)):
    print_voie(i)
