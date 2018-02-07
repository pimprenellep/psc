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


def dijkstra(graph, initial):
    visited = {initial: 0}
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
    graph = Graph()

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        graph.add_node(node)

    graph.add_edge('A', 'B', 10)
    graph.add_edge('A', 'C', 20)
    graph.add_edge('B', 'D', 15)
    graph.add_edge('C', 'D', 30)
    graph.add_edge('B', 'E', 50)
    graph.add_edge('D', 'E', 30)
    graph.add_edge('E', 'F', 5)
    graph.add_edge('F', 'G', 2)

    print(shortest_path(graph, 'A', 'D')) # output: (25, ['A', 'B', 'D']) 
