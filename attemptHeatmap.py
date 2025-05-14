import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from collections import defaultdict
from matplotlib.colors import LogNorm


# =============================================
# Quantum Network Parameters (from the paper)
# =============================================
class QuantumNetwork:
    def __init__(self):
        # Physical parameters (default values from the paper)
        self.p_ht = 0.53  # Atom-photon entanglement probability
        self.v_h = 0.8  # Herald detector efficiency
        self.v_t = 0.8  # Telecom detector efficiency
        self.v_o = 0.39  # Optical BSM efficiency
        self.v_a = 0.39  # Atomic BSM efficiency
        self.L0 = 22e3  # Attenuation length (22 km)
        self.c_f = 2e8  # Light speed in fiber (m/s)
        self.tau_p = 5.9e-6  # Atom pulse duration (5.9 μs)
        self.tau_h = 20e-6  # Herald detection time (20 μs)
        self.tau_t = 10e-6  # Telecom detection time (10 μs)
        self.tau_d = 100e-6  # Atom cooling time (100 μs)
        self.tau_o = 10e-6  # Optical BSM duration (10 μs)
        self.tau_a = 10e-6  # Atomic BSM duration (10 μs)
        self.T_ch = 10e-3  # Quantum memory coherence time (10 ms)

    def get_T_c(self, links):
        return sum(l['T_ij_c'] for l in links)

    def recT(self, links):
        n = len(links)
        if n == 1:
            return links[0]['T_ij']
        else:
            k = n // 2
            left_links = links[:k]
            right_links = links[k:]
            T_r_left = self.recT(left_links)
            T_r_right = self.recT(right_links)
            T = max(T_r_left, T_r_right)
            T_c = max(self.get_T_c(left_links), self.get_T_c(right_links))
            T_r_ab = (T + self.tau_a + T_c) / self.v_a
            return T_r_ab

    def recTau(self, links):
        n = len(links)
        if n == 1:
            return links[0]['T_ij_s']
        else:
            k = n // 2
            left_links = links[:k]
            right_links = links[k:]
            tau_r_left = self.recTau(left_links)
            tau_r_right = self.recTau(right_links)
            tau = max(tau_r_left, tau_r_right)
            T_c = max(self.get_T_c(left_links), self.get_T_c(right_links))
            tau_r_ab = tau + self.tau_a + T_c
            return tau_r_ab

    # =============================================
    # End-to-End Entanglement Rate (Algorithm 1 in paper)
    # =============================================
    def end_to_end_rate(self, path, distances):
        # Split path into separate links
        links = []
        for i in range(len(path) - 1):
            link = {}
            link['src'] = path[i]
            link['dst'] = path[i + 1]
            link['dist'] = distances[path[i]][path[i + 1]]
            p_ij = 0.5 * self.v_o * (self.p_ht * self.v_h * self.v_t) ** 2 * np.exp(-link['dist'] / self.L0)
            T_ij_c = link['dist'] / (2 * self.c_f)
            tau_ij = self.tau_t + T_ij_c * 2 + self.tau_o
            T_ij_s = self.tau_p + max(self.tau_h, tau_ij)
            T_ij_f = self.tau_p + max(self.tau_h, tau_ij, self.tau_d)
            T_ij = ((1 - p_ij) * T_ij_f + p_ij * T_ij_s) / p_ij
            link['tau_ij'] = tau_ij
            link['T_ij_c'] = T_ij_c
            link['T_ij_s'] = T_ij_s
            link['T_ij_f'] = T_ij_f
            link['T_ij'] = T_ij
            links.append(link)
        n = len(links)

        # Calculate the end-to-end entanglement rate
        if n == 1 and links[0]['tau_ij'] < self.T_ch:
            return 1.0 / links[0]['T_ij']
        else:
            k = n // 2
            left_links = links[:k]
            right_links = links[k:]
            T_r_left = self.recT(left_links)
            T_r_right = self.recT(right_links)
            T = max(T_r_left, T_r_right)
            T_c = max(self.get_T_c(left_links), self.get_T_c(right_links))
            T_r_ij = (T + self.tau_a + T_c) / self.v_a
            tau_r_left = self.recTau(left_links)
            tau_r_right = self.recTau(right_links)
            tau = max(tau_r_left, tau_r_right)
            tau_r_ij = tau + self.tau_a + T_c
            if tau_r_ij - min([l['T_ij_s'] - l['tau_ij'] for l in links]) <= self.T_ch:
                return 1 / T_r_ij


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
    # Define route lengths to evaluate (in km)
    route_lengths_km = np.linspace(2, 300, 100)
    placements = {
        "Single link": None,
        "d_ik = d_kj": 0.5,
        "d_ik = d_kj/2": 1/3,
        "d_ik = d_kj/4": 0.2,
        "d_ik = lim_n→∞": 0.01,
    }

    qnet = QuantumNetwork()
    results = {}

    for label, fraction in placements.items():
        rates = []
        for L in route_lengths_km:
            if fraction is None:
                # Single link (no repeater)
                distances = {
                    "v1": {"v3": L * 1e3},
                    "v3": {"v1": L * 1e3}
                }
                path = ["v1", "v3"]
            else:
                # Two segments with a repeater at v2
                d_ik = L * fraction
                d_kj = L - d_ik
                distances = {
                    "v1": {"v2": d_ik * 1e3},
                    "v2": {"v1": d_ik * 1e3, "v3": d_kj * 1e3},
                    "v3": {"v2": d_kj * 1e3}
                }
                path = ["v1", "v2", "v3"]

            rate = qnet.end_to_end_rate(path, distances)
            rates.append(rate if rate is not None else 1e-20)  # Avoid log(0)
        results[label] = rates

    # Plotting
    plt.figure(figsize=(10, 6))
    for label, rates in results.items():
        plt.plot(route_lengths_km, rates, label=label, linewidth=2)

    plt.yscale("log")
    plt.xlabel(r'route length $d_{i,k} + d_{k,j}$ [Km]')
    plt.ylabel(r'End-to-End Entanglement Rate $\xi_{i,j}(T^{CH})$')
    plt.title("Expected End-to-End Entanglement Rate vs Route Length")
    plt.legend()
    plt.tight_layout()
    plt.savefig('figure5_reproduction.png')
    plt.show()

    # Create the heatmap for 0 <= alpha <= 1
    alpha_values = np.linspace(0, 1, 100)
    results_heatmap = {}
    for alpha in alpha_values:
        rates = []
        for L in route_lengths_km:
            d_ik = L * alpha / (alpha+1)
            d_kj = L / (alpha+1)
            distances = {
                "v1": {"v2": d_ik * 1e3},
                "v2": {"v1": d_ik * 1e3, "v3": d_kj * 1e3},
                "v3": {"v2": d_kj * 1e3}
            }
            path = ["v1", "v2", "v3"]
            rate = qnet.end_to_end_rate(path, distances)
            rates.append(rate if rate is not None else 1e-20)
        results_heatmap[alpha] = rates

    # Plotting the heatmap
    plt.figure(figsize=(10, 6))
    plt.set_cmap('gray')
    plt.imshow([results_heatmap[alpha] for alpha in alpha_values], aspect='auto', origin='lower', 
               extent=[min(route_lengths_km), max(route_lengths_km), 0, 1], norm=LogNorm())
    plt.colorbar(label='End-to-End Entanglement Rate')
    plt.xlabel(r'route length $d_{i,k} + d_{k,j}$ [Km]')
    plt.ylabel('α')
    plt.title(r'End-to-End Entanglement Rate vs Route Length for $d_{i,k} = \alpha d_{k,j}$')
    plt.tight_layout()
    plt.savefig('entanglement_rate_heatmap.png')
    plt.show()