from random import randint
from typing import Dict, List

import requests
from faker import Faker


def make_get_call(endpoint: str, params: dict = None) -> requests.Response:
    return requests.get(endpoint, params=params)


def make_post_call(endpoint: str, body: dict = {}) -> requests.Response:
    return requests.post(endpoint, json=body)


def sum_call(port: int, n: int = 1):
    endpoint = f"http://localhost:{port}/sum/"
    for _ in range(n):
        params = {"val1": randint(0, 10000), "val2": randint(0, 10000)}
        make_get_call(endpoint, params)


def create_users(port: int, n: int = 1) -> List[Dict[str, str]]:
    endpoint = f"http://localhost:{port}/users/"
    users_created: List[Dict[str, str]] = []

    for _ in range(n):
        params = {"email": Faker("en_US").email(), "password": Faker("en_US").password()}
        users_created.append(make_post_call(endpoint, params).json())

    return users_created


def create_items_for_users(port: int, users: List[Dict[str, str]]):
    for user in users:
        endpoint = f"http://localhost:{port}/users/{user['id']}/items/"
        params = {"title": " ".join(Faker("en_US").words()), "description": Faker("en_US").paragraph(nb_sentences=3)}
        make_post_call(endpoint, params)


def read_items(port: int):
    endpoint = f"http://localhost:{port}/items/"
    make_get_call(endpoint).text


def read_users(port: int):
    endpoint = f"http://localhost:{port}/users/"
    make_get_call(endpoint).text


def auto_otel_app():
    print("making requests to auto otel app...")
    # auto otel app
    AUTO_OTEL_APP_PORT = 8000
    users = create_users(AUTO_OTEL_APP_PORT, 10)
    create_items_for_users(AUTO_OTEL_APP_PORT, users)
    read_users(AUTO_OTEL_APP_PORT)
    read_items(AUTO_OTEL_APP_PORT)
    print("finished requests to auto otel app")

def auto_otel_app2():
    print("making requests to auto otel app...")
    # auto otel app
    AUTO_OTEL_APP_PORT = 8001
    users = create_users(AUTO_OTEL_APP_PORT, 10)
    create_items_for_users(AUTO_OTEL_APP_PORT, users)
    read_users(AUTO_OTEL_APP_PORT)
    read_items(AUTO_OTEL_APP_PORT)
    print("finished requests to auto otel app")


def prog_otel_app():
    print("making requests to prog otel app...")
    # programmatic otel app
    PROG_OTEL_APP_PORT = 8002
    users = create_users(PROG_OTEL_APP_PORT, 10)
    create_items_for_users(PROG_OTEL_APP_PORT, users)
    read_users(PROG_OTEL_APP_PORT)
    read_items(PROG_OTEL_APP_PORT)
    print("finished requests to prog otel app")


if __name__ == "__main__":
    auto_otel_app()
    auto_otel_app2()
    prog_otel_app()
