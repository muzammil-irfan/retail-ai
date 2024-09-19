from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class StoreSales(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(index=True)
    dept_id: int = Field(index=True)
    sales_date: date = Field(index=True)
    weekly_sales: float
    is_holiday: bool
