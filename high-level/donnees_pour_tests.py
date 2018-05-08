A=[0,0,1,1,1]
B=[3,0,1,1,1]
C=[2,1,1,1,1]
D=[0,3,1,1,1]
E=[3,3,1,1,1]
F=[2,4,1,1,1]
G=[1,5,1,1,1]
H=[5,5,1,1,1]
I=[3,6,1,1,1]

Lprises=[A,B,C,D,E,F,G,H,I,[]]

ini=[0,2,4,-1,20]

Lmouv=[[0,2,3,-1],[-1,2,3,5],[3,2,3,5],[3,2,6,5],[3,4,6,5],[3,4,6,8]]


A=[2.234,0.667]
B=[1.434,0.977]
C=[1.95,1.484]
D=[1.917,1.65]
E=[1.90,2.634]
F=[1.384,2.784]
G=[2.35,3.234]
I=[2.801,2.267]
K=[1.217,3.334]
L=[1.95,3.851]
N=[2.034,4.251]
M=[1.234,4.201]

Lpr = [A,B,C,D,I,E,F,G,K,L,M,N]

PGpeutatteindreD4(A,D,C,B,Lpr)
PGpeutatteindreD4(A,D,E,B,Lpr)
MDpeutatteindreC3(B,F,E,0,Lpr,3)
MDpeutatteindreD4(B,C,F,E,Lpr)
MGpeutatteindreC3(C,E,F,1,Lpr,3)
MGpeutatteindreC3(C,G,F,1,Lpr,3)
MGpeutatteindreC3(D,G,F,0,Lpr,3)
MGpeutatteindreD4(D,I,G,F,Lpr)

Lmouv6b=[[1,0,3,2],[1,0,3,5],[1,-1,6,5],[1,2,6,5],[-1,2,6,5],[-1,2,6,7],[3,-1,6,7],[3,4,6,7]]

#fausses positions
PDpeutatteindreC3(B,D,C,3,Lpr,3)
MDpeutatteindreD4(D,C,E,I,Lpr)
MDpeutatteindreC3(A,C,D,0,Lpr,3)
MDpeutatteindreC3(A,C,D,1,Lpr,3)