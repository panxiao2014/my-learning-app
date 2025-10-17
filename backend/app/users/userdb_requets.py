from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .userdb_ops import choose_ramdon_user, add_user, delete_user


router = APIRouter()


def get_db(request: Request) -> Session:
    """Dependency to get database session"""
    SessionLocal = request.app.state.db_session_factory
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/addUser")
async def add_user_request(request: Request, db: Session = Depends(get_db)):
    # get the user from the request:
    user = await request.json()
    ret = add_user(db, user)
    return ret


@router.get("/randomUser")
async def ramdon_user(db: Session = Depends(get_db)) -> dict:
    user = choose_ramdon_user(db)
    if user is None:
        raise HTTPException(status_code=404, detail="No users found in database")
    return user


@router.post("/deleteUser")
async def delete_user_request(request: Request, db: Session = Depends(get_db)):
    # get the user from the request:
    user = await request.json()
    ret = delete_user(db, user)
    return ret