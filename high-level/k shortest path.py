from collections import defaultdict, deque


class GraphDij(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance

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
            distance = dist[u]+graph.distances[(u,node)]
            if(distance < dist[node]):
                dist[node]= distance
                previous[node]=u
                Queue.push(distance,node)
    return previous, dist
            



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
            distance = dist[u]+graph.distances[(u,node)]
            if(distance < dist[node]):
                dist[node]= distance
                previous[node]=u
                Queue.push(distance,node)
    return previous, dist
            
def dij_k_path(graph,source, destination):
    n=len(graph.nodes)
    dist=[10000000]*n
    previous = np.zeros(n,k)
    for i in range(n):
        previous[i]=-1
    dist[source]=0
    Queue = Heap()
    Queue.push(0,(source,0))
    etape =[0]*n
    S= graph.nodes
    while len(Queue)>0 and etape[destination]:
        (u,n)=Queue.pop()
        S.remove(u)
        if u!= destination:
            for node in graph.edges[u]:
                distance = dist[u]+graph.distances[(u,node)]
                Queue.push(distance,(node,etape[node]))
                etape[node]+=1
                previous[node][etape[node]]=[u,n]

            
        
        
    

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
