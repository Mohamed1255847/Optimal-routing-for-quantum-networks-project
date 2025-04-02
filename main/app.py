import numpy as np
from itertools import combinations
from collections import defaultdict

# =============================================
# Quantum Network Parameters (from the paper)
# =============================================
class QuantumNetwork:
    def __init__(self):
        # Physical parameters (default values from the paper)
        self.p_ht = 0.53       # Atom-photon entanglement probability
        self.v_h = 0.8          # Herald detector efficiency
        self.v_t = 0.8          # Telecom detector efficiency
        self.v_o = 0.39         # Optical BSM efficiency
        self.v_a = 0.39         # Atomic BSM efficiency
        self.L0 = 22e3          # Attenuation length (22 km)
        self.c_f = 2e8          # Light speed in fiber (m/s)
        self.tau_p = 5.9e-6     # Atom pulse duration (5.9 μs)
        self.tau_h = 20e-6      # Herald detection time (20 μs)
        self.tau_t = 10e-6      # Telecom detection time (10 μs)
        self.tau_d = 100e-6     # Atom cooling time (100 μs)
        self.tau_o = 10e-6      # Optical BSM duration (10 μs)
        self.tau_a = 10e-6      # Atomic BSM duration (10 μs)
        self.T_ch = 10e-3       # Quantum memory coherence time (10 ms)

    # =============================================
    # Link Entanglement Rate (Eq. 8 in the paper)
    # =============================================
    def link_entanglement_rate(self, d_ij):
        # Probability of successful link entanglement (Eq. 2)
        p_ij = 0.5 * self.v_o * (self.p_ht * self.v_h * self.v_t)**2 * np.exp(-d_ij / self.L0)

        # Time for successful attempt (Eq. 4-5)
        tau_ij = self.tau_t + (d_ij / (2 * self.c_f)) + self.tau_o + (d_ij / (2 * self.c_f))
        T_ij_s = self.tau_p + max(self.tau_h, tau_ij)

        # Time for failed attempt (Eq. 6)
        T_ij_f = self.tau_p + max(self.tau_h, tau_ij, self.tau_d)

        # Average time for entanglement generation (Eq. 7)
        T_ij = ((1 - p_ij) * T_ij_f + p_ij * T_ij_s) / p_ij

        # Link entanglement rate (Eq. 8)
        if self.T_ch < tau_ij:
            return 0.0
        else:
            return 1.0 / T_ij

    # =============================================
    # End-to-End Entanglement Rate (Eq. 11)
    # =============================================
    def end_to_end_rate(self, path, distances):
        if len(path) == 1:
            # Direct link case
            d = distances[path[0]][path[1]]
            return self.link_entanglement_rate(d)
        else:
            # Recursive case (split path into sub-paths)
            k = len(path) // 2
            left_path = path[:k+1]
            right_path = path[k:]

            # Recursively compute rates for sub-paths
            rate_left = self.end_to_end_rate(left_path, distances)
            rate_right = self.end_to_end_rate(right_path, distances)

            # If either sub-path has zero rate, the whole path fails
            if rate_left == 0 or rate_right == 0:
                return 0.0

            # Time for entanglement swapping (Eq. 10)
            T_left = 1.0 / rate_left
            T_right = 1.0 / rate_right
            T_swap = (max(T_left, T_right) + self.tau_a) / self.v_a

            # Check decoherence constraint (Eq. 11)
            tau_left = T_left
            tau_right = T_right
            tau_total = max(tau_left, tau_right) + self.tau_a

            if self.T_ch < tau_total:
                return 0.0
            else:
                return 1.0 / T_swap

# =============================================
# Optimal Path Selection (Algorithm 3 in paper)
# =============================================
def find_optimal_path(network, nodes, distances):
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
        rate = network.end_to_end_rate(path, distances)
        if rate > best_rate:
            best_rate = rate
            best_path = path

    return best_path, best_rate

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

# =============================================
# Example Usage
# =============================================
if __name__ == "__main__":
    # Example network topology (from Fig. 7 in the paper)
    nodes = ["v1", "v2", "v3", "vj"]
    distances = {
        "v1": {"v2": 5e3},  # 5 km
        "v2": {"v1": 5e3, "v3": 5e3, "vj": 10e3},  # 5 km and 10 km
        "v3": {"v2": 5e3, "vj": 5e3},
        "vj": {"v2": 10e3, "v3": 5e3}
    }

    # Initialize the quantum network
    qnet = QuantumNetwork()

    # Find the optimal path from v1 to vj
    best_path, best_rate = find_optimal_path(qnet, nodes, distances)

    print(f"Optimal path: {best_path}")
    print(f"Entanglement rate: {best_rate:.2f} entanglements/second")