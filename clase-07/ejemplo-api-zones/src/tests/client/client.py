import requests


class UsersClient:
    USER_URL = "{uri}/users/{user_id}"
    USERS_URL = "{uri}/users"

    def __init__(self, uri):
        self.uri = uri

    def get_user(self, user_id):
        response = requests.get(self.USER_URL.format(uri=self.uri, user_id=user_id))
        return response.json()

    def add_user(self, username, email):
        requests.post(
            self.USERS_URL.format(uri=self.uri),
            json={"username": username, "email": email},
        )
        return

    def delete_user(self, user_id):
        requests.delete(self.USER_URL.format(uri=self.uri, user_id=user_id))
        return

    def update_user(self, user_id, username, email):
        requests.put(
            self.USER_URL.format(uri=self.uri, user_id=user_id),
            json={"username": username, "email": email},
        )
        return

    def get_users(self):
        response = requests.get(self.USERS_URL.format(uri=self.uri))
        return response.json()
