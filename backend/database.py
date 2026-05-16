from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Update this string with your actual MySQL username, password, and database name
# Format: mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = "mysql+mysqlconnector://root:ariba900@localhost:3306/expensetracker"

# 2. Create the engine bridge to connect Python to MySQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Checks if the connection is still alive before sending queries
    pool_recycle=3600    # Prevents "MySQL server has gone away" errors by recycling connections hourly
)

# 3. Create a session factory to generate unique transactional database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the base class that your models.py will inherit from to auto-generate tables
Base = declarative_base()

# 5. Dependency injection function to handle opening and closing database sessions safely
def get_db():
    """
    Yields a database session instance to a FastAPI endpoint route,
    and guarantees the connection closes cleanly after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()