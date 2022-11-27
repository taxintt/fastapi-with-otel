from fastapi.testclient import TestClient

from app.src.main import app

client = TestClient(app)


def test_hoge():
    response = client.get("/hoge")
    assert response.status_code == 200
    assert response.json() == {"message": "return hoge"}
