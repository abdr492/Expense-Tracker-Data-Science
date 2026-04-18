import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load cleaned dataset
# -------------------------------
input_path = "data/processed/cleaned_expenses.csv"
df = pd.read_csv(input_path)

# Filter only expenses
expense_df = df[df["Type"] == "Expense"]

# Set style
sns.set(style="whitegrid")

# -------------------------------
# 1. Category-wise Bar Chart
# -------------------------------
category_spending = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=category_spending.index, y=category_spending.values)
plt.title("Total Expense by Category")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/category_spending.png")
plt.show()

# -------------------------------
# 2. Expense Distribution (Pie Chart)
# -------------------------------
plt.figure(figsize=(7, 7))
plt.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%', startangle=140)
plt.title("Expense Distribution by Category")
plt.axis('equal')

# Save chart
plt.savefig("outputs/charts/pie_chart.png")
plt.show()

# -------------------------------
# 3. Monthly Expense Trend
# -------------------------------
df["Date"] = pd.to_datetime(df["Date"])
expense_df["Month_Num"] = pd.to_datetime(expense_df["Date"]).dt.month

monthly_expense = expense_df.groupby("Month_Num")["Amount"].sum()

plt.figure(figsize=(10, 5))
monthly_expense.plot(marker='o')
plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Amount (₹)")
plt.grid(True)
plt.tight_layout()

# Save chart
plt.savefig("outputs/charts/monthly_trend.png")
plt.show()

print("✅ Charts saved in outputs/charts/")