import pandas as pd

# -------------------------------
# Load cleaned dataset
# -------------------------------
input_path = "data/processed/cleaned_expenses.csv"
df = pd.read_csv(input_path)

# -------------------------------
# Separate Income & Expense
# -------------------------------
expense_df = df[df["Type"] == "Expense"]
income_df = df[df["Type"] == "Income"]

# -------------------------------
# KPI Calculations
# -------------------------------
total_expense = expense_df["Amount"].sum()
total_income = income_df["Amount"].sum()
savings = total_income - total_expense

print("📊 KEY METRICS")
print(f"Total Income: ₹{total_income:,.2f}")
print(f"Total Expense: ₹{total_expense:,.2f}")
print(f"Savings: ₹{savings:,.2f}")

# -------------------------------
# Category-wise Spending
# -------------------------------
category_spending = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

print("\n📊 Category-wise Spending:")
print(category_spending)

# -------------------------------
# Monthly Expense Trend
# -------------------------------
monthly_expense = expense_df.groupby("Month")["Amount"].sum()

print("\n📈 Monthly Expense:")
print(monthly_expense)

# -------------------------------
# Top Spending Category
# -------------------------------
top_category = category_spending.idxmax()
top_amount = category_spending.max()

print(f"\n🔥 Highest Spending Category: {top_category} (₹{top_amount:,.2f})")

# -------------------------------
# Overspending Detection (Simple)
# -------------------------------
avg_expense = expense_df["Amount"].mean()

high_expense = expense_df[expense_df["Amount"] > avg_expense * 2]

print("\n⚠️ High Expense Transactions:")
print(high_expense[["Date", "Category", "Amount"]].head())

# -------------------------------
# Save results (optional)
# -------------------------------
category_spending.to_csv("outputs/category_spending.csv")
monthly_expense.to_csv("outputs/monthly_expense.csv")

print("\n💾 Analysis results saved in outputs/")