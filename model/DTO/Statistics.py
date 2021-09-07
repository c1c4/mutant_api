from pydantic import BaseModel

class Statistics(BaseModel):
    count_mutant_dna: int
    count_human_dna: int
    ratio: float

    class Config:
        orm_mode = True