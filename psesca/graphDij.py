from collections import defaultdict, deque
import heapq


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
            
def dij_k_path(graph,source):
    pass
    


    
"""    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path
"""
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

"""
def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)
"""

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

"""create_Graph(1)
#ini et final à déterminer
print(shortest_path(graph,ini, final))
"""
if __name__ == '__main__':
    graph = GraphDij()

    for node in [0, 1, 2, 3, 4, 5, 6]:
        graph.add_node(node)

    graph.add_edge(0, 1, 10)
    graph.add_edge(0, 2, 20)
    graph.add_edge(0,3,25)
    graph.add_edge(1, 3, 15)
    graph.add_edge(2, 3, 30)
    graph.add_edge(1, 4, 50)
    graph.add_edge(3, 4, 30)
    graph.add_edge(4, 5, 5)
    graph.add_edge(5, 6, 2)

    print(short_path(graph, 0, 3)) # output: (25, ['A', 'B', 'D']) 
