import matplotlib.pyplot as plt
from helpers.QNC import QuantumNetwork
from helpers.findOptimalPath import find_optimal_path


def run_optimal_path_study():
    # Example network topology (from Fig. 7 in the paper)
    nodes = ["v1", "v2", "v3", "vj"]

    x_axis = []
    y_axis = []

    for x in range(150):
        distances = {
            "v1": {"v2": x * 1e3},
            "v2": {"v1": x * 1e3, "v3": x * 1e3, "vj": 10e3},
            "v3": {"v2": x * 1e3, "vj": 1e3},
            "vj": {"v2": 10e3, "v3": 1e3}
        }

        # Initialize the quantum network
        qnet = QuantumNetwork()

        # Find the optimal path from v1 to v3 (or vj if needed)
        best_path, best_rate = find_optimal_path(qnet, nodes, distances, 'v1', 'v3')
        x_axis.append(2 * x)  # Assuming route length is 2*x km as in original
        y_axis.append(best_rate if best_rate is not None else 1e-20)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(x_axis, y_axis)
    plt.xlabel('Route length (km)')
    plt.yscale('log')
    plt.ylabel('Entanglement rate (entanglements/s)')
    plt.title('Expected entanglement rate')
    plt.tight_layout()
    plt.savefig('entanglement_rate_plot.png')
    plt.show()

    print("Plot saved as entanglement_rate_plot.png")
    #Optionally print best path and rate
    print(f"Optimal path: {best_path}")
    print(f"Entanglement rate: {best_rate:.2f} entanglements/second")
