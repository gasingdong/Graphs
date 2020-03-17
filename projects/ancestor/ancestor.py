
def earliest_ancestor(ancestors, starting_node):

    def build_graph(data):
        vertices = {}
        for node in data:
            parent = node[0]
            child = node[1]
            if child in vertices:
                vertices[child].add(parent)
            else:
                vertices[child] = {parent}
        return vertices

    graph = build_graph(ancestors)

    if starting_node not in graph:
        return -1

    paths = {starting_node: [starting_node]}

    def pathfinding(start, data, earliest):
        for v in data[start]:
            paths[v] = paths[start] + [v]
            path_length = len(paths[v])
            earliest_length = len(paths[earliest]) if earliest > -1 else 0
            if path_length > earliest_length:
                earliest = v
            elif path_length == earliest_length:
                earliest = v if v < earliest else earliest
            if v in data:
                return pathfinding(v, data, earliest)
        return earliest

    return pathfinding(starting_node, graph, -1)
