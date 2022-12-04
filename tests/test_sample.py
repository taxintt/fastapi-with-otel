from fastapi.testclient import TestClient

from app.src.main import app

client = TestClient(app)


def test_get_sample():
    response = client.get("/sample")
    assert response.status_code == 200
    assert response.json() == {"message": "return sample"}
