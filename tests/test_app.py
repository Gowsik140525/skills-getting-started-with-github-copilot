import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "participants" in data["Basketball"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/Basketball/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Basketball" in response.json()["message"]
    # Check participant is added
    get_resp = client.get("/activities")
    assert email in get_resp.json()["Basketball"]["participants"]

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_for_activity_already_signed_up():
    email = "alex@mergington.edu"
    # Already in Basketball
    response = client.post(f"/activities/Basketball/signup?email={email}")
    # Should be 400 error for already signed up
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
