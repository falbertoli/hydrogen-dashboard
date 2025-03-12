# backend/models/gse.py
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GroundSupportEquipment(Base):
    """
    Represents a ground support equipment (GSE) record in the database.
    """
    __tablename__ = 'gse_data'  # Match the table name

    id = Column(Integer, primary_key=True)  # Add an ID column as the primary key.
    ground_support_equipment = Column(String, nullable=False)  #More descriptive name, required
    fuel_used = Column(String)
    fuel_consumption_online = Column(String)  # Keep as String if it's text like "15 mpg"
    average_speed_mi_hr = Column(Integer)  # Or Float, depending on your data.
    usable_fuel_consumption_ft3_min = Column(Float)
    operating_time_departure = Column(Integer)
    operating_time_arrival = Column(Integer)
    notes = Column(String)
    link = Column(String)

    def __repr__(self):
        return (f"<GroundSupportEquipment(equipment='{self.ground_support_equipment}', "
                f"fuel='{self.fuel_used}')>")