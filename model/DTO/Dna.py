from typing import List
from pydantic import BaseModel

class DNA(BaseModel):
    dna: List[str]

    class Config:
        orm_mode = True

class DNACreate(DNA):
    is_mutant: bool
