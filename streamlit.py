import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
uploaded_file = "https://github.com/vaidyamohit/Marketing-Dashboard/raw/main/Dataset%20Marketing.xlsx"
df = pd.read_excel(uploaded_file, engine="openpyxl")

# Set up Streamlit app
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

# Title
st.title("Marketing Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
category_column = st.sidebar.selectbox(
    "Select a Category Column:",
    [col for col in df.columns if df[col].dtype == "object"]
)
numerical_column = st.sidebar.selectbox(
    "Select a Numerical Column:",
    [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
)
data_filter = st.sidebar.text_input(
    "Apply Filter (e.g., Sales > 5000):",
    value=""
)
apply_filter = st.sidebar.button("Apply Filter")

# Apply filter
filtered_df = df.copy()
if apply_filter and data_filter:
    try:
        filtered_df = filtered_df.query(data_filter)
        st.sidebar.success("Filter applied successfully!")
    except Exception as e:
        st.sidebar.error(f"Invalid filter: {e}")

# Insights Section
st.subheader("Key Insights")
col1, col2, col3, col4 = st.columns(4)
try:
    total_value = filtered_df[numerical_column].sum()
    avg_value = filtered_df[numerical_column].mean()
    max_value = filtered_df[numerical_column].max()
    min_value = filtered_df[numerical_column].min()

    col1.metric(f"Total {numerical_column}", f"{total_value:,.2f}")
    col2.metric(f"Average {numerical_column}", f"{avg_value:,.2f}")
    col3.metric(f"Max {numerical_column}", f"{max_value:,.2f}")
    col4.metric(f"Min {numerical_column}", f"{min_value:,.2f}")
except Exception as e:
    st.error(f"Error calculating insights: {e}")

# Graphs Section
st.subheader("Visualizations")

# Bar Chart
st.write(f"Bar Chart: {numerical_column} by {category_column}")
fig, ax = plt.subplots(figsize=(10, 5))
filtered_df.groupby(category_column)[numerical_column].sum().plot(kind='bar', ax=ax)
ax.set_title(f"Bar Chart: {numerical_column} by {category_column}")
ax.set_xlabel(category_column)
ax.set_ylabel(numerical_column)
st.pyplot(fig)

# Pie Chart
st.write(f"Pie Chart: {numerical_column} Distribution by {category_column}")
fig, ax = plt.subplots(figsize=(8, 8))
filtered_df.groupby(category_column)[numerical_column].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
ax.set_ylabel('')
st.pyplot(fig)

# Data Table Section
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)

# Download Option
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
