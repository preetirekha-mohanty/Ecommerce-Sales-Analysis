
import pandas as pd
import numpy as np

# 1. Load the dataset
df = pd.read_excel(
    r'D:\ECOMMERCE SALES ANALYSIS\Ecommerce_Unclean_Project.xlsx'
)

# 2. Display the first five rows
print(df.head(5))

# 3. Display dataset information
print(df.info())

# 4. Display summary statistics
print(df.describe())

# 5. Dataset shape
print(df.shape)

# 6. Check missing values
print(df.isnull().sum())

# 7. Check duplicate values
print(df.duplicated().sum())

# 8. Remove duplicate records
df.drop_duplicates(inplace=True)

# 9. Replace invalid values
df.replace(['N/A', 'NULL', ''], np.nan, inplace=True)

# 10. Remove extra spaces
# Preserve numeric values while removing spaces from text
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# 11. Standardize text format
df['Customer_Name'] = df['Customer_Name'].str.title()
df['City'] = df['City'].str.title()
df['State'] = df['State'].str.title()

# 12. Validate email addresses
df = df[
    df['Email'].str.contains(
        r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
        na=False
    )
].copy()

# 13. Convert date columns
df['Order_Date'] = pd.to_datetime(
    df['Order_Date'], errors='coerce'
)

df['Delivery_Date'] = pd.to_datetime(
    df['Delivery_Date'], errors='coerce'
)

# 14. Convert numeric columns
cols = ['Qty', 'Unit_Price', 'Discount']

for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# 15. Remove invalid quantity
df = df[df['Qty'] > 0].copy()

print("\nDataset after removing invalid quantities:")
print(df.head())

# 16. Fill missing values

# Discount
df['Discount'] = df['Discount'].fillna(0)

# Phone
df['Phone'] = (
    df['Phone'].astype('string').fillna('Unknown')
)

# Delivery Date
df['Delivery_Date'] = df['Delivery_Date'].fillna(
    df['Order_Date']
)

# Verify Discount values
print("\nDiscount Values:")
print(df['Discount'].value_counts().sort_index())

# 17. Feature Engineering

# Total Sales
df['Sales'] = df['Qty'] * df['Unit_Price']

print("\nDataset with Sales:")
print(df.head())

# Net Amount
df['Net_Amount'] = (
    df['Sales'] - (df['Sales'] * df['Discount'] / 100)
)

# Profit (Assuming 20% profit margin)
df['Profit'] = df['Net_Amount'] * 0.20

# Order Month
df['Month'] = df['Order_Date'].dt.month_name()

# Year
df['Year'] = df['Order_Date'].dt.year

# Weekday
df['Weekday'] = df['Order_Date'].dt.day_name()

# 18. Display final dataset information
print("\nFinal Dataset Information:")
print(df.info())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# 19. Export clean data
df.to_csv(
    r'D:\ECOMMERCE SALES ANALYSIS\Clean_Ecommerce.csv',
    index=False
)

print("\nData cleaning completed successfully!")

# 20. MySQL Connection
from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "Your Password"
host = "localhost"
port = "3306"
database = "ecommerce"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "sales"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM sales LIMIT 5;", engine)

print("\nProject Completed Successfully!")
