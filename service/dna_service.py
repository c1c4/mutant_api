from db.repositories.statistics_repository import StatisticsRepository
from db.repositories.dna_repository import DNARepository
from model import Dna
from model.DTO.Dna import DNACreate
from service import statistics_service
from fastapi import HTTPException


class DnaService:
    def horizontal(self, char, row_dna, nitrogenous_base, position=0) -> int:
        if position == len(row_dna)-1:
            return 0
        
        position += 1
        char_to_compare = row_dna[position]

        if char == char_to_compare:
            nitrogenous_base[char] = nitrogenous_base[char] + 1
        elif nitrogenous_base[char] == 4:
            return 1
        else:
            nitrogenous_base[char] = 1
        
        return self.horizontal(char_to_compare, row_dna, nitrogenous_base, position)

    def vertical(self, char, dna, base_position, nitrogenous_base, position=0) -> int:
        if position == len(dna)-1:
            return 0
        
        position += 1
        char_to_compare = dna[position][base_position]

        if char == char_to_compare:
            nitrogenous_base[char] = nitrogenous_base[char] + 1
        elif nitrogenous_base[char] == 4:
            return 1
        else:
            nitrogenous_base[char] = 1
        
        return self.vertical(char_to_compare, dna, base_position, nitrogenous_base, position)

    def obliquely(self, char, dna, nitrogenous_base, start_position=0, position=0, down=True):
        if down and (position == len(dna) -1 or start_position == len(dna[0]) -1):
            return 0
        elif not down and (position == len(dna) -1 or start_position == 0):
            return 0

        position += 1
        if down:
            start_position += 1
        else:
            start_position -= 1
        
        char_to_compare = dna[start_position][position]

        if char == char_to_compare:
            nitrogenous_base[char] = nitrogenous_base[char] + 1
        elif nitrogenous_base[char] == 4:
            return 1
        else:
            nitrogenous_base[char] = 1
        
        return self.obliquely(char_to_compare, dna, nitrogenous_base, start_position, position, down)

    def tracker_dna(self, dna: list, dna_repo: DNARepository, stats_repo: StatisticsRepository) -> Dna.Dna:
        seq = 0

        if len(dna) == 0:
            raise HTTPException(403, 'Empty DNA')

        db_dna = dna_repo.get_dna_by_dna(dna)

        if db_dna:
            return db_dna

        # check if has only ATCG
        valid_sequence_dna = True
        for row_dna in dna:
            diff = list(set(row_dna) - set(['A', 'T', 'C', 'G']))
            if len(diff) > 0:
                valid_sequence_dna = False
                break
        
        if not valid_sequence_dna:
            raise HTTPException(403, 'DNA must contain only A, T, C, G')

        first_char_position = dna[0][0]
        seq = seq + self.horizontal(first_char_position, dna[0], {'A': 1, 'T': 1, 'C': 1, 'G': 1})
        seq = seq + self.vertical(first_char_position, dna, 0, {'A': 1, 'T': 1, 'C': 1, 'G': 1})
        seq = seq + self.obliquely(first_char_position, dna, {'A': 1, 'T': 1, 'C': 1, 'G': 1})
        if seq < 2:
            # check horizontal
            for idx in range(1, len(dna)):
                first_char_position = dna[idx][0]
                seq = seq + self.horizontal(first_char_position, dna[idx], {'A': 1, 'T': 1, 'C': 1, 'G': 1})

            if seq < 2:
                # check vertical
                for idx in range(1, len(dna[0])):
                    char = dna[0][idx]
                    seq = seq + self.vertical(char, dna, idx, {'A': 1, 'T': 1, 'C': 1, 'G': 1})

                    # check first line obliquely \
                    if seq < 2:
                        seq = seq + self.obliquely(char, dna, {'A': 1, 'T': 1, 'C': 1, 'G': 1}, start_position=0, position=idx)

            
            if seq < 2:
                # check obliquely \
                for idx_dna in range(1, len(dna)):
                    row_dna = dna[idx_dna]
                    for idx_row_dna in range(len(row_dna)):
                        seq = seq + self.obliquely(row_dna[idx_row_dna], dna, {'A': 1, 'T': 1, 'C': 1, 'G': 1}, 
                            start_position=idx_dna, position=idx_row_dna)

            if seq < 2:
                # check obliquely /
                for idx_dna in range(len(dna)-1, -1, -1):
                    for idx_row_dna in range(len(row_dna)):
                        seq = seq + self.obliquely(row_dna[idx_row_dna], dna, {'A': 1, 'T': 1, 'C': 1, 'G': 1}, 
                            start_position=idx_dna, position=idx_row_dna, down=False)

        if seq > 1:
            dna_create = DNACreate(dna=dna, is_mutant=True)

            dna_stored = dna_repo.create_dna(dna_create)

            statistics_service.create_or_update_statistics(stats_repo, True)

        else:
            dna_create = DNACreate(dna=dna, is_mutant=False)

            dna_stored = dna_repo.create_dna(dna_create)

            statistics_service.create_or_update_statistics(stats_repo, False)

        return dna_stored