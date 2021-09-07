from db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

class Dna(Base):
    __tablename__ = 'dnas'

    id = Column(Integer, primary_key=True)
    dna = Column(ARRAY(String), index=True)
    is_mutant = Column(Boolean)
