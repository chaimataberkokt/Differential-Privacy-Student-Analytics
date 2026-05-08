#  Differential Privacy Student Analytics System

A comprehensive educational project demonstrating differential privacy techniques applied to student performance analytics. This system computes meaningful statistics about student grades, participation, and success rates while mathematically guaranteeing that individual student data cannot be inferred.


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [How Differential Privacy Works](#how-differential-privacy-works)
- [Optimal Epsilon Search](#optimal-epsilon-search)
- [Dataset](#dataset)
- [Technical Details](#technical-details)
- [Results & Visualizations](#results--visualizations)
- [Contributing ](#contributing)
- [Requirements](#Requirements)
---

## Overview

This project addresses a critical challenge in educational data analysis: **How can we share useful statistics about student performance without compromising individual privacy?**

The system integrates **Differential Privacy** mechanisms to add carefully calibrated noise to aggregate statistics, ensuring that:

No single student's data can be inferred from published results  
 Results remain statistically useful for institutional decision-making  
 Privacy vs. accuracy trade-offs are clearly visible and quantifiable  
Privacy budget management prevents privacy loss from multiple queries  

**Use Cases:**
- Educational institutions publishing aggregate performance statistics
- Research studies analyzing student outcomes
- Benchmarking and comparative analysis across cohorts
- Regulatory compliance for sensitive educational data

---

##  Features

### Core Privacy Mechanisms

| Mechanism | Formula | Use Case |
|-----------|---------|----------|
| **Laplace** | `Noise ~ Laplace(0, Δ/ε)` | Strict ε-DP guarantees, simple queries |
| **Gaussian** | `Noise ~ N(0, σ²)` where `σ = √(2·ln(1.25/δ))·Δ/ε` | Approximate (ε,δ)-DP, smoother noise |

### Statistics Computed

- **Mean Final Mark** - Average course performance
- **Mean Participation** - Average engagement level
- **Mean Quiz Average** - Average quiz performance
- **Count** - Number of students (with noise)
- **Pass Rate** - Proportion of students passing

### Interactive Dashboard

The Streamlit app provides:

- **Real-time Privacy Controls**: Adjust epsilon and mechanism on the fly
- **Dataset Overview**: Key metrics and raw data preview
- **True vs Private Comparison**: Side-by-side metric comparison
- **Error Analysis**: Quantify noise introduced by privacy
- **Advanced Visualizations**:
  - Final mark distribution histograms
  - True vs private value bar charts
  - Error distribution box plots
  - Privacy-accuracy trade-off curves
- **Educational Insights**: Privacy level assessment and recommendations
- **Multiple Trials**: Run repeated queries to observe noise variance

###  Jupyter Notebook

Complete exploratory analysis including:
- Data loading and preprocessing
- Privacy risk demonstration
- True statistics computation
- Sensitivity analysis
- Mechanism comparison (Laplace vs Gaussian)
- Utility evaluation with error metrics
- Privacy budget management
- Epsilon trade-off experiments

---

##  Project Structure

```
CNS Primary Project/
├── README.md                      # Main project documentation
├── QUICKSTART.md                  # Quick setup and usage guide
├── .gitignore                     # Git ignore configuration
├── setup.py                       # Python package setup
├── requirements.txt               # Python dependencies (pinned versions)
├── DP_Students_Analytics.ipynb    # Jupyter notebook with full analysis
├── DP_Analytics_Students.py       # Production Python module (backend)
├── app.py                         # Streamlit dashboard (frontend)
└── students.csv                   # Student dataset (260 students, 11 features)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive project documentation with all details |
| `QUICKSTART.md` | Setup guide and common workflows |
| `.gitignore` | Git configuration to exclude unnecessary files |
| `setup.py` | PyPI package configuration and metadata |
| `requirements.txt` | Pinned Python package versions for reproducibility |
| `DP_Students_Analytics.ipynb` | Complete educational notebook with explanations, visualizations, and experiments |
| `DP_Analytics_Students.py` | Reusable Python module containing core DP algorithms and data processing |
| `app.py` | Interactive Streamlit dashboard for visualization and experimentation |
| `students.csv` | Student performance dataset (260 students, 11 features) |

---

##  Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/chaimataberkokt/Differential-Privacy-Student-Analytics
cd dp-student-analytics
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install streamlit pandas numpy matplotlib plotly jupyter scipy
```

### Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit {streamlit.__version__} installed')"
```

---

##  Quick Start

### Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

### Run the Jupyter Notebook

```bash
jupyter notebook DP_Students_Analytics.ipynb
```

### Use as Python Module

```python
from DP_Analytics_Students import DP_Analytics_Students

# Initialize system
analytics = DP_Analytics_Students("students.csv", pass_threshold=10)

# Get dataset profile
profile = analytics.get_dataset_profile()
print(profile)

# Run DP query with epsilon=0.5
results = analytics.dp_queries(epsilon=0.5, mechanism="laplace", equal_split=True)

# Evaluate utility
utility = analytics.evaluate_utility(results)
print(utility)
```

---

##  Usage Guide

### Dashboard Controls

1. **Sidebar Settings**:
   - Adjust **Privacy Budget (ε)** to see real-time changes in results
   - Select **Noise Mechanism** (Laplace/Gaussian)
   - Set **Number of Trials** for error estimation

2. **Main Sections**:
   - **Dataset Overview**: Understand your data characteristics
   - **True vs Private**: Compare original and private statistics
   - **Error Analysis**: See how much noise is introduced
   - **Visualizations**: Explore privacy-accuracy trade-offs
   - **Insights**: Get recommendations based on epsilon

### Interpreting Results

#### Privacy Levels

| Epsilon Range | Privacy | Accuracy | Best For |
|---|---|---|---|
| 0.01 - 0.1 |  Very Strong | Very Low | Maximum privacy requirement |
| 0.1 - 0.5 |  Strong | Low-Moderate | Sensitive applications |
| 0.5 - 1.0 |  Balanced | Moderate-High | Most use cases (Recommended) |
| 1.0 - 2.0 |  Moderate | High | Analysis requiring accuracy |
| 2.0+ |  Weak | Very High | Non-sensitive data |

#### Error Metrics

- **Absolute Error**: Raw difference between true and private values
- **Relative Error %**: Error as percentage of true value
- **MAE (Mean Absolute Error)**: Average error across trials
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors more

### Example Workflows

#### Scenario 1: Maximum Privacy

```
Set epsilon = 0.1
Mechanism = Laplace
Expected: ~80-90% relative error, strongest privacy
```

#### Scenario 2: Balanced Approach

```
Set epsilon = 0.5
Mechanism = Laplace
Expected: ~10-20% relative error, good privacy
```

#### Scenario 3: High Utility

```
Set epsilon = 1.5
Mechanism = Gaussian
Expected: ~2-5% relative error, moderate privacy
```

---

##  How Differential Privacy Works

### The Core Concept

Differential privacy ensures that the output of an analysis changes very little whether or not a single individual's data is included.

**Formal Definition:**
An algorithm M is (ε, δ)-differentially private if for any two datasets D and D' differing by one record:

```
P[M(D) ∈ S] ≤ e^ε · P[M(D') ∈ S] + δ
```

### Key Concepts

#### 1. Sensitivity (Δ)

Measures how much a query's output can change when one record is added/removed:

- **Count Sensitivity**: Δ = 1 (always)
- **Mean Sensitivity**: Δ = (max - min) / n
- **Pass Rate Sensitivity**: Δ = 1 / n

*High sensitivity → Need more noise → Weaker utility*

#### 2. Privacy Budget (ε)

The total amount of privacy you "spend" across all queries:

- Smaller ε = Stronger privacy but more noise
- Larger ε = Weaker privacy but less noise
- **Composition Rule**: Total privacy = sum of individual ε values

#### 3. Noise Mechanisms

**Laplace Mechanism (Strict ε-DP):**
```
Noisy_Value = True_Value + Laplace(0, Δ/ε)
```
- Sharp, concentrated noise
- Best for worst-case privacy
- Good for counts and simple aggregates

**Gaussian Mechanism (Approximate (ε,δ)-DP):**
```
Noisy_Value = True_Value + N(0, σ²)
where σ = √(2·ln(1.25/δ)) · Δ/ε
```
- Smooth, normal-distributed noise
- Better average-case privacy
- Good for means and continuous values

---

##  Optimal Epsilon Search

### Overview

**Challenge:** How do you choose the right epsilon value for your use case?

Manual selection is difficult because the relationship between epsilon and accuracy is non-linear and task-dependent. Too small an epsilon sacrifices utility; too large defeats the privacy purpose.

**Solution:** This project implements an **automated two-phase grid search with elbow detection** to find the optimal epsilon value that balances privacy and utility.

### The Two-Phase Approach

#### Phase 1: Coarse-Grain Search
- Searches epsilon values at **large intervals** (e.g., 0.01 to 2.0 in steps of 0.2)
- Identifies the approximate region where accuracy improves most
- Fast exploration of the full privacy-accuracy curve

#### Phase 2: Fine-Grain Search
- Zooms into the promising region found in Phase 1
- Uses **smaller intervals** (e.g., 0.01 steps) for precision
- Finds the exact elbow point and threshold values

### Elbow Detection Algorithm

The algorithm identifies the **elbow point** — the epsilon value where:
- Increasing epsilon **below** the elbow dramatically reduces error
- Increasing epsilon **above** the elbow barely improves accuracy
- At the elbow, you get the best privacy-utility balance

**Mathematical basis:** The algorithm computes the rate of change in error as epsilon increases and finds where this rate drops significantly.

### Key Outputs

The search produces three critical values:

| Value | Meaning | When to Use |
|-------|---------|------------|
| **Elbow Epsilon** | Best overall balance between privacy and accuracy | Default choice for most use cases |
| **Threshold Epsilon** | Smallest epsilon achieving your target error | When you have specific accuracy requirements |
| **Privacy-Accuracy Curve** | Complete mapping of epsilon vs. error | Understanding trade-offs |

### Why Grid Search?

The relationship between epsilon and noise is **deterministic and mathematical** — there's nothing to learn or optimize using machine learning. A grid search is:

-  **Exact**: Finds the true optimal value
-  **Fast**: Completes in seconds for real datasets
-  **Interpretable**: Every step is transparent and explainable
-  **Reproducible**: Same data always gives same results

### Using Optimal Epsilon Search

#### In the Dashboard

1. Open the Streamlit app
2. Go to **Sidebar → Optimal ε Finder**
3. Check **"Find optimal ε for this data"**
4. Select the statistic to optimize for (Mean Final Mark, Pass Rate, etc.)
5. Set your **Target relative error** threshold
6. The system runs the search and displays:
   - Elbow point (recommended epsilon)
   - Threshold epsilon (for your target error)
   - Full privacy-accuracy visualization

#### In Python Code

```python
from DP_Analytics_Students import DP_Analytics_Students

analytics = DP_Analytics_Students("students.csv", pass_threshold=10)

# Run optimal epsilon search
results = analytics.find_optimal_epsilon(
    metric="mean_final_mark",
    target_error=5.0,  # 5% relative error
    mechanism="laplace"
)

optimal_eps = results["optimal_epsilon"]
print(f"Recommended epsilon: {optimal_eps:.4f}")
```

### Example Results

For the student analytics dataset optimizing for **Mean Final Mark**:

```
Coarse Search (Phase 1):
  ε = 0.01 → Error: 87.3%
  ε = 0.2  → Error: 21.5%
  ε = 0.4  → Error: 8.2%     ← Elbow region identified
  ε = 0.6  → Error: 4.1%
  ε = 1.0  → Error: 1.8%

Fine Search (Phase 2):
  ε = 0.35 → Error: 11.2%
  ε = 0.40 → Error: 8.3%     ← ELBOW POINT
  ε = 0.45 → Error: 6.1%
  ε = 0.50 → Error: 4.8%

Results:
  Optimal epsilon (elbow):    0.40
  Threshold epsilon (5% target): 0.47
  Recommended privacy level:  Strong
```

### Interpretation Guide

#### Below the Elbow
- Increasing epsilon gives **large accuracy gains**
- Strong privacy is sacrificed for little utility improvement
-  Not recommended

#### At the Elbow
- Best **balance** of privacy and accuracy
- Further increases give **diminishing returns**
-  **Default recommendation**

#### Above the Elbow
- Accuracy improves slowly with larger epsilon
- Privacy protection becomes weak
- Consider only if accuracy requirement is strict

### Advanced Options

#### Choosing the Optimization Metric

- **mean_final_mark**: Overall course performance
- **mean_participation**: Student engagement
- **mean_quiz_avg**: Assessment performance
- **pass_rate**: Student success rates

Different metrics may have different optimal epsilons due to varying sensitivities.

#### Target Error Selection

- **1-2%**: Nearly as accurate as non-private results (weak privacy)
- **5%**: Good accuracy with reasonable privacy (recommended)
- **10%**: Accepts some accuracy loss for stronger privacy
- **20%+**: Maximum privacy, sacrifices accuracy significantly

---

##  Dataset

### Source
Introduction to Artificial Intelligence module (2024/2025 academic year)

### Characteristics

| Attribute | Details |
|-----------|---------|
| **Students** | 260 students |
| **Features** | 11 evaluation components |
| **Data Type** | Real student performance records |
| **Privacy** | Anonymized for research use |

### Features Included

- **ID**: Student identifier
- **Quiz 1, Quiz 2, Quiz 3**: Individual quiz scores
- **Participation Tutorials**: Tutorial participation score
- **Participation Labs**: Lab participation score
- **Participation Avg**: Average participation
- **Project Mark**: Project assignment score
- **Midterm Mark**: Midterm exam score
- **Semester Work**: Overall semester work score
- **Final Mark**: Final examination score
- **Course Mark**: Overall course score

### Derived Features

- **Quiz Avg**: Average of Quiz 1, Quiz 2, Quiz 3
- **Passed**: Binary (1 if course_mark ≥ 10/20, else 0)

---

## Technical Details

### Architecture

```
┌─────────────────────────────────────────────────┐
│        Streamlit Dashboard (app.py)             │
│  - UI Controls                                  │
│  - Visualizations (Plotly)                      │
│  - Interactive Experiments                      │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│   DP_Analytics_Students.py (Core Module)        │
│  - Data Loading & Preprocessing                 │
│  - True Statistics Computation                  │
│  - Sensitivity Calculation                      │
│  - DP Mechanisms (Laplace & Gaussian)           │
│  - Query Functions                              │
│  - Utility Metrics                              │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│         Data Layer                              │
│  - students.csv                                 │
│  - Pandas DataFrame                             │
└─────────────────────────────────────────────────┘
```

### Class Structure

#### `DP_Analytics_Students`

Main class handling all operations:

```python
# Initialization
analytics = DP_Analytics_Students(csv_path, pass_threshold=10)

# Methods
- query_mean_final_mark(epsilon, mechanism)
- query_mean_participation(epsilon, mechanism)
- query_mean_quiz_avg(epsilon, mechanism)
- query_count(epsilon, mechanism)
- query_pass_rate(epsilon, mechanism)
- dp_queries(epsilon, mechanism, equal_split)
- evaluate_utility(results)
- get_dataset_profile()
- get_data()
```

#### `PrivacyBudget`

Manages privacy budget allocation:

```python
budget = PrivacyBudget(epsilon_total=1.5)
eps_allocated = budget.spend(0.3)
remaining = budget.remaining()
```

### Data Flow

1. **CSV → DataFrame**: Load and parse student data
2. **Preprocessing**: Normalize columns, compute derived features
3. **True Computation**: Calculate actual statistics
4. **Sensitivity Analysis**: Compute Δ for each query
5. **Noise Generation**: Sample from Laplace or Gaussian
6. **Result Aggregation**: Combine and return results

---

## Results & Visualizations

### Key Findings

#### Privacy-Accuracy Trade-off

The dashboard reveals that:

- **ε = 0.1**: 80-90% error (maximum privacy)
- **ε = 0.5**: 10-20% error (good balance)
- **ε = 1.0**: 5-10% error (near-accurate)
- **ε = 2.0+**: <5% error (approaching true values)

#### Mechanism Comparison

- **Laplace**: More stable, sharper noise peaks
- **Gaussian**: Smoother noise distribution, better for averages

#### Sensitivity Ranking

1. Mean Final Mark (highest sensitivity)
2. Mean Participation
3. Mean Quiz Average
4. Pass Rate (lowest sensitivity)

### Interpretation Guide

 **Lower epsilon values** = Stronger privacy, more noise distortion
 **Higher epsilon values** = Weaker privacy, results closer to truth
 **Optimal range** = 0.5-1.0 for most institutional use cases

---

##  Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Additional statistical queries (median, percentiles)
- [ ] More noise mechanisms (exponential mechanism, etc.)
- [ ] Multi-user privacy budget system
- [ ] Real-time auditing and logging
- [ ] Advanced filtering and segmentation
- [ ] Export capabilities (PDF, CSV reports)
- [ ] Mobile-responsive dashboard
- [ ] API endpoint for remote access

### Steps to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


##  Requirements

```
streamlit>=1.28.0
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
plotly>=5.0.0
jupyter>=1.0.0
scipy>=1.7.0
```

See `requirements.txt` for pinned versions.

## FAQ

### Q: Why add noise if it reduces accuracy?
**A:** Privacy and utility are inherent trade-offs. The noise prevents inference attacks on individual data while maintaining statistical usefulness for institutional decision-making.

### Q: Is epsilon a percentage?
**A:** No, epsilon is a privacy budget parameter. It's not a percentage. Smaller ε means stronger privacy guarantees mathematically, not numerically.

### Q: Can I use this with production data?
**A:** Yes, with appropriate security measures. Ensure proper access controls, encryption, and compliance with regulations like FERPA (educational records) or GDPR.

### Q: Which mechanism should I use?
**A:** For educational use: **Laplace** for simplicity and strict guarantees. For research: **Gaussian** for smoother results on averaged metrics.

### Q: How many trials do I need?
**A:** 10-50 trials give stable error estimates. More trials = more reliable statistics but slower computation.

---

