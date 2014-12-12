import graph

if __name__ == '__main__':
    import sys

    if not sys.argv[1].split()[0].isdigit():
        raise ValueError('No source vertex provided.')

    if sys.argv[1].split()[2].isdigit():
        src, dest, graph_str = sys.argv[1].split(None, 2)
        src = int(src)
        dest = int(dest)

        validity, path_to_end = graph.parse_graph(src, graph_str, dest, dijkstra=False)
        if not validity:
            print 'Graph was invalid: had negative weight cycle.'
        print path_to_end
        
    else:
        src, graph_str = sys.argv[1].split(None, 1)
        src = int(src)
        
        dist, pred = graph.parse_graph(src, graph_str, dijkstra=False)
        print 'distances from the source: {}'.format(dist)
        print 'preceding vertices: {}'.format(pred)



