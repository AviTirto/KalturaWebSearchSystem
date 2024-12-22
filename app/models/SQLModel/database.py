from sqlmodel import SQLModel, create_engine, Session

# Define the SQLite database URL
DATABASE_URL = "sqlite:///database.db"  # This will create a file named 'database.db'

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True to log SQL queries

# Initialize the database and create all tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Function to get a session for database operations
def get_session() -> Session:
    return Session(engine)

# Run the initialization function
if __name__ == "__main__":
    init_db()
