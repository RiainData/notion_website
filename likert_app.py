import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import kagglehub

# --- MUST BE FIRST STREAMLIT COMMAND ---
st.set_page_config(layout="wide")

# --- LOAD DATASET ---
@st.cache_data
def load_dataset():
    try:
        dataset_path = kagglehub.dataset_download("teejmahal20/airline-passenger-satisfaction")
        csv_path = os.path.join(dataset_path, "train.csv")
        df = pd.read_csv(csv_path)
        return df, csv_path
    except Exception as e:
        st.error(f"Dataset could not be loaded: {e}")
        st.stop()

df_train, csv_path = load_dataset()
st.success(f"Loaded dataset from: {csv_path}")

# --- SETUP ---
rating_features = [
    "Inflight wifi service", "Departure/Arrival time convenient", "Ease of Online booking",
    "Gate location", "Food and drink", "Online boarding", "Seat comfort", 
    "Inflight entertainment", "On-board service", "Leg room service", 
    "Baggage handling", "Checkin service", "Inflight service", "Cleanliness"
]

fig = make_subplots(
    rows=7, cols=2,
    subplot_titles=rating_features,
    vertical_spacing=0.08,
    horizontal_spacing=0.1
)

# --- ADD BARS TO SUBPLOTS ---
for i, feature in enumerate(rating_features):
    row = i // 2 + 1
    col = i % 2 + 1
    counts = df_train[feature].value_counts().sort_index()

    fig.add_trace(go.Bar(
        x=counts.index.astype(str),
        y=counts.values,
        width=0.55,
        marker=dict(
            color=counts.values,
            colorscale='Greens',
            line=dict(color='rgba(0,0,0,0.05)', width=2)
        ),
        hovertemplate=f'Feature: {feature}<br>Rating: %{{x}}<br>Count: %{{y}}<extra></extra>',
        showlegend=False
    ), row=row, col=col)

# --- STYLE ---
fig.update_layout(
    height=2800,
    title_text="Service Rating Distributions (0–5 Scale)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Courier New, monospace", color="black", size=12),
    margin=dict(t=100, l=50, r=50, b=50)
)

for i in range(len(rating_features)):
    row = i // 2 + 1
    col = i % 2 + 1
    fig.update_xaxes(title_text="Rating", gridcolor='rgba(0,0,0,0.05)', row=row, col=col)
    fig.update_yaxes(title_text="Count", gridcolor='rgba(0,0,0,0.05)', row=row, col=col)

# --- STREAMLIT LAYOUT ---
st.set_page_config(layout="wide")
st.title("🛫 Airline Survey Service Ratings Dashboard")
st.markdown("This dashboard displays the distribution of service feature ratings across passengers.")
st.plotly_chart(fig, use_container_width=True)
