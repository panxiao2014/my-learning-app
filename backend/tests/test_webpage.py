import pytest
from playwright.sync_api import Page, expect
from sqlalchemy.orm import Session

from app.config.config import TEST_PING, FakeUser, USER_ADD_RESULT, LOCAL_HOST_URL
from app.users.userdb_ops import delete_fake_user
from app.users.userdb_utils import init_database_session
from app.main import app


@pytest.fixture(scope="module")
def setup_database():
    """Set up database session for e2e tests."""
    # Initialize database session for testing
    init_database_session(app)
    
    # Provide database session to tests
    SessionLocal = app.state.db_session_factory
    db = SessionLocal()
    try:
        yield db  # Provide the database session to tests
    finally:
        db.close()


@pytest.mark.e2e
def test_click_button_displays_test_ping(page: Page):
    # Open the frontend app
    page.goto(LOCAL_HOST_URL)

    # Navigate to the Main tab (should be default, but ensure we're on the right tab)
    page.get_by_test_id("main-nav-button").click()
    
    # Wait for the main content to be visible
    main_content = page.get_by_test_id("main-content")
    expect(main_content).to_be_visible()

    # Click the button labeled "Click me"
    page.get_by_role("button", name="Click me").click()

    # Expect the TEST_PING text to become visible
    expect(page.get_by_text(TEST_PING)).to_be_visible()

    # Additionally, verify that the TEST_PING text is displayed to the right of the button
    button = page.get_by_role("button", name="Click me")
    resp_text = page.get_by_text(TEST_PING)

    # Get bounding boxes for both elements
    button_box = button.bounding_box()
    resp_box = resp_text.bounding_box()

    # Assert that the TEST_PING text is to the right of the button
    assert button_box is not None and resp_box is not None, "Could not get bounding boxes"
    assert resp_box["x"] > button_box["x"] + button_box["width"], "TEST_PING text is not to the right of the button"
    
    # Also verify they are on the same vertical position
    button_center_y = button_box["y"] + button_box["height"] / 2
    resp_center_y = resp_box["y"] + resp_box["height"] / 2
    assert abs(button_center_y - resp_center_y) < 5, "TEST_PING text is not aligned vertically with the button"


@pytest.mark.e2e
def test_click_show_me_a_user_button_displays_user_info(page: Page):
    # Open the frontend app
    page.goto(LOCAL_HOST_URL)

    # Navigate to the Users tab first
    page.get_by_test_id("users-nav-button").click()
    
    # Wait for the users content to be visible
    users_content = page.get_by_test_id("users-content")
    expect(users_content).to_be_visible()

    # Click the button labeled "Show me a user"
    page.get_by_role("button", name="Show me a user").click()

    # Wait for the user information to be displayed in the specific user display area
    # Use the new data-testid for more reliable targeting
    user_display_area = page.get_by_test_id("user-display-content")
    expect(user_display_area).to_be_visible()
    
    # Verify that the user information is displayed in the correct container
    # Check for the specific user data labels within the user display area
    expect(user_display_area.get_by_text("Name:")).to_be_visible()
    expect(user_display_area.get_by_text("Gender:")).to_be_visible()
    expect(user_display_area.get_by_text("Age:")).to_be_visible()

    # Verify that the user information is displayed in the correct format
    # The text should be in the format: "Name: [name]", "Gender: [gender]", "Age: [age]"
    user_info_container = user_display_area.locator("div:has-text('Name:')").first
    expect(user_info_container).to_be_visible()
    
    # Verify that the "No user selected yet." text is no longer visible
    expect(page.get_by_text("No user selected yet.")).not_to_be_visible()


@pytest.mark.e2e
def test_click_add_user_button(page: Page, setup_database: Session):
    """
    Use FakeUser to test the add user button.
    """

    # Open the frontend app
    page.goto(LOCAL_HOST_URL)
    
    # Navigate to the Users tab
    page.get_by_test_id("users-nav-button").click()
    
    # Wait for the users content to be visible
    users_content = page.get_by_test_id("users-content")
    expect(users_content).to_be_visible()
    
    # Locate the add-user-form div by its data-testid
    add_user_form = page.get_by_test_id("add-user-form")

    # Fill the form fields using data from FakeUser
    add_user_form.get_by_label("Name").fill(FakeUser["name"])
    add_user_form.get_by_label("Gender").select_option(FakeUser["gender"])
    add_user_form.get_by_label("Age").fill(str(FakeUser["age"]))

    # Click the "Add User" button within the form
    add_user_form.get_by_role("button", name="Add User").click()
    
    # Wait for the popup modal to appear using the friendly ID
    popup_modal = page.get_by_test_id("add-user-popup-modal")
    expect(popup_modal).to_be_visible()
    
    # Verify the popup content is visible using the friendly ID
    popup_content = page.get_by_test_id("add-user-popup-content")
    expect(popup_content).to_be_visible()
    
    # Locate the popup message by its ID and check for the success message within it
    popup_message = popup_content.get_by_test_id("add-user-popup-message")
    expect(popup_message).to_contain_text(USER_ADD_RESULT["success"].message)
    
    # Verify the OK button is present and clickable
    ok_button = popup_content.get_by_role("button", name="OK")
    expect(ok_button).to_be_visible()
    expect(ok_button).to_be_enabled()
    
    # Clean up: delete the fake user after test completion
    try:
        delete_fake_user(setup_database)
    except Exception as e:
        print(f"Failed to delete fake user: {e}")
