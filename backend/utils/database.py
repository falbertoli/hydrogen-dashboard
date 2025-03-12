# backend/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import current_app
from models.aircraft import Base as AircraftBase
from models.gse import Base as GSEBase
import logging

logger = logging.getLogger(__name__)

# Global session factories
aircraft_session_factory = None
gse_session_factory = None

def init_db(app):
    """Initialize database connections and create all tables."""
    global aircraft_session_factory, gse_session_factory
    
    logger.debug("Initializing database connections")
    
    # Create engines
    aircraft_engine = create_engine(
        app.config['AIRCRAFT_DATABASE_URI'],
        echo=True  # Enable SQL logging
    )
    gse_engine = create_engine(
        app.config['GSE_DATABASE_URI'],
        echo=True
    )

    # Create session factories
    aircraft_session_factory = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=aircraft_engine
        )
    )
    
    gse_session_factory = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=gse_engine
        )
    )

    # Create tables
    AircraftBase.metadata.create_all(aircraft_engine)
    GSEBase.metadata.create_all(gse_engine)

    logger.debug("Database initialization complete")
    return aircraft_engine, gse_engine

def get_aircraft_db_session():
    """Get a session for the aircraft database."""
    if aircraft_session_factory is None:
        raise RuntimeError("Database not initialized")
    
    session = aircraft_session_factory()
    try:
        yield session
    finally:
        session.close()

def get_gse_db_session():
    """Get a session for the GSE database."""
    if gse_session_factory is None:
        raise RuntimeError("Database not initialized")
    
    session = gse_session_factory()
    try:
        yield session
    finally:
        session.close()

def teardown_db():
    """Cleanup database connections."""
    if aircraft_session_factory:
        aircraft_session_factory.remove()
    if gse_session_factory:
        gse_session_factory.remove()