from itertools import combinations
from helpers.enumeratePaths import enumerate_paths


# =============================================
# Optimal Path Selection (Algorithm 3 in paper)
# =============================================
def find_optimal_path(network, nodes, distances, startPoint, endPoint):
    # Generate all possible simple paths (no loops)
    all_paths = []
    for src, dst in combinations(nodes, 2):
        # Enumerate all possible paths (simplified for small networks)
        # In practice, use a more efficient method for large networks
        paths = enumerate_paths(src, dst, nodes, distances)
        all_paths.extend(paths)

    # Find the path with the highest entanglement rate
    best_path = None
    best_rate = 0.0

    for path in all_paths:
        if path[0] == startPoint and path[-1] == endPoint:
            rate = network.end_to_end_rate(path, distances)
            if rate > best_rate:
                best_rate = rate
                best_path = path

    return best_path, best_rate