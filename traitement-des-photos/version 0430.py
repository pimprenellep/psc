from colorthief import ColorThief
from PIL import Image
import numpy as np
from math import *

im = Image.new("RGB", (512, 512), "white")
img=Image.open('ensta1.jpg')
color_thief = ColorThief('ensta1.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=5)
l,c=img.size
r=dominant_color[0]
b=dominant_color[1]
g=dominant_color[2]

def max_liste(liste):
    maxi = liste[0]
    ind_maxi = 0
    k=0
    for h in liste :
        if h>maxi:
            maxi = h
            ind_maxi = k
        k=k+1
    return(maxi, ind_maxi)

def score(img, p1, p2):
    l, c = img.size
    pixel1 = img.getpixel(p1)
    pixel2 = img.getpixel(p2)
    return (pixel1[0]-pixel2[0])**2 + (pixel1[1]-pixel2[1])**2 + (pixel1[2]-pixel2[2])**2

imgN=Image.new(img.mode, img.size)
imgNN=Image.new(img.mode, img.size)
L=np.zeros((l,c)) #matrice de zéros de dim lxc

M = np.zeros((l, c))

unMarked = []
for i in range(l):
    for j in range(c):    
        unMarked.append((i, j))

while len(unMarked) > 0:
    startX, startY = unMarked.pop()
    if M[startX][startY] > 0: continue;
    M[startX][startY] = 1
    waitingBords = []
    area = []
    waitingBords.append((startX, startY))
    area.append((startX, startY))
    iL = l; iR = 0; jT = c; jB = 0;
    while len(waitingBords) > 0:
        p = waitingBords.pop()
        x, y = p
        bords = []
        if x-1 >= 0: bords.append((x-1, y))
        if y-1 >= 0: bords.append((x, y-1))
        if x+1 < l: bords.append((x+1, y))
        if y+1 < c: bords.append((x, y+1))
        for (i, j) in bords:
            if M[i][j] == 0 and score(img, (i, j), p) < 60:
                waitingBords.append((i, j))
                area.append((i, j))
                M[i][j] = 1
                if i < iL: iL = i
                elif i > iR: iR = i
                if j < jT: jT = j
                elif j > jB: jB = j
    if ((jB - jT) > 50 and (iR - iL) > 50): continue;
    for (i, j) in area:
        M[i][j] = 2


for i in range(l):
    for j in range(c):
        pixel=img.getpixel((i,j))
        if M[i][j] == 1:
            imgN.putpixel((i,j),(256,256,256))#colorier le pixel en noir si celui-ci n'est pas intéressant
        else:
            imgN.putpixel((i,j),pixel)
            L[i][j] = 1
imgN.save('imgN.png')

##parcours matrice cases adjacentes afin de délimiter les prises

n=max(l,c)
taille_pixel_h=0
taille_pixel_l=0

#n=5
#M=[[0,0,1,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,0,0],[1,1,1,1,0]]
Liste_barycentres=[]
colors = []
for i in range(l-1):
    for j in range(c-1):
        if L[i][j]==1:
            haut_max=i
            bas_max=i
            gauche_max=j
            droite_max=j
            somme_color = [0,0,0]
            color = []     
            L[i][j]=2
            nb_pixel=1
            #on parcourt les cases adjacentes
            dejavues = [[False]*(n+1) for i in range(n+1)]
            p=[]
            p.append((i,j))
            dejavues[i][j]=True
            while len(p)>0:
                case=p.pop()
                x, y=case
                if x==0 and y==0:
                    indicesAdjacentes = [(x + 1, y), (x, y + 1)]
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
                '''calcul des dimensions de la prise'''
                for (i, j) in adjacentes:
                    if j>droite_max:
                        droite_max=j
                    if j<gauche_max:
                        gauche_max=j
                    if haut_max<i:
                        haut_max=i
                    if bas_max>i:
                        bas_max=i
                    pixel=img.getpixel((i,j))
                    '''collecte des couleurs de la prise'''
                    color.append([pixel[0],pixel[1],pixel[2]])
                    nb_pixel+=1
                    dejavues[i][j] = True
                    L[i][j]=2
                    p.append((i,j))
            if(nb_pixel>(l*c)/4800) and (droite_max - gauche_max)<l/10 and (bas_max - haut_max)<c/10 and (droite_max - gauche_max)/(bas_max - haut_max)<4 and (bas_max - haut_max)/(droite_max - gauche_max)<4 and nb_pixel*10>(droite_max - gauche_max)*(bas_max - haut_max):
                for col in color : 
                    somme_color = [somme_color[0]+(col[0]+.0)/(nb_pixel+.0),somme_color[1]+(col[1]+.0)/(nb_pixel+.0),somme_color[2]+(col[2]+.0)/(nb_pixel+.0)]
                    
                colors.append(somme_color[0]+somme_color[1]+somme_color[2])
                Liste_barycentres.append([int(floor((haut_max+bas_max)/2)),int(floor((gauche_max+droite_max)/2)), int(floor((haut_max - bas_max)/2)), int(floor((droite_max - gauche_max)/2)), nb_pixel, somme_color])   

 
    
def echelle(colors,Liste_barycentres):
    m,i = max_liste(colors)
    hauteur_pix = Liste_barycentres[i][3]*2
    print("hauteur pix = ", hauteur_pix)
    #print("min =", i)
    taille_pixel = 0.24/hauteur_pix
    del Liste_barycentres[i]
    del colors[i]
    return(taille_pixel, i)

echelle = echelle(colors, Liste_barycentres)
print(echelle)
#print(colors)
#print(Liste_barycentres)

def proche_gris(pixel1):
    return sqrt((pixel[0]-pixel[1])**2+(pixel[0]-pixel[2])**2+(pixel[2]-pixel[1])**2)<50

    

    
    

## renvoie les prises isolées et l'ensemble des numéros associés pour que l'utilisateur entre la voie

Liste_voies=[]
imgNtemp=Image.new(img.mode,img.size)
imgchiffre=Image.new(img.mode,img.size)
for m in range(len(Liste_barycentres)-1):
#for m in range(29):
    image=Image.new(img.mode,(2*Liste_barycentres[m][2],2*Liste_barycentres[m][3]))
    #imgNtemp=Image.new(img.mode,(2*Liste_barycentres[m][2],2*Liste_barycentres[m][3]))
    for i in range(2*Liste_barycentres[m][2]-2):
        for j in range(2*Liste_barycentres[m][3]-2):
            image.putpixel((i,j),imgN.getpixel((Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1,Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1)))  
    image.save('image.png')
    color_thief_temp = ColorThief('image.png')
    dominant_color = color_thief_temp.get_color(quality=1)
    #print(dominant_color)
    palette = color_thief_temp.get_palette(color_count=2, quality=1)
    if proche_gris(palette[0]):
        dominant_color=palette[1]
    r=dominant_color[0]
    b=dominant_color[1]
    g=dominant_color[2]
    chiffre=Image.open('{}.png'.format(m+1))
    size1,size2=chiffre.size
    for i in range(2*Liste_barycentres[m][2]-1):
        for j in range(2*Liste_barycentres[m][3]-1):
            pixel=image.getpixel((i,j))
            #if abs(pixel[0]-r)<60 and abs(pixel[1]-b)<=60 and abs(pixel[2]-g)<=60:
            imgNtemp.putpixel((Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1,Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1),pixel)
            """else :
                imgNtemp.putpixel((Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1,Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1),(256,256,256))"""
    for i in range(size1-1):
        for j in range(size2-1):
            if(0<Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1<l) and (0<Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1<c):
                imgchiffre.putpixel((Liste_barycentres[m][0]+i-Liste_barycentres[m][2]+1,Liste_barycentres[m][1]+j-Liste_barycentres[m][3]+1), chiffre.getpixel((i,j)))


while len(Liste_barycentres)>0:
    prise = Liste_barycentres.pop()
    voie_color = [prise[5][0],prise[5][1],prise[5][2]]
    prise_count = 1
    voie = [[prise[0],prise[1],prise[2],prise[3],prise[4]]]
    Liste_barycentres2 = []
    while len(Liste_barycentres)>0:
        p = Liste_barycentres.pop()
        if ((p[5][0]-voie_color[0])**2+(p[5][1]-voie_color[1])**2+(p[5][2]-voie_color[2])**2)<1000:
            voie_color = [(voie_color[0]*prise_count+p[5][0])/(prise_count+1),(voie_color[1]*prise_count+p[5][1])/(prise_count+1),(voie_color[2]*prise_count+p[5][2])/(prise_count+1)]
            prise_count = prise_count+1;
            voie.append([p[0],p[1],p[2],p[3],p[4]])
        else: Liste_barycentres2.append(p)
    Liste_voies.append([voie, voie_color])
    Liste_barycentres = Liste_barycentres2
    
imgvoies=Image.new(img.mode,img.size)
for voie in Liste_voies:
    for prise in voie[0]:
        for i in range(2*prise[2]-1):
            for j in range(2*prise[3]-1):
                imgvoies.putpixel((prise[0]+i-prise[2]+1,prise[1]+j-prise[3]+1),(int(voie[1][0]),int(voie[1][1]),int(voie[1][2])))
        
    
for vn in range(len(Liste_voies)):
    f = open('{}.json'.format(vn+1), "w")
    print(Liste_voies[vn][0], file = f)
    f.close()
    

#imgNtemp.show()
imgNtemp.save('imgNtemp.png')
imgvoies.save('imgvoies.png')
#imgchiffre.show()
imgchiffre.save('imgchiffre.png')

#à partir de la liste des prises données par l'utilisateur, renvoie la voie sélectionnée à titre de confirmation
def print_voie(L):
    imgNN=Image.new(img.mode, img.size)
    for i in range(l):
        for j in range(c):
            imgNN.putpixel((i,j),(256,256,256))
    for m in range(len(L)):
        Liste = Liste_barycentres[L[m]-1]
        #image=Image.new(img.mode,(2*Liste_barycentres[2],2*Liste_barycentres[3]))
        print(Liste_barycentres)
        '''for i in range(2*Liste[2]-2):
            for j in range(2*Liste[3]-2):
                image.putpixel((i,j),imgN.getpixel((Liste[0]+i-Liste[2]+1,Liste[1]+j-Liste[3]+1)))'''  
        for i in range(2*Liste[2]-1):
            for j in range(2*Liste[3]-1):
                pixel=imgN.getpixel((Liste[0]+i-Liste[2]+1,Liste[1]+j-Liste[3]+1))
                if abs(256-r)>30 and abs(256-b)>=30 and abs(256-g)>=30:
                    imgNN.putpixel((Liste[0]+i-Liste[2]+1,Liste[1]+j-Liste[3]+1), pixel)
    return Liste
   
                                
