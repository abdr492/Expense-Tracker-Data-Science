import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

st.markdown("""
<style>
.kpi-box {
    transition: transform 0.3s ease;
}
.kpi-box:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2937);
    padding: 15px;
}

/* Sidebar titles */
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #00C897;
}

/* Input fields */
[data-testid="stSidebar"] .stSelectbox, 
[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stDateInput {
    background-color: #1f2937;
    border-radius: 8px;
}

/* Button styling */
[data-testid="stSidebar"] button {
    background: linear-gradient(90deg, #4F46E5, #3B82F6);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("data/processed/cleaned_expenses.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("➕ Add New Transaction")

with st.sidebar.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment", "Health"])
    amount = st.number_input("Amount", min_value=0.0)
    txn_type = st.selectbox("Type", ["Expense", "Income"])
    payment = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        new_data = pd.DataFrame({
            "Date": [date],
            "Category": [category],
            "Amount": [amount],
            "Type": [txn_type],
            "Payment_Method": [payment]
        })

        # Append to CSV
        new_data.to_csv("data/processed/cleaned_expenses.csv", mode='a', header=False, index=False)

        st.success("✅ Transaction Added Successfully!")
# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("🔍 Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

type_filter = st.sidebar.selectbox(
    "Transaction Type",
    ["All", "Expense", "Income"]
)

# Apply filters
filtered_df = df[df["Category"].isin(category_filter)]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]

# -------------------------------
# Title
# -------------------------------
st.markdown("""
<h1 style='text-align: center; color: #00C897;'>
💰 Expense Tracker Dashboard
</h1>
""", unsafe_allow_html=True)

# -------------------------------
# KPI Metrics
# -------------------------------
expense_df = filtered_df[filtered_df["Type"] == "Expense"]
income_df = filtered_df[filtered_df["Type"] == "Income"]

total_expense = expense_df["Amount"].sum()
total_income = income_df["Amount"].sum()
savings = total_income - total_expense
# -------------------------------
# Prepare Data for Charts
# -------------------------------
category_spending = expense_df.groupby("Category")["Amount"].sum()

st.markdown("""
<style>
.kpi-box {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}
.kpi-title {
    font-size: 16px;
    color: #9CA3AF;
}
.kpi-value {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# 💸 Expense Box (Red Theme)
col1.markdown(f"""
<div class="kpi-box" style="
background: linear-gradient(135deg, #7F1D1D, #DC2626);
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0px 4px 12px rgba(0,0,0,0.4);
">
<span style="color:#FCA5A5;font-size:16px;">💸 Total Expense</span><br>
<span style="color:#FFE4E6;font-size:28px;font-weight:bold;">
₹{total_expense:,.0f}
</span>
</div>
""", unsafe_allow_html=True)


# 💰 Income Box (Green Theme)
col2.markdown(f"""
<div class="kpi-box" style="
background: linear-gradient(135deg, #064E3B, #10B981);
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0px 4px 12px rgba(0,0,0,0.4);
">
<span style="color:#6EE7B7;font-size:16px;">💰 Total Income</span><br>
<span style="color:#ECFDF5;font-size:28px;font-weight:bold;">
₹{total_income:,.0f}
</span>
</div>
""", unsafe_allow_html=True)


# 📊 Savings Box (Gold Theme)
col3.markdown(f"""
<div class="kpi-box" style="
background: linear-gradient(135deg, #78350F, #F59E0B);
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0px 4px 12px rgba(0,0,0,0.4);
">
<span style="color:#FCD34D;font-size:16px;">📊 Savings</span><br>
<span style="color:#FFF7ED;font-size:28px;font-weight:bold;">
₹{savings:,.0f}
</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
# -------------------------------
# Category-wise Bar Chart
# -------------------------------
import plotly.express as px

st.markdown("""
<div style="
background: linear-gradient(90deg, #4F46E5, #3B82F6);
padding:12px;
border-radius:12px;
margin-bottom:15px;
text-align:center;">
<h3 style="color:white;">📊 Expense by Category</h3>
</div>
""", unsafe_allow_html=True)

if not category_spending.empty:
    fig = px.bar(
    x=category_spending.index,
    y=category_spending.values,
    color=category_spending.index,
    color_discrete_sequence=px.colors.qualitative.Bold,
    labels={'x': 'Category', 'y': 'Amount'},
    title="Category-wise Spending"
)
st.plotly_chart(fig, use_container_width=True, key="category_chart")

st.markdown("<br>", unsafe_allow_html=True)
# -------------------------------
# Monthly Trend
# -------------------------------
st.markdown("""
<div style="
background: linear-gradient(90deg, #059669, #10B981);
padding:12px;
border-radius:12px;
margin-bottom:15px;
text-align:center;">
<h3 style="color:white;">📈 Monthly Trend</h3>
</div>
""", unsafe_allow_html=True)

monthly = filtered_df.groupby(filtered_df["Date"].dt.month)["Amount"].sum()

fig = px.line(
    x=monthly.index,
    y=monthly.values,
    markers=True
)

fig.update_traces(line=dict(color="#00C897", width=3))

st.plotly_chart(fig, use_container_width=True, key="monthly_chart")

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

# -------------------------------
# Pie Chart (Matplotlib)
# -------------------------------
with col_left:
    st.markdown("""
    <div style="
    background: linear-gradient(90deg, #F59E0B, #FBBF24);
    padding:12px;
    border-radius:12px;
    margin-bottom:15px;
    text-align:center;">
    <h3 style="color:white;">🥧 Expense Distribution</h3>
    </div>
    """, unsafe_allow_html=True)

    if not category_spending.empty:
        fig = px.pie(
            values=category_spending.values,
            names=category_spending.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(hole=0.5)
        st.plotly_chart(fig, use_container_width=True, key="pie_chart")
    else:
       st.write("No data available")

st.markdown("<br>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="
    background: linear-gradient(90deg, #EC4899, #F472B6);
    padding:12px;
    border-radius:12px;
    margin-bottom:15px;
    text-align:center;">
    <h3 style="color:white;">🧠 Smart Insights</h3>
    </div>
    """, unsafe_allow_html=True)

    if not category_spending.empty:
        top_category = category_spending.idxmax()
        avg_expense = expense_df["Amount"].mean()

        st.markdown(f"""
        <div style="
        background: linear-gradient(90deg, #111827, #1f2937);
        padding:20px;
        border-radius:12px;
        text-align:center;
        ">

        <h3 style="color:#60A5FA;">
        📊 Highest spending category: {top_category}
        </h3>

        <h3 style="color:#34D399;">
        {"✅ Your savings are positive. Good job!" if savings >= 0 else "⚠️ You are spending more than your income!"}
        </h3>

        <h3 style="color:#FBBF24;">
        💰 Average expense per transaction: ₹{avg_expense:,.2f}
        </h3>

        </div>
        """, unsafe_allow_html=True)

# -------------------------------
# Raw Data View
# -------------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
