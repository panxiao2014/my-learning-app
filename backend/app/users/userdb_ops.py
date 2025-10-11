from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Users
from app.config.config import UserAddResultType, USER_ADD_RESULT, USER_DELETE_RESULT, FakeUser


def choose_ramdon_user(db: Session) -> Optional[Dict[str, Any]]:
    """
    Randomly select a user from the users table.
    Returns None if no users exist in the database.
    """
    # Get total count of users
    try:
        total_users = db.query(Users).count()
    except Exception as e:
        print(f"⚠️ Error getting total users: {e}")
        return None
    
    if total_users == 0:
        return None
    
    # Get a random user using OFFSET with random ordering
    random_user = db.query(Users).order_by(func.random()).first()
    
    if random_user:
        return {
            "name": random_user.name,
            "gender": random_user.gender,
            "age": random_user.age,
        }
    
    return None


def add_user(db: Session, user: Dict[str, Any]) -> UserAddResultType:
    """
    Add a user to the users table.
    Checks for duplicate user and returns result accordingly.
    """
    # Check if user already exists (by name only)
    try:
        existing_user = db.query(Users).filter_by(
            name=user["name"]
        ).first()
    except Exception as e:
        db.rollback()
        return USER_ADD_RESULT["error"]
    if existing_user:
        return USER_ADD_RESULT["duplicate"]

    try:
        db.add(Users(name=user["name"], gender=user["gender"], age=user["age"]))
        db.commit()
        return USER_ADD_RESULT["success"]
    except Exception as e:
        db.rollback()
        return USER_ADD_RESULT["error"]
    return


def delete_user(db: Session, user: Dict[str, str]) -> UserAddResultType:
    """
    Delete a user from the users table.
    """
    user_name = user["name"]
    #check if user does not exist:
    if not db.query(Users).filter_by(name=user_name).first():
        return USER_DELETE_RESULT["not_found"]

    try:
        db.query(Users).filter_by(name=user_name).delete()
        db.commit()
        return USER_DELETE_RESULT["success"]
    except Exception as e:
        db.rollback()
        return USER_DELETE_RESULT["error"]
    return


def delete_fake_user(db: Session) -> UserAddResultType:
    """
    Delete the fake test user from the users table.
    This function is specifically for cleaning up test data.
    """
    return delete_user(db, {"name": FakeUser["name"]})