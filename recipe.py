from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:RRmm2108!@localhost/collect_data"

# Create an SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define ORM class representing your database table
class Recipe(Base):
    __tablename__ = 'ForCoock'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    ingredients = Column(String)
    directions = Column(String)