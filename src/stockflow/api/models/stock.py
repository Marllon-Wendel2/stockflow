from sqlalchemy import Column, Integer, String, Numeric
from stockflow.config.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)

    reference_month = Column(String, index=True)
    category = Column(String)
    product_name = Column(String)

    units_sold = Column(Integer)
    units_in_stock = Column(Integer)
    unit_price = Column(Numeric(10, 2))
