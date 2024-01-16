import json
import random

import requests
from faker import Faker

API_BASE_URL = "http://127.0.0.1:8000"

fake = Faker()


def get_values_from_config() -> dict:
    """
    Reads config file and return dict of values to be used in the script
    """
    FILE_PATH = "automated_bot/config.json"

    with open(FILE_PATH) as file:
        data = json.load(file)
        return data


def register_users(number_of_users: int) -> list:
    """
    Calls an endpoint to register specified number of users and creates a list of registered users
    """
    REGISTER_URL = f"{API_BASE_URL}/auth/register"
    users = []
    for _ in range(number_of_users):
        password = fake.password()
        user_request_data = {
            "username": fake.unique.first_name(),
            "email": fake.unique.email(),
            "password": password,
            "password2": password,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        register_response = requests.post(REGISTER_URL, json=user_request_data)

        if register_response.status_code == 201:
            # use initial data to store password for future login
            users.append(user_request_data)
    return users


def login_user(user_data: dict):
    """
    Uses user data to retrieve a token
    """
    LOGIN_URL = f"{API_BASE_URL}/auth/login"

    login_data = {"username": user_data["username"], "password": user_data["password"]}
    login_response = requests.post(LOGIN_URL, json=login_data)

    return login_response.json().get("access")


def create_posts(max_posts_number: int, headers: dict) -> list:
    """
    Creates random amount of posts, but not more than specified max value
    """
    POSTS_URL = f"{API_BASE_URL}/posts/"
    posts_amount = random.randint(1, max_posts_number)

    posts_ids = []
    for _ in range(posts_amount):
        post_data = {"body": fake.text(), "title": fake.text(50)}
        posts_response = requests.post(POSTS_URL, json=post_data, headers=headers)
        response_body = posts_response.json()
        posts_ids.append(response_body.get("id"))
    return posts_ids


def like_post(post_id: str, headers: dict):
    """
    Likes provided post
    """
    POSTS_LIKE_URL = f"{API_BASE_URL}/posts/{post_id}/likes"
    requests.post(POSTS_LIKE_URL, headers=headers)


def main():
    """
    Contains main bot logic
    """
    config_data = get_values_from_config()

    users = register_users(config_data["number_of_users"])
    # list of all posts that all users created
    posts_ids = []
    for user in users:
        token = login_user(user)
        headers = {"Authorization": f"Bearer {token}"}

        posts = create_posts(
            max_posts_number=config_data["max_posts_creation_per_user"], headers=headers
        )
        posts_ids.extend(posts)

    for user in users:
        # get token again to have control of what user likes post
        token = login_user(user)
        headers = {"Authorization": f"Bearer {token}"}

        user_likes_amount = 0
        while user_likes_amount < config_data["max_likes_per_user"]:
            # randomly choose post to like
            post_index = random.randint(1, len(posts_ids) - 1)
            like_post(posts_ids[post_index], headers)
            user_likes_amount += 1

    print("Bot finished execution completely")


if __name__ == "__main__":
    main()
