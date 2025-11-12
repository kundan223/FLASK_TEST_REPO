import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_predict_route(client):
    response = client.post('/api/predict', json={
        "user_name": "Alice",
        "amount": 1200.50,
        "location": "Delhi",
        "device": "iPhone 13"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
