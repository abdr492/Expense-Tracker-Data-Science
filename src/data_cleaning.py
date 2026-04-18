import pandas as pd

# -------------------------------
# Load dataset
# -------------------------------
input_path = "data/raw/expenses.csv"
df = pd.read_csv(input_path)

print("🔍 Raw Data Preview:")
print(df.head())

# -------------------------------
# Check missing values
# -------------------------------
print("\n❓ Missing Values:")
print(df.isnull().sum())

# -------------------------------
# Drop missing values (important columns)
# -------------------------------
df = df.dropna(subset=["Date", "Amount", "Category", "Type"])

# -------------------------------
# Convert data types
# -------------------------------
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# -------------------------------
# Remove duplicates
# -------------------------------
df = df.drop_duplicates()

# -------------------------------
# Standardize text columns
# -------------------------------
df["Category"] = df["Category"].astype(str).str.strip().str.title()
df["Type"] = df["Type"].astype(str).str.strip().str.title()
df["Payment_Method"] = df["Payment_Method"].astype(str).str.strip().str.title()

# -------------------------------
# Feature Engineering
# -------------------------------
df["Month"] = df["Date"].dt.month_name()
df["Day"] = df["Date"].dt.day
df["Weekday"] = df["Date"].dt.day_name()

# -------------------------------
# Final preview
# -------------------------------
print("\n✅ Cleaned Data Preview:")
print(df.head())

# -------------------------------
# Save cleaned dataset
# -------------------------------
output_path = "data/processed/cleaned_expenses.csv"
df.to_csv(output_path, index=False)

print(f"\n💾 Cleaned dataset saved at: {output_path}")