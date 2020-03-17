
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

    def pathfinding(start, data):
        for v in data[start]:
            paths[v] = paths[start] + [v]
            if v in data:
                pathfinding(v, data)

    pathfinding(starting_node, graph)
    max_level = 0
    earliest = []
    for path in paths:
        level = len(paths[path])
        if level > max_level:
            earliest = [path]
            max_level = level
        elif level == max_level:
            earliest.append(path)
    return min(earliest) if earliest else -1
