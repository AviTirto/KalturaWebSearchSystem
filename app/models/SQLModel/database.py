from sqlmodel import SQLModel, create_engine, Session
import os

# Define the SQLite database URL
DATABASE_PATH = os.getenv("DATABASE_PATH", "./database.db")  # Default to './database.db' if env var not set
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"  # Full path to the database file

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Initialize the database and create all tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Function to get a session for database operations
def get_session() -> Session:
    return Session(engine)

# Run the initialization function
if __name__ == "__main__":
    init_db()
