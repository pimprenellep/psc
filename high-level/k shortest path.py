from collections import defaultdict, deque
import heapq
import numpy as np


class GraphDij(object):
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.append(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        "self.edges[to_node].append(from_node)"
        self.distances[(from_node, to_node)] = distance


 
class PriorityQueue(list):
 
    def __init__(self, data):
        super(Heap, self).__init__()
        for i, x in enumerate(data):
            self.push(i, x)
 
    def push(self, priority, item):
        """
            On push en rajoute une priorité
        """
        heapq.heappush(self, (priority, item))
 
    def pop(self):
        """
            On pop en retirant la proprité
        """
        return heapq.heappop(self)[1]
 
    def __len__(self):
        return len(self)
 
    def __iter__(self):
        """
            Comme on a une méthode next(), on peut se retourner soi-même.
            Ainsi la boucle for appelera next() automatiquement. 
        """
        return self
 
    def next(self):
        """ 
           On depop la liste du plus petit au plus grand.
        """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration
        
class Heap(object):
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """

    def __init__(self):
        """ create a new min-heap. """
        self._heap = []

    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        assert priority >= 0
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap)[1] # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        """ Get all elements ordered by asc. priority. """
        return self

    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration


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
    return previous, dist
            
'''def dij_k_path(graph,source):
    pass'''
    


    

def short_path(graph, source, destination):
    previous, dist = dijkstra(graph, source)
    full_path = deque()
    current = previous[destination]
    while current !=source :
        full_path.appendleft(current)
        current = previous[current]
    full_path.appendleft(source)
    full_path.append(destination)
    return dist[destination], list(full_path)


#utilisation de la fonction créégraphe d'Elisabeth avec pondération p entre le coût des postitions et le coût des arrêtes
def create_Graph(p):
    (G, Lpos, Lprise)= Creegraphe(Lprise,ini)
    graph = GraphDij()
    for i in range(len(Lpos)):
        graph.add_node(i)
    for i in range(len(Lpos)):
        for j in range(len(Lpos[i])):
            #on ajoute le coût de l'arrête +p*le coût du noeud
            graph.add_edge(i,G[i][j][0],G[i][j][1]+p*Lpos[i][4])


            
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
            


if __name__ == '__main__':
    graph = GraphDij()

    for node in [0, 1, 2, 3, 4, 5, 6]:
        graph.add_node(node)

    graph.add_edge(0, 1, 15)
    graph.add_edge(0, 2, 40)
    graph.add_edge(0,3,50)
    graph.add_edge(1, 3, 15)
    graph.add_edge(2, 3, 30)
    graph.add_edge(1, 4, 50)
    graph.add_edge(3, 4, 30)
    graph.add_edge(4, 5, 5)
    graph.add_edge(5, 6, 2)

    previous, paths = dij_k_path(graph, 0,3,3)
    if(len(paths)>0):
        print(paths[0])
        print(paths[2])
        print(paths[1])
    '''print(short_path(graph, 0, 3,)) # output: (25, ['A', 'B', 'D']) 

    dist, L = short_paths(graph, 0,3,1)
    #print(L[0])'''

            



