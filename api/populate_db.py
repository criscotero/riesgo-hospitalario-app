import psycopg2
from app import settings as config
from app.db import Base
from app.model.models import Patient
from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.DATABASE_NAME

# Create the initial connection URL to PostgreSQL (without specifying the database)
initial_connection_url = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/postgres"
)

print(initial_connection_url)

conn = None

# Connect to PostgreSQL to create the database if it doesn't exist
try:
    conn = psycopg2.connect(initial_connection_url)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the database
    cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
    print(f"Database '{DATABASE_NAME}' created successfully")

except DuplicateDatabase as e:
    if "already exists" in str(e):
        print(f"Database '{DATABASE_NAME}' already exists.")
    else:
        print(f"Error creating database: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()

# Database connection URL to the newly created database
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
print(SQLALCHEMY_DATABASE_URL)

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Drop all tables if they exist
Base.metadata.drop_all(engine)
print("Tables dropped")

# Create all tables
Base.metadata.create_all(engine)
print("Tables created")


# Populate database with a default patient
print("Populating database with default patient")
Session = sessionmaker(bind=engine)
session = Session()


patient = Patient(
    #redis_job_id="job_1234567890",
    first_name="John",
    last_name="Doe",
    identification="ABC123456",
    age=45,
    r5height=1.75,
    r5weight=70.5,
    r5adla=2,
    r5adltot6=3,
    r5iadlfour=1,
    r5nagi8=4,
    r5grossa=2,
    r5mobilsev=5,
    r5uppermob=1,
    r5lowermob=3,
    r5fallnum=0,
    predicted_class=0,
    predicted_score=0.89,
)

session.add(patient)
session.commit()
print("Default patient added")