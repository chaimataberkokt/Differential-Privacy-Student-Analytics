import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from DP_Analytics_Students import DP_Analytics_Students, PrivacyBudget


# PAGE CONFIGURATION


st.set_page_config(
    page_title="DP Student Analytics",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔒 Differential Privacy Student Analytics Dashboard")
st.markdown("---")


# SIDEBAR CONTROLS


st.sidebar.header("⚙️ Privacy Controls")

epsilon = st.sidebar.slider(
    "Privacy Budget (ε)",
    min_value=0.01,
    max_value=5.0,
    value=0.5,
    step=0.01,
    help="Lower ε = stronger privacy but more noise. Higher ε = better accuracy but weaker privacy."
)

mechanism = st.sidebar.selectbox(
    "Noise Mechanism",
    options=["laplace", "gaussian"],
    help="Laplace: strict ε-DP. Gaussian: approximate (ε,δ)-DP."
)

num_trials = st.sidebar.slider(
    "Number of Trials",
    min_value=1,
    max_value=100,
    value=10,
    help="More trials give more stable error estimates."
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Privacy vs Accuracy Trade-off:**
    - 🔐 **Low ε** (0.01-0.2): Maximum privacy, high noise
    - ⚖️ **Medium ε** (0.3-1.0): Balanced privacy & utility
    - 🎯 **High ε** (1.0+): Better accuracy, weaker privacy
    """
)


# LOAD AND INITIALIZE


@st.cache_resource
def load_analytics():
    """Load the analytics backend (cached for performance)."""
    return DP_Analytics_Students("students.csv", pass_threshold=10)


with st.spinner("Loading analytics system..."):
    analytics = load_analytics()

dataset_profile = analytics.get_dataset_profile()
df = analytics.get_data()


# SECTION 1: DATASET OVERVIEW


st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Students",
        value=f"{dataset_profile['students_count']}",
        delta="N"
    )

with col2:
    st.metric(
        label="Pass Rate",
        value=f"{dataset_profile['pass_rate']:.2%}",
        delta="Actual"
    )

with col3:
    final_min, final_max = dataset_profile['final_mark_range']
    st.metric(
        label="Final Mark Range",
        value=f"{final_min:.1f} - {final_max:.1f}",
        delta="Score Range"
    )

with col4:
    st.metric(
        label="Pass Threshold",
        value=f"{dataset_profile['pass_threshold']:.1f}",
        delta="Out of 20"
    )

st.markdown("---")

# Dataset preview
with st.expander("🔍 View Raw Data", expanded=False):
    st.subheader("First 10 Rows of Processed Dataset")
    st.dataframe(
        df[["id", "final_mark", "participation_avg", "quiz_avg", "passed"]].head(10),
        use_container_width=True
    )
    st.write(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")

st.markdown("---")


# SECTION 2: TRUE vs PRIVATE STATISTICS


st.header("📈 True vs Differentially Private Statistics")

# Run DP queries
results = analytics.dp_queries(epsilon=epsilon, mechanism=mechanism, equal_split=True)
true_stats = results["true_stats"]
noisy_stats = results["noisy_stats"]

# Create comparison dataframe
comparison_data = []
for key in true_stats.keys():
    comparison_data.append({
        "Statistic": key.replace("_", " ").title(),
        "True Value": f"{true_stats[key]:.4f}",
        "Private Value": f"{noisy_stats[key]:.4f}",
        "Absolute Error": f"{abs(true_stats[key] - noisy_stats[key]):.4f}",
        "Relative Error %": f"{abs(true_stats[key] - noisy_stats[key]) / abs(true_stats[key]) * 100:.2f}%" if true_stats[key] != 0 else "N/A"
    })

comparison_df = pd.DataFrame(comparison_data)

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Side-by-side metric comparison
st.subheader("Key Metrics Comparison")

metrics_display = [
    ("mean_final_mark", "Mean Final Mark"),
    ("mean_participation", "Mean Participation"),
    ("pass_rate", "Pass Rate"),
]

for metric_key, metric_label in metrics_display:
    col1, col2, col3, col4 = st.columns(4)
    
    true_val = true_stats[metric_key]
    noisy_val = noisy_stats[metric_key]
    abs_error = abs(true_val - noisy_val)
    rel_error = (abs_error / abs(true_val) * 100) if true_val != 0 else 0
    
    with col1:
        st.metric(f"{metric_label} (True)", f"{true_val:.4f}")
    
    with col2:
        st.metric(f"{metric_label} (Private)", f"{noisy_val:.4f}")
    
    with col3:
        st.metric("Abs Error", f"{abs_error:.4f}", delta=f"{-abs_error:.4f}")
    
    with col4:
        st.metric("Rel Error %", f"{rel_error:.2f}%")

st.markdown("---")


# SECTION 3: ERROR ANALYSIS


st.header("📉 Error Analysis")

# Run multiple trials
trial_results = []

for trial in range(num_trials):
    trial_res = analytics.dp_queries(epsilon=epsilon, mechanism=mechanism, equal_split=True)
    for key in trial_res["true_stats"].keys():
        true_val = trial_res["true_stats"][key]
        noisy_val = trial_res["noisy_stats"][key]
        abs_err = abs(true_val - noisy_val)
        rel_err = (abs_err / abs(true_val) * 100) if true_val != 0 else 0
        
        trial_results.append({
            "Trial": trial + 1,
            "Statistic": key,
            "True Value": true_val,
            "Private Value": noisy_val,
            "Absolute Error": abs_err,
            "Relative Error %": rel_err
        })

trial_df = pd.DataFrame(trial_results)

# Error statistics table
st.subheader(f"Error Statistics Across {num_trials} Trials")

error_summary = trial_df.groupby("Statistic").agg({
    "Absolute Error": ["mean", "std", "min", "max"],
    "Relative Error %": ["mean", "std"]
}).round(4)

st.dataframe(error_summary, use_container_width=True)

st.markdown("---")

# SECTION 4: VISUALIZATIONS


st.header("📊 Visualizations")

# Visualization 1: Histogram of Final Marks
st.subheader("Distribution of Final Marks")

fig_hist = go.Figure()
fig_hist.add_trace(go.Histogram(
    x=df["final_mark"],
    nbinsx=20,
    name="Final Mark",
    marker_color="rgba(0, 100, 200, 0.7)"
))
fig_hist.update_layout(
    xaxis_title="Final Mark",
    yaxis_title="Frequency",
    showlegend=False,
    height=400
)
st.plotly_chart(fig_hist, use_container_width=True)

# Visualization 2: True vs Private Values Bar Chart
st.subheader("True vs Private Statistics Comparison")

comparison_for_chart = {
    "Mean Final Mark": (true_stats["mean_final_mark"], noisy_stats["mean_final_mark"]),
    "Mean Participation": (true_stats["mean_participation"], noisy_stats["mean_participation"]),
    "Mean Quiz Avg": (true_stats["mean_quiz_avg"], noisy_stats["mean_quiz_avg"]),
    "Pass Rate": (true_stats["pass_rate"], noisy_stats["pass_rate"]),
}

fig_bar = go.Figure(data=[
    go.Bar(
        name="True Value",
        x=list(comparison_for_chart.keys()),
        y=[v[0] for v in comparison_for_chart.values()],
        marker_color="rgba(0, 150, 0, 0.7)"
    ),
    go.Bar(
        name="Private Value (ε={})".format(epsilon),
        x=list(comparison_for_chart.keys()),
        y=[v[1] for v in comparison_for_chart.values()],
        marker_color="rgba(255, 100, 0, 0.7)"
    )
])
fig_bar.update_layout(
    barmode="group",
    height=400,
    xaxis_title="Statistics",
    yaxis_title="Value",
    hovermode="x unified"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Visualization 3: Error Distribution Across Trials
st.subheader("Error Distribution Across Trials")

fig_error = go.Figure()

for stat in trial_df["Statistic"].unique():
    stat_data = trial_df[trial_df["Statistic"] == stat]
    fig_error.add_trace(go.Box(
        y=stat_data["Absolute Error"],
        name=stat.replace("_", " ").title(),
        boxmean="sd"
    ))

fig_error.update_layout(
    height=400,
    yaxis_title="Absolute Error",
    xaxis_title="Statistic",
    showlegend=True
)
st.plotly_chart(fig_error, use_container_width=True)

# Visualization 4: Privacy-Accuracy Trade-off Curve
st.subheader("Privacy-Accuracy Trade-off Curve")

epsilons_range = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]
tradeoff_results = []

with st.spinner("Computing trade-off curve..."):
    for eps in epsilons_range:
        trial_errors = []
        for _ in range(5):  # 5 trials per epsilon
            res = analytics.dp_queries(epsilon=eps, mechanism=mechanism, equal_split=True)
            true_val = res["true_stats"]["mean_final_mark"]
            noisy_val = res["noisy_stats"]["mean_final_mark"]
            trial_errors.append(abs(true_val - noisy_val))
        
        avg_error = np.mean(trial_errors)
        tradeoff_results.append({
            "epsilon": eps,
            "avg_error": avg_error,
            "std_error": np.std(trial_errors)
        })

tradeoff_df = pd.DataFrame(tradeoff_results)

fig_tradeoff = go.Figure()
fig_tradeoff.add_trace(go.Scatter(
    x=tradeoff_df["epsilon"],
    y=tradeoff_df["avg_error"],
    error_y=dict(
        type='data',
        array=tradeoff_df["std_error"],
        visible=True
    ),
    mode='lines+markers',
    name='Mean Absolute Error',
    marker=dict(size=8, color='rgba(200, 50, 50, 0.8)'),
    line=dict(color='rgba(200, 50, 50, 0.8)', width=2)
))
fig_tradeoff.update_layout(
    xaxis_title="Privacy Budget (ε)",
    yaxis_title="Mean Absolute Error (Mean Final Mark)",
    title="Privacy-Accuracy Trade-off",
    height=400,
    showlegend=True,
    hovermode="x unified"
)
st.plotly_chart(fig_tradeoff, use_container_width=True)

st.markdown("---")


# SECTION 5: INSIGHTS & EXPLANATIONS


st.header("💡 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔐 Privacy-Accuracy Trade-off")
    
    if epsilon < 0.2:
        privacy_level = "🔓 **VERY STRONG PRIVACY**"
        accuracy_level = "📉 Very High Noise"
        explanation = "Epsilon is very small. You get maximum privacy protection, but the results are heavily distorted by noise."
    elif epsilon < 0.5:
        privacy_level = "🔒 **STRONG PRIVACY**"
        accuracy_level = "📊 Moderate Noise"
        explanation = "Epsilon is low. Good privacy with some accuracy loss. Suitable for sensitive applications."
    elif epsilon < 1.0:
        privacy_level = "⚖️ **BALANCED**"
        accuracy_level = "📈 Low Noise"
        explanation = "Epsilon is moderate. Good balance between privacy and utility. Recommended for most use cases."
    elif epsilon < 2.0:
        privacy_level = "🎯 **WEAKER PRIVACY**"
        accuracy_level = "✅ Very Low Noise"
        explanation = "Epsilon is high. Results are highly accurate but privacy is weaker."
    else:
        privacy_level = "⚠️ **WEAK PRIVACY**"
        accuracy_level = "🎯 Minimal Noise"
        explanation = "Epsilon is very high. Near-true results but limited privacy protection."
    
    st.write(f"**Current Setting: ε = {epsilon}**")
    st.write(f"**Privacy Level:** {privacy_level}")
    st.write(f"**Accuracy:** {accuracy_level}")
    st.write(f"**Interpretation:** {explanation}")

with col2:
    st.subheader("📊 Current Results Summary")
    
    avg_abs_error = trial_df["Absolute Error"].mean()
    avg_rel_error = trial_df["Relative Error %"].mean()
    
    st.write(f"**Mechanism:** {mechanism.upper()}")
    st.write(f"**Number of Trials:** {num_trials}")
    st.write(f"**Avg Absolute Error:** {avg_abs_error:.4f}")
    st.write(f"**Avg Relative Error:** {avg_rel_error:.2f}%")
    
    if avg_rel_error < 5:
        st.success("✅ Results are highly accurate!")
    elif avg_rel_error < 15:
        st.info("⚠️ Results are reasonably accurate with some noise.")
    else:
        st.warning("⚠️ Results show significant noise. Consider increasing epsilon.")

st.markdown("---")

st.subheader("🎓 How Differential Privacy Works")

with st.expander("Learn More", expanded=False):
    st.markdown("""
    ### What is Differential Privacy?
    
    Differential Privacy (DP) is a mathematical framework that protects individual data 
    while allowing useful aggregate statistics.
    
    **Key Idea:** The output should not change significantly whether or not a single 
    student's data is included.
    
    ### Mechanisms Used
    
    **1. Laplace Mechanism (ε-DP):**
    - Adds noise from Laplace distribution: Noise ~ Laplace(0, Δ/ε)
    - Provides strict privacy guarantees
    - Best for simple queries like counts
    
    **2. Gaussian Mechanism ((ε,δ)-DP):**
    - Adds noise from Normal distribution: Noise ~ N(0, σ²)
    - Where σ = √(2·ln(1.25/δ)) · Δ/ε
    - Smoother noise, good for averages
    
    ### Sensitivity
    
    Sensitivity measures how much a query can change when one record is added/removed:
    - **Count Sensitivity:** Δ = 1
    - **Mean Sensitivity:** Δ = (max - min) / n
    - **Pass Rate Sensitivity:** Δ = 1 / n
    
    ### Privacy Budget (ε)
    
    - **Small ε:** Strong privacy, high noise
    - **Large ε:** Weak privacy, low noise
    - Multiple queries share the same budget
    
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🔒 Differential Privacy Student Analytics Dashboard</p>
    <p><small>Built with Streamlit | Backend: DP_Analytics_Students.py</small></p>
</div>
""", unsafe_allow_html=True)
