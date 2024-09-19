import pandas as pd
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.models import StoreSales  # Replace this with your actual model import
from app.database import engine

# Load CSV file into pandas DataFrame
df = pd.read_csv('sales_data-set.csv')

# Fix date format in case it's not in standard format
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Create the table in the database
SQLModel.metadata.create_all(engine)

# Function to load data into the database
def load_data():
    with Session(engine) as session:
        for _, row in df.iterrows():
            try:
                # Create StoreSales object for each row
                sales_entry = StoreSales(
                    store_id=row['Store'],
                    dept_id=row['Dept'],
                    sales_date=row['Date'],
                    weekly_sales=row['Weekly_Sales'],
                    is_holiday=row['IsHoliday'] == 'TRUE'  # Convert 'TRUE'/'FALSE' to boolean
                )
                session.add(sales_entry)
            except IntegrityError:
                session.rollback()
            else:
                session.commit()

# Load data into the database
load_data()
