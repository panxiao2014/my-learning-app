import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.users.userdb_utils import init_database_session, seed_database
from app.config.config import TEST_PING
from app.config.config import USER_ADD_RESULT, USER_DELETE_RESULT, FakeUser


@pytest.fixture(scope="module")
def setup_database():
    """Set up database session for all FastAPI tests."""
    # Initialize database session for testing
    init_database_session(app)
    seed_database()
    
    # Provide database session to tests (assumes tables and data already exist)
    SessionLocal = app.state.db_session_factory
    db = SessionLocal()
    try:
        yield db  # Provide the database session to tests
        
    finally:
        db.close()
        # Clean up database engine
        if hasattr(app.state, 'db_engine'):
            app.state.db_engine.dispose()


@pytest.mark.fastapi
def test_ping_returns_test_ping_string():
    client = TestClient(app)
    response = client.get("/ping")
    assert response.status_code == 200
    body = response.json()
    assert body.get("message") == TEST_PING


@pytest.mark.fastapi
def test_ramdon_user_returns_valid_user(setup_database):
    """Test that /randomUser endpoint returns a valid user when users exist in database."""
    # Test the endpoint
    client = TestClient(app)
    response = client.get("/randomUser")
    
    # Verify response
    assert response.status_code == 200
    body = response.json()
    
    # Verify the response contains the expected fields
    assert "name" in body
    assert "gender" in body
    assert "age" in body
    
    # Verify data types
    assert isinstance(body["name"], str)
    assert isinstance(body["gender"], str)
    assert isinstance(body["age"], int)
    
    # Verify gender is one of the valid values
    assert body["gender"] in ["Male", "Female"]
    
    # Verify age is within valid range
    assert 0 <= body["age"] <= 100
    
    # Verify name is not empty
    assert len(body["name"]) > 0

@pytest.mark.fastapi
def test_add_and_delete_user():
    """Test that /addUser and /deleteUser endpoints work correctly."""

    client = TestClient(app)
    response = client.post("/addUser", json=FakeUser)
    assert response.status_code == USER_ADD_RESULT["success"].status_code
    body = response.json()
    assert body.get("message") == USER_ADD_RESULT["success"].message

    response = client.post("/deleteUser", json={"name": FakeUser["name"]})
    assert response.status_code == USER_DELETE_RESULT["success"].status_code
    body = response.json()
    assert body.get("message") == USER_DELETE_RESULT["success"].message