import pandas as pd
import io

# 1. READ CSV (Concepts Tested: Reading CSV)
data = """PRODUCT,QUANTITY,PRICE
A,2,100
B,1,200
A,3,100
C,5,50"""

df = pd.read_csv(io.StringIO(data))

# 2. BONUS: ADD NEW COLUMN & CALCULATE REVENUE (Chained Operations)
# .assign() creates the new 'TOTAL' column (Bonus Task)
results = df.assign(TOTAL=df['QUANTITY'] * df['PRICE'])

# 3. TASK: SUMMARIZE SALES PER PRODUCT (Basic Aggregation)
# Group by PRODUCT and sum the TOTAL (Revenue) column
product_summary = results.groupby('PRODUCT')['TOTAL'].sum().reset_index()
product_summary.rename(columns={'TOTAL': 'REVENUE'}, inplace=True)

# 4. BONUS: SORT BY REVENUE (Focus: Column-based Operations)
product_summary = product_summary.sort_values(by='REVENUE', ascending=False)

# 5. FIND: TOTAL REVENUE & TOP-SELLING PRODUCT
total_revenue = product_summary['REVENUE'].sum()
top_selling = product_summary.iloc[0]['PRODUCT']

# Display final outputs
print("--- Sales Dataset ---")
print(results)
print("\n--- Summary Sorted by Revenue ---")
print(product_summary)
print(f"\nOverall Total Revenue: {total_revenue}")
print(f"Top-Selling Product: {top_selling}")