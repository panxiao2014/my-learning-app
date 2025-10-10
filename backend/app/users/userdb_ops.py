from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Users


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