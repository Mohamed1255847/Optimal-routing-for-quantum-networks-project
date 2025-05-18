
import numpy as np
import matplotlib.pyplot as plt
from helpers.QNC import QuantumNetwork
from matplotlib.colors import LogNorm



def run_placement_study():
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

    # Plotting line plots for different placements
    plt.figure(figsize=(10, 6))
    for label, rates in results.items():
        plt.plot(route_lengths_km, rates, label=label, linewidth=2)

    plt.yscale("log")
    plt.xlabel(r'Route length $d_{i,k} + d_{k,j}$ [Km]')
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
            d_ik = L * alpha / (alpha + 1)
            d_kj = L / (alpha + 1)
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
    plt.xlabel(r'Route length $d_{i,k} + d_{k,j}$ [Km]')
    plt.ylabel('α')
    plt.title(r'End-to-End Entanglement Rate vs Route Length for $d_{i,k} = \alpha d_{k,j}$')
    plt.tight_layout()
    plt.savefig('entanglement_rate_heatmap.png')
    plt.show()
