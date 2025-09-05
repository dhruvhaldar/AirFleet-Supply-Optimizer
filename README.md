# ✈️ Real-World Aerospace Optimization & Control Problems

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-f5d7e3)](https://www.python.org/)
[![PuLP](https://img.shields.io/badge/PuLP-2.7.0-purple)](https://coin-or.github.io/pulp/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)](https://jupyter.org/)
[![PyPy](https://img.shields.io/badge/PyPy-3.11%2B-blue)](https://www.pypy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.11.2-yellow)](https://www.scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7.2-A8DADC)](https://matplotlib.org/)

This repository contains projects that bridge **optimization** and **control theory** for real-world aerospace problems:
- Optimize **spare parts distribution & inventory** using MILP/ILP  
- Implement **control systems** for nonlinear aerospace dynamics (e.g., B747 pitch tracking, four-tank benchmark system)  

---

## Features

### 🛠 Optimization (MILP/ILP)
- **Multi-period planning** for aerospace spare parts  
- **Cost minimization** across transportation, purchase, holding, and shortage  
- **Truck vs Air transport modes** with real-world constraints (capacity, lead times)  
- **Visual analytics** for decision support  

### 🎛 Control Systems
- **Linear Quadratic Integral (LQI) Controller** for pitch tracking of a Boeing 747  
- **Four-Tank Process**: nonlinear benchmark for multivariable control  
  - Nonlinear + linearized models  
  - Decentralized PI control  
  - Robustified control (Glover–McFarlane loop shaping)  
  - Data visualization (tank levels, inputs, RGA heatmaps, sensitivity plots)  

---

## Prerequisites

- Python 3.11+ (or PyPy3.11+, but note SciPy is not fully supported in PyPy)  
- Jupyter Notebook (for running models interactively)  
- Install dependencies from `requirements_python.txt`:
  - **Optimization**: PuLP, NumPy, Pandas, Matplotlib  
  - **Control**: SciPy, python-control, Matplotlib  

---

## Installation

```bash
git clone https://github.com/dhruvhaldar/AirFleet-Supply-Optimizer.git
cd AirFleet-Supply-Optimizer

# Create venv
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# OR
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
