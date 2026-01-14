from sqlalchemy import Column, Integer, String, Float

class Stock:
    reference_month = Column(String)
    category = Column(String)
    product_name = Column(String)
    units_sold = Column(Integer)
    units_in_stock = Column(Integer)
    unit_price = Column(Float)