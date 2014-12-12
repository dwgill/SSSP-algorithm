SSSP-algorithm
==============

This is a rudimentary implementation of Dijktra's Algorithm and the
Bellman-Ford algorithm, both of them solutions to single source shortest path
problems. They can be invoked in the following format:

```
    python dijkstra.py '{# vertices in graph} {list of edges}`
```

Where the number of vertices is a whole number, and the list of edges a sequence
of vertex-to-vertex tuples each with an associated real weight. For example,
below we add a vertex `(a1, b1)` with weight `w1`, and so on for the other edges.

```
    (a1 b1): w1, (a2 b2): w2, (a3 b3): w3
```
