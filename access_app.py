import pandas as pd
import plotly.graph_objects as go

selected_countries = [
    'United States', 'Iran', 'China', 'Germany', 'Saudi Arabia',
    'Russia', 'Brazil', 'Nigeria', 'India'
]

df_selected = df[df['entityName'].isin(selected_countries)].copy()
df_selected = df_selected.sort_values(['entityName', 'dataYear'])
df_selected['smoothed'] = df_selected.groupby('entityName')['dataValue'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())

custom_colors = {
    'United States': '#1f77b4',
    'China': '#d62728',
    'India': '#ff7f0e',
    'Germany': '#2ca02c',
    'Saudi Arabia': '#9467bd',
    'Russia': '#8c564b',
    'Brazil': '#e377c2',
    'Nigeria': '#7f7f7f',
    'Iran': '#17becf'
}

label_offsets = {
    'United States': 1.5,
    'Germany': -1.5,
    'China': 0.5,
    'India': -0.5,
    'Saudi Arabia': 0.8,
    'Russia': -0.8,
    'Brazil': 1.0,
    'Nigeria': -1.0,
    'Iran': 0
}

fig = go.Figure()

for country in selected_countries:
    country_data = df_selected[df_selected['entityName'] == country]
    
    if country_data.empty:
        continue

    fig.add_trace(go.Scatter(
        x=country_data['dataYear'],
        y=country_data['smoothed'],
        mode='lines',
        line=dict(color=custom_colors[country], width=3),
        name=country,
        showlegend=False
    ))

    last_row = country_data[country_data['dataYear'] == country_data['dataYear'].max()]
    if not last_row.empty:
        y_val = last_row['smoothed'].values[0] + label_offsets.get(country, 0)
        fig.add_annotation(
            x=last_row['dataYear'].values[0],
            y=y_val,
            text=f"<b>{country}</b>",
            font=dict(family="Courier New, monospace", size=12, color="black"),
            showarrow=False,
            xanchor='left'
        )

fig.update_layout(
    title='Internet Access Over Time (Key Global Countries)',
    xaxis_title='Year',
    yaxis_title='Internet Access (%)',
    template='plotly_white',
    font=dict(family="Courier New, monospace"),
    height=750,
    hovermode='x unified'
)

fig.show()