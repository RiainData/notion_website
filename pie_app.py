import streamlit as st
import pandas as pd
import plotly.express as px
import os
import kagglehub

# --- PAGE CONFIG ---
st.set_page_config(layout="wide")

# --- LOAD DATASET ---
@st.cache_data
def load_dataset():
    dataset_path = kagglehub.dataset_download("teejmahal20/airline-passenger-satisfaction")
    csv_path = os.path.join(dataset_path, "train.csv")
    df = pd.read_csv(csv_path)
    return df

df = load_dataset()

# --- DEFINE PIE CHART FUNCTION ---
def plot_pie_chart(data, column, title):
    counts = data[column].value_counts()
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        hole=0.3,
        title=title,
    )
    fig.update_traces(textinfo="percent+label", pull=[0.05]*len(counts))
    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    return fig

# --- STREAMLIT LAYOUT ---
st.write("")  # Empty line to give some spacing

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_pie_chart(df, "Customer Type", "Customer Type Distribution"), use_container_width=True)
with col2:
    st.plotly_chart(plot_pie_chart(df, "Gender", "Gender Distribution"), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(plot_pie_chart(df, "Class", "Class Distribution"), use_container_width=True)
with col4:
    st.plotly_chart(plot_pie_chart(df, "satisfaction", "Satisfaction Levels"), use_container_width=True)
