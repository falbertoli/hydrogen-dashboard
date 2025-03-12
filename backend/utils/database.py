# backend/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_config
from models.aircraft import Base as AircraftBase  # Import Base for aircraft
from models.gse import Base as GSEBase  # Import Base for GSE

config = get_config()  # Get the active configuration

# Create engines for both databases
aircraft_engine = create_engine(config.DATABASE_URI)
gse_engine = create_engine(config.GSE_DATABASE_URI)

# Create session factories for both databases
AircraftSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=aircraft_engine)
GSESessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=gse_engine)


def init_db(app):
    """Create all tables in both databases."""
    AircraftBase.metadata.create_all(bind=aircraft_engine)  # Create Aircraft tables
    GSEBase.metadata.create_all(bind=gse_engine)  # Create GSE tables


def get_aircraft_db_session():
    """Provide a session for the aircraft database."""
    db = AircraftSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_gse_db_session():
    """Provide a session for the GSE database."""
    db = GSESessionLocal()
    try:
        yield db
    finally:
        db.close()