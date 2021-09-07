from db.repositories.base import BaseRepository
from model.Statistics import Statistics
from model.DTO.Statistics import Statistics as StatisticsDTO

class StatisticsRepository(BaseRepository):

    def get_statistics(self):
        return self.db.query(Statistics).first()

    def create_statistics(self, status: StatisticsDTO):
        db_statistics = Statistics(**status.dict())
        self.db.add(db_statistics)
        self.db.commit()
        self.db.refresh(db_statistics)
        return db_statistics

    def update_statistics(self, id_status, status_update: StatisticsDTO):
        db_statistics_updated = self.db.query(Statistics).filter(Statistics.id == id_status).one_or_none()

        if not db_statistics_updated:
            return None

        for var, value in vars(status_update).items():
            setattr(db_statistics_updated, var, value) if value else None

        self.db.commit()
        self.db.refresh(db_statistics_updated)
        return db_statistics_updated