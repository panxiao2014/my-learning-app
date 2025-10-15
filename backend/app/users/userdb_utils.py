"""
Common utilities for user database operations.
This module contains shared functions used across user-related database operations.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from .models import Users
from pathlib import Path
from fastapi import FastAPI
import json


def get_db_host() -> str:
    #If running in AWS, use RDS_DATABASE_HOST defined in backend task:
    if os.getenv("RDS_DATABASE_HOST"):
        print("🐳 Detected AWS, using 'RDS_DATABASE_HOST'")
        return os.getenv("RDS_DATABASE_HOST")
    
    # If running inside Docker, use docker network hostname
    if os.getenv("RUNNING_IN_DOCKER"):
        print("🐳 Detected Docker via RUNNING_IN_DOCKER env, using 'postgres'")
        return "postgres"
    
    return "localhost"


def get_localhost_url() -> str:
    # If running in Github Actions, use 80:
    if os.getenv("RUN_IN_GITHUB_ACTIONS"):
        return "http://localhost:80"
    else:
        return "http://localhost:5173"
    

def read_postgres_password() -> str:
    """
    Read PostgreSQL password from environment variable or file.
    
    Returns:
        str: The PostgreSQL password
        
    Raises:
        RuntimeError: If password is not found in environment variable or file
    """
    # Try to get from environment variable (for AWS deployment)
    # the value is got from the AWS Secrets Manager by secret ARN, which is defined in the AWS Task and have the following format:
    # {"username":"postgres","password":"<password>","engine":"postgres","host":"userdb.abcdefg.ap-northeast-3.rds.amazonaws.com","port":5432,"dbInstanceIdentifier":"userdb"}
    postgres_secret = os.getenv("POSTGRES_SECRET")
    if postgres_secret:
        print(f"🐳 Detected POSTGRES_SECRET")
        return json.loads(postgres_secret)["password"]
    
    # try to get from environment variable (for CI/CD in Github Actions)
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    if postgres_password:
        print(f"🐳 Detected POSTGRES_PASSWORD")
        return postgres_password
    
    #get password from local file
    tokens_path = Path(__file__).resolve().parent.parent.parent / "tokens" / "postgresql.txt"
    try:
        return tokens_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise RuntimeError(f"PostgreSQL password not found in environment variable POSTGRES_PASSWORD or file at: {tokens_path}")

def seed_database():
    """Seed the database with test users."""
    try:
        db_host = get_db_host()
        password = read_postgres_password()
        # Get database connection
        
        database_url = f"postgresql+psycopg2://postgres:{password}@{db_host}:5432/userdb"
        
        # Create engine and session
        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Ensure the users table exists (supports custom __tablename__ changes)
        inspector = inspect(engine)
        users_table_name = Users.__tablename__
        if not inspector.has_table(users_table_name):
            # Create the table using raw SQL with IF NOT EXISTS and anonymous constraints
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {users_table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL UNIQUE,
                gender VARCHAR(6) NOT NULL CHECK (gender IN ('Male','Female')),
                age INTEGER NOT NULL CHECK (age >= 0 AND age <= 100)
            )
            """
            with engine.begin() as conn:
                conn.execute(text(create_sql))
        
        # Create session
        db = SessionLocal()
        
        try:
            # Check if users already exist
            existing_users = db.query(Users).count()
            if existing_users > 0:
                return
            
            # Create test users
            test_users = [
                Users(name="Alice", gender="Female", age=25),
                Users(name="Bob", gender="Male", age=30),
            ]
            
            # Add users to database
            for user in test_users:
                db.add(user)
            
            # Commit changes
            db.commit()

            # Verify the seeded users can be retrieved
            retrieved = db.query(Users).filter(Users.name.in_([u.name for u in test_users])).all()
            retrieved_names = {u.name for u in retrieved}
            expected_names = {u.name for u in test_users}
            if retrieved_names != expected_names:
                sys.exit(1)
            
            for user in retrieved:
                print(f"  - {user.name} ({user.gender}, age {user.age})")
                
        except Exception as e:
            db.rollback()
            print(f"🛒 Error seeding database: {e}")
            sys.exit(1)
        finally:
            db.close()
            
    except Exception as e:
        print(f"🛒 Error connecting to database: {e}")
        sys.exit(1)

def init_database_session(app: FastAPI):
    """
    Initialize database session for the application.
    
    Args:
        app: FastAPI application instance
    """
    db_host = get_db_host()

    try:
        password = read_postgres_password()
        database_url = f"postgresql+psycopg2://postgres:{password}@{db_host}:5432/userdb"
        engine = create_engine(database_url, pool_pre_ping=True)
        # Probe connectivity early to fail fast
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as exc:
        message = "Failed to initialize database session to host '{host}': {err}".format(
            host=db_host, err=str(exc)
        )
        raise RuntimeError(message) from exc

    app.state.db_engine = engine
    app.state.db_session_factory = SessionLocal

    return

