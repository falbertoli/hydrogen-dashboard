# backend/repositories/gse_repository.py
from sqlalchemy.orm import Session
from models.gse import GroundSupportEquipment

class GSERepository:
    def __init__(self, db: Session):
        self.db = db

    def get_gse_by_equipment_type(self, equipment_types: list):
        """Retrieve GSE data by equipment type."""
        return self.db.query(GroundSupportEquipment).filter(GroundSupportEquipment.ground_support_equipment.in_(equipment_types)).all()

    def create_gse(self, gse_data: dict):
        """Create a new GSE record."""
        db_gse = GroundSupportEquipment(**gse_data)
        self.db.add(db_gse)
        self.db.commit()
        self.db.refresh(db_gse)
        return db_gse