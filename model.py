from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey)
from sqlalchemy.orm import declarative_base ## new way of importing declarative base
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brands(Base):
    __tablename__ = 'brand'
    
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column('Brand_name', String)
    pro = relationship('Products', back_populates='brans', cascade= 'all, delete, delete-orphan')

    
    def __repr__(self):
        return f'\n{self.brand_id} | {self.brand_name}'

class Products(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product_name', String)
    product_quantity = Column('Product_quantity', Integer)
    product_price = Column('Product_price', Integer)
    date_updated = Column('Date_updated', Date)
    brand_id = Column(Integer,ForeignKey('brand.brand_id'))
    brans = relationship('Brands', back_populates='pro')
    
    def __repr__(self):
        return f'\n{self.product_id} | {self.product_name} | {self.product_quantity} | {self.product_price} | {self.date_updated} | Brand ID: {self.brand_id}'
     