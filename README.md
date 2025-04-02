# Quantum Network Routing Optimizer

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)

Implementation of the optimal routing protocol for quantum networks based on ["Optimal Routing for Quantum Networks"](https://www.researchgate.net/publication/320868252) by Marcello Caleffi.

## Branch Strategy
| Branch    | Purpose                          | Stability  |
|-----------|----------------------------------|------------|
| `develop` | Active development               | Unstable   |
| `release` | Production-ready code            | Stable     |

## Quick Start
```bash
# Development (local)
pip install -r requirements.txt
python quantum_network.py

# Production (Docker)
docker build -t quantum-routing .
docker run --rm quantum-routing