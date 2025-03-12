# backend/repositories/aircraft_repository.py
from sqlalchemy import and_
from models.aircraft import Aircraft
import logging

logger = logging.getLogger(__name__)

class AircraftRepository:
    def __init__(self, session):
        self.session = session

    def get_aircraft_data(self, end_year, slider_perc, limit=None):
        """
        Get aircraft data filtered for July and domestic flights.
        """
        try:
            query = self.session.query(Aircraft).filter(
                and_(
                    Aircraft.month == 7,  # July data
                    Aircraft.data_source == "DU"  # Domestic flights
                )
            )

            # Log the SQL query
            logger.debug(f"SQL Query: {query}")

            if limit:
                query = query.limit(limit)

            results = query.all()
            logger.debug(f"Found {len(results)} aircraft records")
            
            return results

        except Exception as e:
            logger.error(f"Error querying aircraft data: {str(e)}")
            raise