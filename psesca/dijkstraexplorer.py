from .explorer import Explorer
from .dummycontroller import DummyController
from .graphDij import *

class DijkstraExplorer(Explorer) :
    def __init__(self, stanceGraph):
        super().__init__(stanceGraph)

    '''def short_path(graph, source, destination):
        previous, dist = dijkstra(graph, source)
        full_path = deque()
        current = previous[destination]
        while current !=source :
            full_path.appendleft(current)
            current = previous[current]
        full_path.appendleft(source)
        full_path.append(destination)
        return dist[destination], list(full_path)

    def dijkstra(graph, source):
        n=len(graph.nodes)
        dist=[10000000]*n
        previous = [0]*n
        for i in range(n):
            previous[i]=-1
        dist[source]=0
        Queue = Heap()
        Queue.push(0,source)
        while len(Queue)>0 :
            u= Queue.pop()
            for node in graph.edges[u]:
                print(u, node)
                distance = dist[u]+graph.distances[(u,node)]
                if(distance < dist[node]):
                    dist[node]= distance
                    previous[node]=u
                    Queue.push(distance,node)
        return previous, dist'''

    def dij_k_path(graph,source, destination,k):
        nb_sommet=len(graph.nodes)
        
        
        paths=[]
        previous={}
        Queue = Heap()
        Queue.push(0,(source,source,0,0))
        etape =[0]*nb_sommet
        
        dejaVu=[]
        
        for i in range(nb_sommet):
            dejaVu.append(False)
            
        while (len(Queue)>0 and etape[destination]!=k) :
            (prev,u,n,c)=Queue.pop()
            
            #print(prev,u,n,c)
            if (not dejaVu[u]):
                etape[u]+=1
                dejaVu[u] = True
                previous[(u,etape[u])]=(prev,n)
                #print(previous)
                
                if u!= destination:
                    for node in graph.edges[u]:
                        distance = c+graph.distances[(u,node)]
                        Queue.push(distance,(u,node,etape[u], distance))
                        
                        
                else :
                    full_path = deque()
                    w = u
                    n = etape[w]
                    full_path.appendleft(w)
                    while w!= source :
                        dejaVu[w] = False
                        (w,n) = previous[(w,n)]
                        full_path.appendleft(w)
                        
                    paths.append(full_path)
            
        return previous, paths


    def findPath(self):
        G, Lpos = self.graph.getGraphRep()
        Lprises = self.graph.getRoute().getHolds()
        #ini
        #fin

        #p paramètre heuristique à ajuster pour faire varier le poids du coût de la position par rapport au coût du mouvement
        p=1
        graph = GraphDij()
        for i in range(len(Lpos)):
            graph.add_node(i)
        for i in range(len(Lpos)):
            for j in range(len(Lpos[i])):
                #on ajoute le coût de l'arrête +p*le coût du noeud
                graph.add_edge(i,G[i][j][0],G[i][j][1]+p*Lpos[i][4])

        
        print("Traversing graph")
        #nombre de chemins que l'on cherche : k
        k=10
        dij_k_path(graph, ini, fin, k)
        #utilise Lprise et ini
    """create_Graph(1)
#ini et final à déterminer
print(shortest_path(graph,ini, final))
"""
