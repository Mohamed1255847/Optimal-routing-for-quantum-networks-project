# Optimal-routing-for-quantum-networks-project

## how to run the project
### using docker 
`docker run --name quantum-router-container quantam-optimal-router`
### using local ENV 
`python3 app.py`

### or
`python app.py`

## Overview

This repository contains code and analysis related to **optimal routing for quantum networks**. It explores how to maximize end-to-end entanglement rates in quantum communication networks by studying different repeater placements and routing strategies.

Quantum networks are a cutting-edge technology enabling secure communication, distributed quantum computing, and advanced sensing by leveraging quantum entanglement. Efficient routing and repeater placement are critical challenges to overcome decoherence and loss in long-distance quantum links.

---

## Project Description

The project implements two main studies:

1. **Repeater Placement and Entanglement Rate Analysis**  
   - Evaluates the end-to-end entanglement rate over a range of route lengths (2 km to 300 km).  
   - Compares multiple repeater placement strategies (single link, equal segment lengths, fractional placements).  
   - Generates line plots and a heatmap illustrating how entanglement rates vary with route length and repeater position.

2. **Optimal Path Finding in a Quantum Network**  
   - Uses a fixed network topology with nodes and links of varying distances.  
   - Iterates over different link distances to find the optimal path maximizing entanglement rate.  
   - Produces a plot of the best achievable entanglement rate versus route length.

Both analyses rely on a `QuantumNetwork` model to compute entanglement rates and a path-finding function to determine optimal routing.

---

## Features

- Parametric study of repeater placement effects on entanglement distribution.
- Visualization of entanglement rate scaling with distance and repeater position.
- Optimal routing search in realistic network topologies.
- Logarithmic scale plots to capture wide dynamic range of entanglement rates.
- Heatmap visualization to explore continuous parameter spaces in repeater placement.

---

## Background

Quantum networking is a rapidly developing field aiming to build a **quantum internet** - a global network enabling quantum communication and distributed quantum computing. Key challenges include:

- Overcoming photon loss and decoherence over long distances.
- Efficient placement of quantum repeaters to extend communication range.
- Routing algorithms that maximize entanglement generation rates.

This project contributes to these challenges by simulating quantum network performance under different routing and repeater placement scenarios, helping inform design and optimization of future quantum networks.

---

## Usage

- The main script runs both studies sequentially, generating plots saved as PNG files:
  - `figure5_reproduction.png` - entanglement rate vs route length for various repeater placements.
  - `entanglement_rate_heatmap.png` - heatmap of entanglement rate vs route length and repeater fraction.
  - `entanglement_rate_plot.png` - optimal entanglement rate vs route length from path optimization.

- Modify or extend the `QuantumNetwork` and `find_optimal_path` implementations to explore additional network topologies or protocols.

---

## References and Further Reading
[Optimal Routing for Quantum Networks](https://www.researchgate.net/publication/320665252_Optimal_Routing_for_Quantum_Networks)

---

## Contact

For questions or contributions, please open an issue or contact the repository maintainer.

---

*This work supports ongoing research toward building scalable, efficient quantum communication networks and contributes tools for evaluating routing and repeater placement strategies.*
