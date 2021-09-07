
from db.repositories.base import BaseRepository
from model.Dna import Dna
from model.DTO.Dna import DNACreate

class DNARepository(BaseRepository):

    def get_dna_by_dna(self, dna: list):
        return self.db.query(Dna).filter(Dna.dna == dna).first()

    def create_dna(self, dna: DNACreate):
        db_dna = Dna(dna=dna.dna, is_mutant= dna.is_mutant)
        self.db.add(db_dna)
        self.db.commit()
        self.db.refresh(db_dna)
        return db_dna