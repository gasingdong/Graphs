"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy
import collections


class Graph:

    """Represent a graph as a dictionary of vertices mapping
    labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        visited = {starting_vertex}
        q = Queue()
        q.enqueue(starting_vertex)
        while q.size():
            head = q.queue[0]
            for v in self.get_neighbors(head):
                if v not in visited:
                    visited.add(v)
                    q.enqueue(v)
            print(q.dequeue())

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        visited = {starting_vertex}
        s = Stack()
        s.push(starting_vertex)
        while s.size():
            head = s.pop()
            for v in self.get_neighbors(head):
                if v not in visited:
                    visited.add(v)
                    s.push(v)
            print(head)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        visited = {starting_vertex}

        def recurse_print(vertex):
            print(vertex)
            for v in self.get_neighbors(vertex):
                if v not in visited:
                    visited.add(v)
                    recurse_print(v)

        recurse_print(starting_vertex)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        paths = {starting_vertex: [starting_vertex]}
        q = Queue()
        q.enqueue(starting_vertex)
        while q.size():
            head = q.dequeue()
            for v in self.get_neighbors(head):
                if v not in paths:
                    paths[v] = paths[head] + [v]
                    if v == destination_vertex:
                        return paths[v]
                    q.enqueue(v)
        return []

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        paths = {starting_vertex: [starting_vertex]}
        s = Stack()
        s.push(starting_vertex)
        while s.size():
            head = s.pop()
            for v in self.get_neighbors(head):
                if v not in paths:
                    paths[v] = paths[head] + [v]
                    if v == destination_vertex:
                        return paths[v]
                    s.push(v)
        return []

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        paths = {starting_vertex: [starting_vertex]}

        def pathfinding(start, end):
            for v in self.get_neighbors(start):
                if v not in paths:
                    paths[v] = paths[start] + [v]
                    if v == end:
                        yield paths[v]
                    yield from pathfinding(v, end)

        return next(pathfinding(starting_vertex, destination_vertex))


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
