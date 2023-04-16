import pytest
import requests
from pactman import EachLike, Like, Term

TEST_USERNAME = "fede"
TEST_EMAIL = "fede@itba.edu"


def test_get_user(pact, user_client):
    TESTED_ID = 1
    BODY_EXPECTED = {
        "id": Term(r"\d+", TESTED_ID),
        "username": "fede",
        "email": TEST_EMAIL,
        "created_date": Term(
            r"\d+-\d+-\d+T\d+:\d+:\d+\.\d+", "2023-03-30T13:11:52.768450"
        ),
    }

    (
        pact.given("User fede exist in db")
        .upon_receiving("a request for fede user")
        .with_request("get", f"/users/{TESTED_ID}")
        .will_respond_with(200, body=BODY_EXPECTED)
    )
    with pact:
        user_client.get_user(TESTED_ID)


def test_add_user(pact, user_client):
    POST_BODY = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
    }
    BODY_EXPECTED = {
        "id": Like(1),
        "message": Term(r"[^\s]+ was added!", f"{TEST_EMAIL} was added!"),
    }
    (
        pact.given("User fede does not exist in db")
        .upon_receiving("a request for add fede user")
        .with_request(
            method="POST",
            path="/users",
            body=POST_BODY,
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(201, body=BODY_EXPECTED)
    )
    with pact:
        user_client.add_user(username=TEST_USERNAME, email=TEST_EMAIL)


@pytest.mark.parametrize(
    "payload, issue",
    [
        [{}, "an empty payload"],
        [{"email": TEST_EMAIL}, "missing username"],
        [{"username": TEST_USERNAME}, "missing email"],
        [
            {"user": TEST_USERNAME, "email": TEST_EMAIL},
            "missing username and other field",
        ],
        [
            {"username": TEST_USERNAME, "mail": TEST_EMAIL},
            "missing email and other field",
        ],
    ],
)
def test_add_user_invalid_json_keys(pact, user_client, payload, issue):
    RESP_BODY = {"message": Like("Input payload validation failed")}
    (
        pact.given("Any case")
        .upon_receiving(f"Adding a user with {issue}")
        .with_request(
            method="POST",
            path="/users",
            body=payload,
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(400, body=RESP_BODY)
    )
    with pact:
        requests.post(user_client.USERS_URL.format(uri=pact.uri), json=payload)


def test_single_user_incorrect_id(pact, user_client):
    TESTED_ID = 99999
    BODY_EXPECTED = {
        "message": Term(r"User \d+ does not exist", f"User {TESTED_ID} does not exist")
    }
    (
        pact.given("Any case")
        .upon_receiving("a request with invalid id")
        .with_request("get", f"/users/{TESTED_ID}")
        .will_respond_with(404, body=BODY_EXPECTED)
    )
    with pact:
        user_client.get_user(TESTED_ID)


def test_remove_user_incorrect_id(pact, user_client):
    TESTED_ID = 99999
    BODY_EXPECTED = {
        "message": Term(r"User \d+ does not exist", f"User {TESTED_ID} does not exist")
    }
    (
        pact.given("Any case")
        .upon_receiving("a delete with invalid id")
        .with_request("delete", f"/users/{TESTED_ID}")
        .will_respond_with(404, body=BODY_EXPECTED)
    )
    with pact:
        user_client.delete_user(TESTED_ID)


def test_remove_user(pact, user_client):
    TESTED_ID = 1
    BODY_EXPECTED = {
        "message": Term(r"[^\s]+ was removed!", f"User {TEST_EMAIL} does not exist")
    }
    (
        pact.given("User fede exist in db")
        .upon_receiving("a delete with a valid id")
        .with_request("delete", f"/users/{TESTED_ID}")
        .will_respond_with(200, body=BODY_EXPECTED)
    )
    with pact:
        user_client.delete_user(TESTED_ID)


def test_update_user(pact, user_client):
    TESTED_ID = 1
    PUT_BODY = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
    }
    BODY_EXPECTED = {
        "id": Like(1),
        "message": Term(r"[^\s]+ was updated!", f"{TEST_EMAIL} was updated!"),
    }
    (
        pact.given("User fede exist in db")
        .upon_receiving("a request for update fede user")
        .with_request(
            method="PUT",
            path=f"/users/{TESTED_ID}",
            body=PUT_BODY,
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(200, body=BODY_EXPECTED)
    )
    with pact:
        user_client.update_user(
            user_id=TESTED_ID, username=TEST_USERNAME, email=TEST_EMAIL
        )


@pytest.mark.parametrize(
    "payload, issue",
    [
        [{}, "an empty payload"],
        [{"email": TEST_EMAIL}, "missing username"],
        [{"username": TEST_USERNAME}, "missing email"],
        [
            {"user": TEST_USERNAME, "email": TEST_EMAIL},
            "missing username and other field",
        ],
        [
            {"username": TEST_USERNAME, "mail": TEST_EMAIL},
            "missing email and other field",
        ],
    ],
)
def test_update_user_with_invalid_fields(pact, user_client, payload, issue):
    RESP_BODY = {"message": Like("Input payload validation failed")}
    TESTED_ID = 1
    (
        pact.given("User fede exist in db")
        .upon_receiving(f"a request for update with {issue} ")
        .with_request(
            method="PUT",
            path=f"/users/{TESTED_ID}",
            body=payload,
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(400, body=RESP_BODY)
    )
    with pact:
        requests.put(
            user_client.USER_URL.format(uri=pact.uri, user_id=TESTED_ID), json=payload
        )


def test_update_user_incorrect_id(pact, user_client):
    TESTED_ID = 99999
    PUT_BODY = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
    }
    BODY_EXPECTED = {
        "message": Term(r"User \d+ does not exist", f"User {TESTED_ID} does not exist")
    }
    (
        pact.given("Any case")
        .upon_receiving("an update with invalid user id")
        .with_request(
            method="PUT",
            path=f"/users/{TESTED_ID}",
            body=PUT_BODY,
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(404, body=BODY_EXPECTED)
    )
    with pact:
        user_client.update_user(
            user_id=TESTED_ID, username=TEST_USERNAME, email=TEST_EMAIL
        )


def test_all_users(pact, user_client):
    BODY_EXPECTED = EachLike(
        {
            "id": Term(r"\d+", 1),
            "username": "fede",
            "email": "fede@itba.edu",
            "created_date": Term(
                r"\d+-\d+-\d+T\d+:\d+:\d+\.\d+", "2023-03-30T13:11:52.768450"
            ),
        }
    )
    (
        pact.given("Users exist in db")
        .upon_receiving("a request for all users")
        .with_request("get", "/users")
        .will_respond_with(200, body=BODY_EXPECTED)
    )
    with pact:
        user_client.get_users()
