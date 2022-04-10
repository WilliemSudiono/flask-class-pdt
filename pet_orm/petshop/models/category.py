from sqlalchemy import Column, String, Integer
from petshop.db import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name=''):
        self.name = name
