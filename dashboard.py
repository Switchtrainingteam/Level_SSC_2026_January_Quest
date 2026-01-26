import streamlit as st
import pandas as pd
import numpy as np

# Set page layout to wide
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    lob_df = pd.read_csv("Level 1.xlsx - LOB Comparison.csv")
    region_df = pd.read_csv("Level 1.xlsx - Regional Performance Comparison.csv")
    outlet_df = pd.read_csv("Level 1.xlsx - Outlet Performance Comparison.csv")
    return lob_df, region_df, outlet_df

lob_df, region_df, outlet_df = load_data()

# --- layout: 2 Columns (Sidebar + Main) ---
# Streamlit uses st.sidebar for the first column
with st.sidebar:
    st.header("Dashboard Menu")
    st.markdown("---")
    region_filter = st.selectbox("Select Region", ["All"] + list(region_df['Region'].unique()))
    st.write("Use this sidebar to filter the data displayed in the main dashboard area.")
    st.markdown("---")
    st.info("Data Source: Level 1.xlsx")

# --- Main Content (Column 2) ---
# We will create 3 rows as requested

# Data Processing based on selection
if region_filter == "All":
    display_df = region_df
    total_pass = region_df['Pass'].sum()
    total_fail = region_df['Fail'].sum()
    total_hc = region_df['Total Headcount'].sum()
else:
    display_df = region_df[region_df['Region'] == region_filter]
    total_pass = display_df['Pass'].sum()
    total_fail = display_df['Fail'].sum()
    total_hc = display_df['Total Headcount'].sum()

pass_rate = (total_pass / total_hc * 100) if total_hc > 0 else 0

# ROW 1: Data Cards
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pass", f"{total_pass}")
col2.metric("Total Fail", f"{total_fail}")
col3.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# ROW 2: Graphs
st.subheader("Performance Analytics")
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.caption("Regional Performance (Pass vs Fail)")
    # Simple Bar Chart for Regions
    fig1, ax1 = plt.subplots()
    x = np.arange(len(region_df['Region']))
    width = 0.35
    ax1.bar(x - width/2, region_df['Pass'], width, label='Pass', color='#27ae60')
    ax1.bar(x + width/2, region_df['Fail'], width, label='Fail', color='#c0392b')
    ax1.set_xticks(x)
    ax1.set_xticklabels(region_df['Region'], rotation=45)
    ax1.legend()
    st.pyplot(fig1)

with graph_col2:
    st.caption("LOB Product Performance")
    # Process LOB Data for plotting
    lob_df['Product'] = lob_df['Result'].apply(lambda x: x.split(' (')[0])
    lob_df['Status'] = lob_df['Result'].apply(lambda x: x.split(' (')[1].replace(')', ''))
    # Sum across all region columns to get total per product
    lob_df['Total'] = lob_df[['Central', 'Northern', 'sarawak', 'Sabah']].sum(axis=1)
    pivot_lob = lob_df.pivot_table(index='Product', columns='Status', values='Total', aggfunc='sum')
    
    # Stacked Bar Chart
    fig2, ax2 = plt.subplots()
    ax2.bar(pivot_lob.index, pivot_lob['Pass'], label='Pass', color='#27ae60')
    ax2.bar(pivot_lob.index, pivot_lob['Fail'], bottom=pivot_lob['Pass'], label='Fail', color='#c0392b')
    ax2.legend()
    st.pyplot(fig2)

st.markdown("---")

# ROW 3: Data Table
st.subheader("Detailed Regional Data")
st.dataframe(region_df, use_container_width=True)
