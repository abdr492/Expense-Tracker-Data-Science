import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -------------------------------
# Configuration
# -------------------------------
num_records = 1000

categories = ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment", "Health"]
payment_methods = ["Cash", "Card", "UPI"]
transaction_types = ["Expense", "Income"]

# -------------------------------
# Generate random dates
# -------------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

date_range = (end_date - start_date).days

def random_date():
    return start_date + timedelta(days=random.randint(0, date_range))

# -------------------------------
# Generate dataset
# -------------------------------
data = []

for _ in range(num_records):
    txn_type = random.choices(transaction_types, weights=[0.8, 0.2])[0]

    if txn_type == "Expense":
        category = random.choice(categories)
        amount = round(random.uniform(50, 5000), 2)
    else:
        category = "Salary"
        amount = round(random.uniform(20000, 80000), 2)

    data.append({
        "Date": random_date(),
        "Category": category,
        "Amount": amount,
        "Type": txn_type,
        "Payment_Method": random.choice(payment_methods)
    })

# -------------------------------
# Create DataFrame
# -------------------------------
df = pd.DataFrame(data)

# Sort by date
df = df.sort_values(by="Date")

# -------------------------------
# Save to CSV
# -------------------------------
output_path = "data/raw/expenses.csv"
df.to_csv(output_path, index=False)

print(f"✅ Synthetic dataset created at: {output_path}")
print(df.head())