from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from typing import List

# Define the base class
Base = declarative_base()

# Define the ArchaeologicalSite model
class ArchaeologicalSite(Base):
    __tablename__ = 'archaeological_sites'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    period = Column(String)
    specialization = Column(String)
    findings = relationship('Finding', back_populates='site')

# Define the Finding model
class Finding(Base):
    __tablename__ = 'findings'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('archaeological_sites.id'))
    date = Column(Date)
    condition = Column(String)
    type = Column(String)
    items = relationship('Item', back_populates='finding')
    site = relationship('ArchaeologicalSite', back_populates='findings')

# Define the Item model
class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    finding_id = Column(Integer, ForeignKey('findings.id'))
    name = Column(String)
    owner = Column(String)
    value = Column(Float)
    epoch = Column(String)
    finding = relationship('Finding', back_populates='items')
