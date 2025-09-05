# ✈️ Real-World Aerospace Optimization Problems

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PuLP](https://img.shields.io/badge/PuLP-2.7.0-blue)](https://coin-or.github.io/pulp/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)](https://jupyter.org/)

Optimize aerospace spare parts distribution and inventory management using advanced optimization techniques. This project implements both **Mixed Integer Linear Programming (MILP)** and **Integer Linear Programming (ILP)** models to solve complex aerospace logistics problems.

## 📋 Features

- **Multi-period Optimization**: Plan spare parts distribution across multiple time periods
- **Cost Minimization**: Optimize total costs including transport, purchase, holding, and shortage costs
- **Multiple Transportation Modes**: Model both truck and air shipments with different cost structures
- **Real-world Constraints**: Account for truck capacity, order lead times, and repair returns
- **Visual Analytics**: Generate insightful visualizations of optimization results

## 🛠️ Test cases

### 1. Mixed Integer Linear Programming (MILP)
The MILP model (in `milp.ipynb`) provides a comprehensive solution for multi-period aerospace spare parts distribution with:
- Binary decision variables for order placement
- Continuous variables for inventory and shipments
- Real-world constraints including capacity and lead times
- Detailed cost analysis and visualization

### 2. Integer Linear Programming (ILP)
The ILP model (in `ilp.ipynb`) offers an alternative approach with:
- Pure integer programming formulation
- Simplified constraints for specific use cases
- Performance-optimized for certain problem sizes

### 3. Linear Quadratic Integral (LQI) Controller

## 📦 Prerequisites

- Python 3.8+
- PyPy (recommended for better performance)
- Jupyter Notebook (for viewing and running the notebooks)
- Required Python packages (see `requirements.txt`):
  - PuLP (for optimization)
  - NumPy (for numerical operations)
  - Matplotlib (for visualization)
  - Pandas (for data manipulation)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhruvhaldar/AirFleet-Supply-Optimizer.git
   cd AirFleet-Supply-Optimizer
   ```

2. **Set up a virtual environment**
   
   For Windows:
   ```
   python -m venv my-pypy-venv
   my-pypy-venv\Scripts\activate
   ```
   
   For Linux/macOS:
   ```bash
   python3 -m venv my-pypy-venv
   source my-pypy-venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Usage

### Running the MILP Model
1. Open `milp.ipynb` in Jupyter Notebook
2. Run all cells to execute the optimization
3. Review the results and visualizations

### Running the ILP Model
1. Open `ilp.ipynb` in Jupyter Notebook
2. Run all cells to execute the optimization
3. Analyze the results and compare with MILP approach

## 📊 Model Parameters

### Input Data
- **Bases**: Storage locations (e.g., Delhi, Mumbai, Bengaluru)
- **Stations**: Demand points (e.g., Kolkata, Hyderabad, Chennai)
- **Parts**: Different types of spare parts
- **Periods**: Planning time periods

### Cost Components
- Transportation costs (truck and air)
- Purchase costs
- Holding costs
- Shortage costs
- Fixed ordering costs

## 📈 Results

The optimization provides:
- Optimal order quantities for each base and period
- Shipment schedules (truck and air)
- Inventory levels over time
- Total cost breakdown
- Performance metrics

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any questions or suggestions, please open an issue or contact the repository owner.

3. **View results**
   - Check the output directory for generated reports
   - Analyze the optimization results

## Project Structure

```
.
├── milp.ipynb    # MILP optimization model
├── ilp.ipynb     # ILP optimization model
├── requirements.txt     # Project dependencies
├── my-pypy-venv  # Virtual environment
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.