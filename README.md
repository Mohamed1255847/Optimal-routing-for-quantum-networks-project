# Optimal-routing-for-quantum-networks-project

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

- [A Strategic Vision for America’s Quantum Networks](https://www.whitehouse.gov/wp-content/uploads/2017/12/A-Strategic-Vision-for-Americas-Quantum-Networks-Feb-2020.pdf)  
- DOE Quantum Internet Blueprint Workshop Report (2020)  
- [Quantum Networking: Findings and Recommendations](https://www.quantum.gov/wp-content/uploads/2024/09/NQIAC-Report-Quantum-Networking.pdf)  
- [Quantum Network Control and Routing Algorithms](https://arxiv.org/abs/2407.19899)  
- [Quantum NETwork: from theory to practice (arXiv 2020)](https://arxiv.org/abs/2009.12000)  

---

## Contact

For questions or contributions, please open an issue or contact the repository maintainer.

---

*This work supports ongoing research toward building scalable, efficient quantum communication networks and contributes tools for evaluating routing and repeater placement strategies.*
