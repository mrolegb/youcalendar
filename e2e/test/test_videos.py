import os
import requests

URL = "http://backend:3080"


def test_videos():
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

    # flush cache
    assert requests.get(URL + "/cache", headers=headers).status_code == 200

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert len(r.json()["message"]) == 50

    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200


def test_videos_multiple_channels():
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
    data = {
        "title": "Asmongold",
        "channel_id": "UCQeRaTukNYft1_6AZPACnog",
    }
    r = requests.post(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200

    # flush cache
    assert requests.get(URL + "/cache", headers=headers).status_code == 200

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    # assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert len(r.json()["message"]) == 100

    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200
    data = {
        "channel_id": "UCQeRaTukNYft1_6AZPACnog",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200


def test_videos_no_channels():
    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 500
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "No channels added"


def test_videos_no_from_date():
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

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Invalid request parameters"

    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200


def test_videos_no_to_date():
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

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Invalid request parameters"

    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200


def test_videos_wrong_content_type():
    headers = {
        "Content-type": "text",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 400
    assert r.json()["status"] == "error"
    assert r.json()["message"] == "Invalid content, expecting json"


def test_videos_cache():
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

    # flush cache
    assert requests.get(URL + "/cache", headers=headers).status_code == 200

    headers = {
        "Content-type": "application/json",
    }
    data = {
        "date_from": "2022-10-01T16:34:58Z",
        "date_to": "2022-10-21T16:34:58Z",
    }
    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert len(r.json()["message"]) == 50

    r = requests.post(URL + "/videos", json=data, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert len(r.json()["message"]) == 50

    headers = {
        "Content-type": "application/json",
        "Authorize": os.environ.get("AUTH_KEY"),
    }
    data = {
        "channel_id": "UCAG3CiKOUkQysyKCXSFEBPA",
    }
    r = requests.delete(URL + "/channels", json=data, headers=headers)
    assert r.status_code == 200
