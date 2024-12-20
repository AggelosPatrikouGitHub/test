import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = 'https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv'
df = pd.read_csv(url)
df.head()


df['Date'] = pd.to_datetime(df['Date'])
df = df[(df['Date'].dt.year >= 2016) & (df['Date'].dt.year <= 2019)]
df = df.dropna(subset=['ZIP Code', 'Item Description', 'Sale (Dollars)', 'Store Number'])
df['Sale (Dollars)'] = pd.to_numeric(df['Sale (Dollars)'], errors='coerce')
zip_item_sales = df.groupby(['ZIP Code', 'Item Description'])['Sale (Dollars)'].sum().reset_index()
popular_items = zip_item_sales.loc[zip_item_sales.groupby('ZIP Code')['Sale (Dollars)'].idxmax()]
popular_items.head()
store_sales = df.groupby('Store Number')['Sale (Dollars)'].sum()


total_sales = store_sales.sum()
store_sales_percentage = (store_sales / total_sales) * 100



store_sales_percentage = store_sales_percentage.reset_index(name='Sales Percentage')
store_sales_percentage.head()
plt.figure(figsize=(12, 6))
sns.barplot(data=popular_items, x='ZIP Code', y='Sale (Dollars)', hue='Item Description')
plt.title('Most Popular Items by ZIP Code (2016-2019)')
plt.ylabel('Sales (Dollars)')
plt.xlabel('ZIP Code')
plt.xticks(rotation=45)
plt.legend(title='Item Description')
plt.tight_layout()
plt.show()
store_sales_percentage.sort_values(by='Sales Percentage', ascending=False, inplace=True)
top_stores = store_sales_percentage.head(10)



plt.figure(figsize=(8, 8))
plt.pie(top_stores['Sales Percentage'], labels=top_stores['Store Number'], autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Stores by Sales Percentage (2016-2019)')
plt.show()