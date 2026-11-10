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


def test_hello(client):
    res = client.get("/hello?name=Laia")
    assert res.status_code == 200
    assert b"Laia" in res.data
