from fastapi.testclient import TestClient
from app.main import app


def test_health():
    assert TestClient(app).get("/health").json() == {"status": "ok", "service": "gateway"}


def test_upstream_status_and_authorization(monkeypatch):
    """Gateway conserva estado HTTP y reenvía el Bearer al microservicio."""
    import httpx
    from app import main

    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["authorization"] = request.headers.get("authorization")
        return httpx.Response(409, json={"detail": "Una regla de negocio lo impide"})

    transport = httpx.MockTransport(handler)
    original_client = httpx.AsyncClient
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda **kwargs: original_client(transport=transport))
    response = TestClient(app).patch(
        "/usuarios/me", headers={"Authorization": "Bearer token-de-prueba"}, json={"nombre": "Test"}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Una regla de negocio lo impide"
    assert seen["authorization"] == "Bearer token-de-prueba"
