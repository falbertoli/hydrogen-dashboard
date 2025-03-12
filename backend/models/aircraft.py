#  backend/models/aircraft.py and backend/models/gse.py
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base  # Updated import

Base = declarative_base()


class Aircraft(Base):
    """
    Represents an aircraft record in the database.
    """
    __tablename__ = 'aircraft_data'  # Define the table name

    id = Column(Integer, primary_key=True)
    departures_performed = Column(Integer)
    distance = Column(Float)
    air_time = Column(Float)
    unique_carrier = Column(String)
    unique_carrier_name = Column(String)
    origin_airport_id = Column(Integer)
    origin = Column(String)
    origin_city_name = Column(String)
    dest_airport_id = Column(Integer)
    dest = Column(String)
    dest_city_name = Column(String)
    aircraft_type = Column(Integer)
    month = Column(Integer)
    data_source = Column(String)
    fuel_consumption = Column(Float)

    def __repr__(self):
        return (f"<Aircraft(unique_carrier='{self.unique_carrier}', "
                f"origin='{self.origin}', dest='{self.dest}')>")