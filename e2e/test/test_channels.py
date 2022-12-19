import os
import requests

URL = "http://backend:3080"


def test_channels():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "title": "Zizaran",
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert r.json()["message"] == "Added channel Zizaran"

    r = requests.get(URL + "/channels")
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert r.json()["message"] == [
        {"title": "Zizaran", "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA"}
    ]

    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert r.json()["message"] == "Channel with id UCAG3CiKOUkQysyKCXSFEBPA was deleted"


def test_auth_no_auth():
    headers = {
        "Content-type": "application/json",
    }
    data = {
        "title": "Zizaran",
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Request unauthorized"

    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Request unauthorized"


def test_auth_wrong_auth():
    headers = {"Content-type": "application/json", "Authorize": "bad_token"}
    data = {
        "title": "Zizaran",
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Request unauthorized"

    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 401
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Request unauthorized"


def test_add_channel_missing_title():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Channel details missing"


def test_add_channel_missing_id():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "title": "Zizaran",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Channel details missing"


def test_delete_channel_wrong_id():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "wrong_id",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "No channel with id wrong_id"


def test_delete_channel_missing_id():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    r = requests.delete(URL + "/channels", json={}, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "No channel data"
