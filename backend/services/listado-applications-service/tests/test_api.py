from fastapi.testclient import TestClient
from app.main import app


def test_health():
    assert TestClient(app).get("/health").json()["status"] == "ok"


def test_requires_bearer():
    response = TestClient(app).post("/publicaciones/compartidas", json={
        "titulo": "Pieza cerca de universidad", "region": "La Araucanía",
        "comuna": "Temuco", "precio_clp": 180000, "cupos_totales": 2
    })
    assert response.status_code == 401


def test_service_does_not_write_if_authusers_denies(monkeypatch):
    import uuid
    import httpx
    from fastapi import HTTPException
    from app.application import ListingService
    from app.config import Settings
    from app.security import Identity

    class FakeRepo:
        called = False
        def create(self, *_args, **_kwargs):
            self.called = True

    repo = FakeRepo()
    identity = Identity(id=uuid.uuid4(), email="test@example.com", bearer="testtoken")
    captured = {}

    def fake_get(url, headers, timeout):
        captured["authorization"] = headers["Authorization"]
        return httpx.Response(404, json={"detail": "No hay perfil"})

    monkeypatch.setattr("app.application.httpx.get", fake_get)
    try:
        ListingService(repo, Settings()).create(identity, {"titulo": "Ejemplo"})
    except HTTPException as error:
        assert error.status_code == 409
    else:
        raise AssertionError("Se esperaba la validación cruzada")
    assert not repo.called
    assert captured["authorization"] == "Bearer testtoken"
