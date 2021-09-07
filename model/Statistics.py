from db import Base
from sqlalchemy import Column, Integer, Float

class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    count_mutant_dna = Column(Integer)
    count_human_dna = Column(Integer)
    ratio = Column(Float)