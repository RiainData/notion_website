import streamlit as st
import pandas as pd
import plotly.graph_objects as go


@st.cache_data
def load_data():
    url = "data/internet_access.csv"
    return pd.read_csv(url)


df = load_data()

default_countries = [
    "United States", "Iran", "China", "Germany",
    "Saudi Arabia", "Russia", "Brazil", "Nigeria", "India"
]

selected_countries = st.multiselect(
    "Choose countries to display",
    options=sorted(df["entityName"].unique()),
    default=default_countries
)

if not selected_countries:
    st.info("Select at least one country to see the chart.")
    st.stop()

df_selected = (
    df[df["entityName"].isin(selected_countries)]
    .sort_values(["entityName", "dataYear"])
    .copy()
)

df_selected["smoothed"] = (
    df_selected
    .groupby("entityName")["dataValue"]
    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

custom_colors = {
    "United States": "#1f77b4", "China": "#d62728", "India": "#ff7f0e",
    "Germany": "#2ca02c", "Saudi Arabia": "#9467bd", "Russia": "#8c564b",
    "Brazil": "#e377c2", "Nigeria": "#7f7f7f", "Iran": "#17becf"
}

label_offsets = {
    "United States": 1.5, "Germany": -1.5, "China": 0.5, "India": -0.5,
    "Saudi Arabia": 0.8, "Russia": -0.8, "Brazil": 1.0, "Nigeria": -1.0, "Iran": 0
}

fig = go.Figure()

for country in selected_countries:
    data = df_selected[df_selected["entityName"] == country]
    if data.empty:
        continue
    fig.add_trace(go.Scatter(
        x=data["dataYear"],
        y=data["smoothed"],
        mode="lines",
        line=dict(color=custom_colors.get(country, "#333"), width=3),
        name=country,
        showlegend=False
    ))
    last = data.iloc[-1]
    fig.add_annotation(
        x=last["dataYear"],
        y=last["smoothed"] + label_offsets.get(country, 0),
        text=f"<b>{country}</b>",
        showarrow=False,
        xanchor="left",
        font=dict(size=12)
    )

fig.update_layout(
    title="Internet Access Over Time",
    xaxis_title="Year",
    yaxis_title="Internet Access (%)",
    template="plotly_white",
    height=650,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
