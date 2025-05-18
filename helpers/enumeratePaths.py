

# Helper function to enumerate paths (simplified)
def enumerate_paths(src, dst, nodes, distances, visited=None):
    if visited is None:
        visited = set()
    visited.add(src)

    paths = []
    if src == dst:
        return [[dst]]

    for neighbor in nodes:
        if neighbor not in visited and distances[src].get(neighbor, None) is not None:
            for subpath in enumerate_paths(neighbor, dst, nodes, distances, visited.copy()):
                paths.append([src] + subpath)

    return paths