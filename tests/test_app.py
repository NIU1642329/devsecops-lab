import pytest

from dice_app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_roll_default_d6(client):
    res = client.get("/rolldice?player=laia")
    assert res.status_code == 200
    body = res.get_json()
    assert body["player"] == "laia"
    assert 1 <= body["result"] <= 6


def test_roll_d20(client):
    body = client.get("/rolldice?sides=20").get_json()
    assert 1 <= body["result"] <= 20


@pytest.mark.parametrize("sides", ["abc", "1", "-3"])
def test_roll_rejects_bad_sides(client, sides):
    assert client.get(f"/rolldice?sides={sides}").status_code == 400


def test_hello(client):
    res = client.get("/hello?name=Laia")
    assert res.status_code == 200
    assert b"Laia" in res.data


def test_hello_escapes_html(client):
    res = client.get("/hello?name=<script>alert(1)</script>")
    assert b"<script>" not in res.data
    assert b"&lt;script&gt;" in res.data


def test_ping_rejects_shell_injection(client):
    res = client.get("/ping?host=127.0.0.1;cat /etc/passwd")
    assert res.status_code == 400


def test_admin_denied_without_configured_password(client):
    assert client.get("/admin?password=").status_code == 403
    assert client.get("/admin?password=changeme").status_code == 403
