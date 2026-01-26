import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
lob_df = pd.read_csv('Level 1.xlsx - LOB Comparison.csv')
regional_df = pd.read_csv('Level 1.xlsx - Regional Performance Comparison.csv')
outlet_df = pd.read_csv('Level 1.xlsx - Outlet Performance Comparison.csv')

# Page Config
st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.title("Performance Dashboard")
    st.info("This dashboard provides a summary of regional and product performance.")
    st.markdown("---")
    st.selectbox("Select View", ["Overview", "Regional Detail", "LOB Analysis"])

# Main Column
col1, col2 = st.columns([1, 4]) # Sidebar simulated or using st.sidebar

# Row 1: Data Cards
t_pass = regional_df['Pass'].sum()
t_fail = regional_df['Fail'].sum()
t_hc = regional_df['Total Headcount'].sum()
pass_rate = (t_pass / t_hc) * 100

r1_col1, r1_col2, r1_col3 = st.columns(3)
r1_col1.metric("Total Pass", t_pass)
r1_col2.metric("Total Fail", t_fail)
r1_col3.metric("Pass Rate", f"{pass_rate:.1f}%")

# Row 2: Graphs
st.markdown("### Performance Visualizations")
r2_col1, r2_col2 = st.columns(2)

with r2_col1:
    fig_reg = px.bar(regional_df, x='Region', y=['Pass', 'Fail'], barmode='group', title="Regional Performance")
    st.plotly_chart(fig_reg, use_container_width=True)

with r2_col2:
    # Melting LOB data for plotting
    lob_melted = lob_df.melt(id_vars='Result', var_name='Region', value_name='Count')
    fig_lob = px.bar(lob_melted, x='Result', y='Count', color='Region', title="LOB Comparison by Region")
    st.plotly_chart(fig_lob, use_container_width=True)

# Row 3: Data Table
st.markdown("### Detailed Data Table")
st.dataframe(regional_df, use_container_width=True)
