from db.repositories.statistics_repository import StatisticsRepository
from api.dependencies.database import get_repository
from fastapi import APIRouter, Depends
from service import statistics_service
from model.DTO.Statistics import Statistics

router = APIRouter(prefix='/stats', tags=['Statistics'])

@router.get("/stats", response_model=Statistics, name='statistics:recover-statistics')
def get_stats(stats_repo: StatisticsRepository = Depends(get_repository(StatisticsRepository))) -> Statistics:
    stats = statistics_service.get_statistics(stats_repo)
    return stats if stats else Statistics(count_mutant_dna=0, count_human_dna=0, ratio=0)
