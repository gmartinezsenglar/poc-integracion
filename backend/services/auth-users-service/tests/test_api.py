from fastapi.testclient import TestClient
from app.main import app


def test_health():
    r = TestClient(app).get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "auth-users"


def test_requires_bearer():
    r = TestClient(app).get("/usuarios/me")
    assert r.status_code == 401
