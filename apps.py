import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("Customer Churn Dashboard")
st.write("Interactive dashboard for telecom customer churn analysis.")

file_path = Path("/Users/nida/GitHub/data_dashboard/data/churn_data_80.csv")

if not file_path.exists():
    st.error(f"File not found: {file_path}")
    st.stop()

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.sidebar.header("Filters")

if "state" in df.columns:
    selected_state = st.sidebar.selectbox(
        "Select State",
        ["All"] + sorted(df["state"].astype(str).unique().tolist())
    )
    if selected_state != "All":
        df = df[df["state"].astype(str) == selected_state]

churn_series = df["churn"].astype(str).str.strip().str.lower()
churn_flag = churn_series.isin(["true", "yes", "1"])

total_customers = len(df)
churn_rate = churn_flag.mean() * 100

col1, col2 = st.columns(2)
col1.metric("Total Customers", total_customers)
col2.metric("Churn Rate (%)", f"{churn_rate:.2f}")

st.subheader("Churn Distribution")
fig, ax = plt.subplots()
df["churn"].astype(str).value_counts().plot(kind="bar", ax=ax)
ax.set_xlabel("Churn")
ax.set_ylabel("Count")
ax.set_title("Churn Distribution")
st.pyplot(fig)

if "customer_service_calls" in df.columns and "total_day_minutes" in df.columns:
    st.subheader("Customer Service Calls vs Total Day Minutes")
    fig, ax = plt.subplots()
    ax.scatter(df["customer_service_calls"], df["total_day_minutes"])
    ax.set_xlabel("Customer Service Calls")
    ax.set_ylabel("Total Day Minutes")
    ax.set_title("Customer Service Calls vs Usage")
    st.pyplot(fig)

st.subheader("Quick Insights")
st.write("- This dashboard helps explore churn patterns interactively.")
st.write("- You can filter customers by state.")
st.write("- Service calls and usage patterns may indicate churn behaviour.")
