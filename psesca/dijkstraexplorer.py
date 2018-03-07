from .explorer import Explorer
from .dummycontroller import DummyController
from .graphDij import *

class DijkstraExplorer(Explorer) :
    def __init__(self, stanceGraph):
        super().__init__(stanceGraph)

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


    def findPath(self):
        G, Lpos = self.graph.getGraphRep()
        Lprises = self.graph.getRoute().getHolds()

        # Code du parcours de graphe
        print("Traversing graph")
        #utilise Lprise et ini
    """create_Graph(1)
#ini et final à déterminer
print(shortest_path(graph,ini, final))
"""
