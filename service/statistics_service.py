from db.repositories.statistics_repository import StatisticsRepository
from model.DTO.Statistics import Statistics as StatisticsDTO
from model.Statistics import Statistics

def get_statistics(stats_repo: StatisticsRepository) -> Statistics:
    return stats_repo.get_statistics()

def create_statistics(stats_repo: StatisticsRepository, statistics: StatisticsDTO) -> Statistics:
    return stats_repo.create_statistics(statistics)

def update_statistics(stats_repo: StatisticsRepository, id_statistics: int, statistics: StatisticsDTO) -> Statistics:
    return stats_repo.update_statistics(id_statistics, statistics)

def create_or_update_statistics(stats_repo: StatisticsRepository, is_mutant: bool):
    count_mutant = 0
    count_human = 0
    ratio = 1.0

    statistics = get_statistics(stats_repo)

    # calculate the ratio and increase the count for the mutant or human
    if is_mutant:
        if statistics:
            count_mutant = statistics.count_mutant_dna + 1
            count_human = statistics.count_human_dna
            ratio = count_mutant / count_human
        else:
            count_mutant = 1
            count_human = 0
            ratio = 1.0
    else:
        if statistics:
            count_mutant = statistics.count_mutant_dna
            count_human = statistics.count_human_dna + 1
            ratio = count_mutant / count_human
        else:
            count_mutant = 0
            count_human = 1
            ratio = 1.0

    if statistics:
        statistics_update = StatisticsDTO(
            count_mutant_dna=count_mutant, 
            count_human_dna=count_human,
            ratio=ratio
        )
        update_statistics(stats_repo, statistics.id, statistics_update)
    else:
        statistics_create = StatisticsDTO(
            count_mutant_dna=count_mutant, 
            count_human_dna=count_human,
            ratio=ratio
        )
        create_statistics(stats_repo, statistics_create)