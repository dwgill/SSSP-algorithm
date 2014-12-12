import re

# Matches strings of the form '## (##, ##):##, (##,##):##, (##,  ##): ##'
# The first number is the total number of vertices,
# following that are pairs of ints representing edges, with each pair having a corresponding real-number weight.
graph_re = r"\d+\s+\(\d+,?\s*\d+\):\s*([-+]?(\d+(\.\d*)?|\.\d+))(,\s+\(\d+,?\s*\d+\):\s*([-+]?(\d+(\.\d*)?|\.\d+)))*"

edge_re  = r"\((?P<src>\d+),?\s*(?P<dest>\d+)\):\s*(?P<weight>[-+]?(\d+(\.\d*)?|\.\d+))"

def parse_graph(src, graph_str, dest=None, dijkstra=True):
    if not re.match(graph_re, graph_str):
        raise ValueError('Invalid Graph format.')

    num_vertices, edges_str = re.split(r"\s+", graph_str, maxsplit=1)
    num_vertices = int(num_vertices)
    start_vertex = src
    stop_vertex  = dest

    if start_vertex >= num_vertices:
        raise ValueError('start vertex is not in range of possible vertices.')
    elif stop_vertex >= num_vertices:
        raise ValueError('stop vertex is not in range of possible vertices.')

    graph = Graph(num_vertices)
    for edge_match in re.finditer(edge_re, edges_str):
        # edge match will have a group 'src', 'dest', 'weight'
        src = int(edge_match.group('src'))
        dest = int(edge_match.group('dest'))
        weight = float(edge_match.group('weight'))
        if src >= num_vertices:
            raise ValueError('Vertex %s is greater than num vertices %s' % (src, num_vertices))
        elif dest >= num_vertices:
            raise ValueError('Vertex %s is greater than num vertices %s' % (dest, num_vertices))
        graph.addEdge(src, dest, weight)

    if dijkstra:
        return graph.dijkstra(start_vertex, stop_vertex)
    else:
        return graph.bellmanFord(start_vertex, stop_vertex)

class Graph(object):
    def __init__(self, total_v):
        self.total_v = total_v
        self.adj = [{} for i in xrange(total_v)]

    def addEdge(self, src_v, dest_v, weight):
        self.adj[src_v][dest_v] = weight

    def edgeExists(self, src_v, dest_v):
        return self.adj[src_v].has_key(dest_v)

    def iterEdges(self):
        for src_v in xrange(self.total_v):
            for dest_v, weight in self.adj[src_v].iteritems():
                yield (src_v, dest_v), weight

    def neighbors(self, v):
        return self.adj[v].keys()

    def edgesFrom(self, v):
        return self.adj[v].iteritems()

    def weight(self, src_v, dest_v):
        return self.adj[src_v].get(dest_v, float('inf'))

    def initializeSingleSource(self, start):
        dist = [float('inf') for i in xrange(self.total_v)]
        pred = [None for i in xrange(self.total_v)]
        dist[start] = 0

        def relax(src_v, dest_v, weight):
            if dist[dest_v] > dist[src_v] + weight:
                dist[dest_v] = dist[src_v] + weight
                pred[dest_v] = src_v

        return dist, pred, relax

    def dijkstra(self, start, end=None):
        dist, pred, relax = self.initializeSingleSource(start)

        q = set(xrange(self.total_v))
        def extractMin(q):
            min_v = min(q, key=lambda e: dist[e])
            q.remove(min_v)
            return min_v

        while q:
            minDist = extractMin(q)
            for dest_v, weight in self.edgesFrom(minDist):
                relax(minDist, dest_v, weight)

        if (end):
            return True, self.constructPath(end, pred)        
        else:
            return dist, pred

    @staticmethod
    def constructPath(end, pred):
        path = []
        current_v = end
        while current_v is not None:
            path.append(current_v)
            current_v = pred[current_v]
        path.reverse()
        return path


    def bellmanFord(self, start, end=None):
        dist, pred, relax = self.initializeSingleSource(start)

        for i in xrange(self.total_v):
            for (src_v, dest_v), weight in self.iterEdges():
                relax(src_v, dest_v, weight)

        for (src_v, dest_v), weight in self.iterEdges():
            if dist[dest_v] > dist[src_v] + weight:
                return False, []

        if end:
            if pred[end] == None and end != start:
                return False, []
            return True, self.constructPath(end, pred)
        else:
            return dist, pred


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
