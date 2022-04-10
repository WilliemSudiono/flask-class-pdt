from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from petshop.db import Base


class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category')
