from db.repositories.statistics_repository import StatisticsRepository
from api.dependencies.database import get_repository
from db.repositories.dna_repository import DNARepository
from fastapi import APIRouter, Depends
from service.dna_service import DnaService
from model.DTO.Dna import DNA

router = APIRouter(prefix='/mutant', tags=['Mutants'])

@router.post('/', name='mutants:check-store-dna')
async def post_dna(dna: DNA,
    dna_repo: DNARepository = Depends(get_repository(DNARepository)),
    stats_repo: StatisticsRepository = Depends(get_repository(StatisticsRepository))
) -> str:
    dna_service = DnaService()
    dna = dna_service.tracker_dna(dna.dna, dna_repo, stats_repo)
    return 'The dna is from a mutant' if dna.is_mutant else 'The dna is from a human'