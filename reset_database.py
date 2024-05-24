# reset_database.py
from models.base_model import Base
from db_config import engine  # Import the engine variable from db_config.py

# Drop existing tables
Base.metadata.drop_all(engine)

# Recreate tables with updated schema
Base.metadata.create_all(engine)
