# db_config.py
from sqlalchemy import create_engine

# Define the database connection URL
DATABASE_URL = 'sqlite:///path/to/your/database.db'

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)
