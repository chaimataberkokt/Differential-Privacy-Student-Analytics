# Quick Start Guide

Get the Differential Privacy Student Analytics system up and running in minutes!

##  Setup

### 1. Clone Repository

```bash
git clone https://github.com/chaimataberkokt/Differential-Privacy-Student-Analytics.git
cd dp-student-analytics
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run app.py
```

The app will open at: **http://localhost:8501**

---

## First Steps

### Using the Dashboard

1. **Adjust Privacy Budget**: Use the slider on the left to set epsilon (0.01 - 5.0)
2. **Select Mechanism**: Choose between Laplace and Gaussian noise
3. **Set Trials**: Determine how many times to run queries (1-100)
4. **Observe Results**: Watch the visualizations update in real-time

### Interpreting Results

| Epsilon | Privacy | Use Case |
|---------|---------|----------|
| 0.1 | 🔓 Very Strong | Maximum privacy needed |
| 0.5 | 🔒 Strong | Sensitive data |
| 1.0 | ⚖️ Balanced | **Recommended** |
| 2.0+ | 🎯 Weak | Non-sensitive analysis |

### Key Metrics

- **True Value**: Exact statistic from the dataset
- **Private Value**: DP-protected statistic with noise
- **Absolute Error**: Raw difference between values
- **Relative Error %**: Error as percentage of true value

---

##  Using as Python Module

### Basic Usage

```python
from DP_Analytics_Students import DP_Analytics_Students

# Initialize
analytics = DP_Analytics_Students("students.csv", pass_threshold=10)

# Get dataset info
profile = analytics.get_dataset_profile()
print(profile)

# Run DP query
results = analytics.dp_queries(epsilon=0.5, mechanism="laplace")

# Access results
true_stats = results["true_stats"]
noisy_stats = results["noisy_stats"]

print(f"True mean: {true_stats['mean_final_mark']}")
print(f"Private mean: {noisy_stats['mean_final_mark']}")
```

### Individual Queries

```python
# Query specific statistics
mean_with_noise = analytics.query_mean_final_mark(epsilon=0.5)
pass_rate = analytics.query_pass_rate(epsilon=0.3)
count = analytics.query_count(epsilon=0.2)

# Evaluate utility
results = analytics.dp_queries(epsilon=0.5)
utility = analytics.evaluate_utility(results)
print(utility)
```

### Privacy Budget Management

```python
from DP_Analytics_Students import PrivacyBudget

# Create budget
budget = PrivacyBudget(epsilon_total=1.5)

# Allocate to queries
eps1 = budget.spend(0.3)
eps2 = budget.spend(0.4)
eps3 = budget.spend(0.5)

# Check status
print(budget.summary())
# {'total_budget': 1.5, 'spent': 1.2, 'remaining': 0.3}
```

---

##  Explore the Notebook

For in-depth learning, run the Jupyter notebook:

```bash
jupyter notebook DP_Students_Analytics.ipynb
```

This covers:
-  Data exploration
-  Privacy concepts
- Mechanism comparison
-  Sensitivity analysis
-  Trade-off experiments

---

##  Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**: Ensure virtual environment is activated and requirements installed:
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: students.csv not found"

**Solution**: Verify you're in the correct directory:
```bash
# From the project root directory
ls students.csv  # or 'dir' on Windows
```

### Issue: Streamlit shows blank page

**Solution**: Check the terminal for error messages and restart:
```bash
Ctrl+C  # Stop current process
streamlit run app.py  # Restart
```

### Issue: Slow computation with high trial numbers

**Solution**: Reduce trials or increase epsilon (faster convergence):
```python
# Use fewer trials
results = analytics.dp_queries(epsilon=0.5)  # Runs once
```

---

## Common Workflows

### Workflow 1: Privacy-First Analysis

```python
# Strong privacy, understand utility loss
epsilon = 0.1
mechanism = "laplace"
results = analytics.dp_queries(epsilon, mechanism)
utility = analytics.evaluate_utility(results)
```

### Workflow 2: Balanced Approach

```python
# Good privacy with reasonable accuracy
epsilon = 0.8
mechanism = "gaussian"
results = analytics.dp_queries(epsilon, mechanism, equal_split=True)
```

### Workflow 3: High Utility (Low Privacy)

```python
# Accurate results, weaker privacy
epsilon = 2.0
mechanism = "gaussian"
results = analytics.dp_queries(epsilon, mechanism)
```

### Workflow 4: Multi-Query Analysis

```python
from DP_Analytics_Students import PrivacyBudget

budget = PrivacyBudget(1.0)

# Run multiple queries with shared budget
q1 = analytics.query_mean_final_mark(budget.spend(0.3))
q2 = analytics.query_pass_rate(budget.spend(0.3))
q3 = analytics.query_count(budget.spend(0.4))

print(f"Remaining budget: {budget.remaining()}")
```


##  Next Steps

1. **Run the dashboard** - Get familiar with the UI
2. **Try different epsilons** - See privacy-accuracy trade-offs
3. **Read the notebook** - Understand the math
4. **Use as a module** - Integrate into your code
5. **Contribute** - Help improve the project!
