from random import randint
from typing import Dict, List

import requests
from faker import Faker


def make_get_call(endpoint: str, params: dict = None) -> requests.Response:
    return requests.get(endpoint, params=params)


def make_post_call(endpoint: str, body: dict = {}) -> requests.Response:
    return requests.post(endpoint, json=body)


def sum_call(n: int = 1):
    endpoint = "http://localhost:8000/sum"
    for _ in range(n):
        params = {"val1": randint(0, 10000), "val2": randint(0, 10000)}
        make_get_call(endpoint, params)


def create_users(n: int = 1) -> List[Dict[str, str]]:
    endpoint = "http://localhost:8000/users"
    users_created: List[Dict[str, str]] = []

    for _ in range(n):
        params = {"email": Faker("en_US").email(), "password": Faker("en_US").password()}
        users_created.append(make_post_call(endpoint, params).json())

    return users_created


def create_items_for_users(users: List[Dict[str, str]]):
    for user in users:
        endpoint = f"http://localhost:8000/users/{user['id']}/items"
        params = {"title": " ".join(Faker("en_US").words()), "description": Faker("en_US").paragraph(nb_sentences=3)}
        make_post_call(endpoint, params)


def read_items():
    endpoint = "http://localhost:8000/items"
    print(make_get_call(endpoint).text)


def read_users():
    endpoint = "http://localhost:8000/users"
    print(make_get_call(endpoint).text)


if __name__ == "__main__":
    users = create_users()
    create_items_for_users(users)
    read_users()
    read_items()
