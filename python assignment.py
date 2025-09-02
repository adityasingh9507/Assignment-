import pandas as pd

# 1. Load the data (replace the file name with your actual file)
df = pd.read_csv("order_id,customer_id,partner_id,ship_mod.csv", parse_dates=['order_purchase_date'])

# 2. Remove invalid orders (canceled or unavailable)
df = df[~df['order_status'].isin(['canceled', 'unavailable'])]

# 3. Extract the month from the order date
df['month'] = df['order_purchase_date'].dt.to_period('M')

# 4. Find each customer's first purchase
first_purchase = df.groupby('customer_id')['order_purchase_date'].transform('min')

# 5. Mark orders that are repeats (date > first purchase date)
df['is_repeat'] = df['order_purchase_date'] > first_purchase

# 6. Group by month and count:
#    - total unique customers
#    - repeat unique customers
summary = df.groupby('month').agg(
    total_customers=('customer_id', 'nunique'),
    repeat_customers=('customer_id', lambda x: df.loc[x.index, 'is_repeat'].sum())
).reset_index()

# 7. Calculate repeat rate (%)
summary['repeat_rate_percent'] = (summary['repeat_customers'] / summary['total_customers'] * 100).round(2)

# 8. Format month to look nice (e.g., "Jan-2017")
summary['month_year'] = summary['month'].dt.strftime('%b-%Y')

# 9. Keep only the important columns
summary = summary[['month_year', 'total_customers', 'repeat_customers', 'repeat_rate_percent']]

# Show result
print(summary)

# 10. Save to CSV file
summary.to_csv("repeat_rate_summary.csv", index=False)