import matplotlib.pyplot as plt

def dessin_graphe(G, Lpos, Lprises):
    bar_x,bar_y=barycentres(Lpos, Lprises)
    plt.plot(bar_x, bar_y, "bs", markersize = 10)
    for i in range(len(G)):
        V=G[i]
        xp,yp=bar_x[i],bar_y[i]
        for v in V:
            xv,yv=bar_x[v[0]],bar_y[v[0]]
            plt.plot([xp,xv],[yp,yv], "b", linewidth = 0.5)
    plt.show()

def type_de_pos(pos):
    if pos[0]==-1:
        return(3.2,1)
    elif pos[1]==-1:
        return(3.2,0)
    else:
        if pos[2]==-1:
            return(3.1,3)
        elif pos[3]==-1:
            return(3.1,2)
        else:
            return(4,"")
    
def bary_pos(pos, Lprises):
    if type_de_pos(pos)[0]==4:
        x=(Lprises[pos[0]][0]+Lprises[pos[1]][0]+Lprises[pos[2]][0]+Lprises[pos[3]][0])/4
        y=(Lprises[pos[0]][1]+Lprises[pos[1]][1]+Lprises[pos[2]][1]+Lprises[pos[3]][1])/4
    elif type_de_pos(pos)[1]==0:
        x=(Lprises[pos[0]][0]+Lprises[pos[2]][0]+Lprises[pos[3]][0])/3
        y=(Lprises[pos[0]][1]+Lprises[pos[2]][1]+Lprises[pos[3]][1])/3
    elif type_de_pos(pos)[1]==1:
        x=(Lprises[pos[1]][0]+Lprises[pos[2]][0]+Lprises[pos[3]][0])/3
        y=(Lprises[pos[1]][1]+Lprises[pos[2]][1]+Lprises[pos[3]][1])/3
    elif type_de_pos(pos)[1]==2:
        x=(Lprises[pos[0]][0]+Lprises[pos[1]][0]+Lprises[pos[2]][0])/3
        y=(Lprises[pos[0]][1]+Lprises[pos[1]][1]+Lprises[pos[2]][1])/3
    elif type_de_pos(pos)[1]==3:
        x=(Lprises[pos[0]][0]+Lprises[pos[1]][0]+Lprises[pos[3]][0])/3
        y=(Lprises[pos[0]][1]+Lprises[pos[1]][1]+Lprises[pos[3]][1])/3
    return(x,y)

def barycentres(Lpos, Lprises):
    bar_x=[0]*len(Lpos)
    bar_y=[0]*len(Lpos)
    for i in range(0,len(Lpos)):
        bx,by = bary_pos(Lpos[i], Lprises)
        bar_x[i]=bx
        bar_y[i]=by
    return(bar_x,bar_y)



