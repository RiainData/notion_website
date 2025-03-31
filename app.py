import streamlit as st
import plotly.express as px

# Load example data
df = px.data.gapminder().query("year == 2007")

# Create a Plotly chart
fig = px.scatter(df, 
                 x="gdpPercap", 
                 y="lifeExp", 
                 size="pop", 
                 color="continent", 
                 hover_name="country", 
                 log_x=True, 
                 size_max=60)

# Streamlit app layout
st.title("🌍 Life Expectancy vs GDP (2007)")
st.write("Interactive Plotly chart rendered via Streamlit.")
st.plotly_chart(fig)
