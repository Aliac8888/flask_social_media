from collections import defaultdict
from math import ceil

from tqdm import tqdm
from app import app
from models.auth import AuthRequest, AuthResponse
from models.comment import CommentInit
from models.post import Post, PostId, PostInit
from models.user import User, UserInit, UsersList
from random import randint, random, shuffle, sample
from config import admin_email, admin_pass
from faker import Faker
import setup

USERS_MIN = 500
USERS_MAX = 1000
USERS_MAX_ISOLATED = 100
USER_GRID_DIMS = 3
ONE_WAY_FOLLOW_ODDS = 0.5
TWO_WAY_FOLLOW_ODDS = 0.15
NORMAL_APPROX_COUNT = 100
USER_NO_POST_ODDS = 0.25
USER_MIN_POSTS = 1
USER_MAX_POSTS = 5
POST_NO_COMMENT_ODDS = 0.5
POST_MIN_COMMENTS = 1
POST_MAX_COMMENTS = 10


def randint_norm(l: int, h: int):
    values = [randint(l, h) for _ in range(NORMAL_APPROX_COUNT)]
    return round(sum(values) / NORMAL_APPROX_COUNT)


def index_to_pos(index: int, dims: list[int]):
    pos: list[int] = []

    for i in dims[:-1]:
        pos.append(index // i)
        index %= i

    pos.append(index)

    return tuple(pos)


def get_user_dims(users: list[User]):
    while True:
        dims: list[int] = []
        length = len(users)
        n_base = ceil(length ** (1 / USER_GRID_DIMS))

        for _ in range(USER_GRID_DIMS - 1):
            n = randint_norm(n_base // 2, n_base)

            new_length = ceil(length / n)

            if n == 1 or new_length == 1:
                break

            length = new_length
            dims.append(n)

        dims.append(length)

        if len(dims) < USER_GRID_DIMS:
            print("Too few user grid dimensions. Retrying….", dims)
        else:
            print("User grid dimensions are", dims)
            return dims


def generate_social_graph(users: list[User]):
    dims = get_user_dims(users)
    pos_of_obj = {v.id: index_to_pos(k, dims) for k, v in enumerate(users)}
    obj_of_pos = {v: k for k, v in pos_of_obj.items()}
    followings: defaultdict[str, set[str]] = defaultdict(set)

    for follower in users:
        pos = pos_of_obj[follower.id]

        for k, v in enumerate(pos):
            following_pos = (*pos[:k], v - 1, *pos[k + 1 :])
            following = obj_of_pos.get(following_pos)

            if following is None:
                continue

            luck = random()

            if luck < ONE_WAY_FOLLOW_ODDS:
                followings[follower.id].add(following)

            if luck < TWO_WAY_FOLLOW_ODDS:
                followings[following].add(follower.id)

    return followings


faker = Faker()

with app.test_client() as c:
    print("Authenticating….")

    jwt = AuthResponse.model_validate(
        c.post(
            "/users/login",
            json=AuthRequest(
                email=admin_email,
                password=admin_pass,
            ).model_dump(),
        ).json
    ).jwt

    print("Creating users….")

    for _ in tqdm(range(randint(USERS_MIN, USERS_MAX))):
        first = faker.first_name()
        last = faker.last_name()

        result = c.post(
            "/users/",
            json=UserInit(
                name=f"{first} {last}",
                email=f"{first}.{last}@example.com".lower(),
                password="",
            ).model_dump(),
        )

    print("Retrieving user list….")
    users = UsersList.model_validate(c.get("/users/").json).users
    assert users
    shuffle(users)

    print("Generating social graph….")
    followings = generate_social_graph(users)

    print("Following users….")
    for follower_id, followables in tqdm(followings.items()):
        for following_id in followables:
            result = c.put(
                f"/users/{follower_id}/followings/{following_id}",
                headers={"Authorization": f"Bearer {jwt}"},
            )

    print("Finding isolated users….")
    isolated_users = {i.id for i in users}

    for follower in users:
        if follower.id in followings:
            isolated_users.discard(follower.id)

    for follower in users:
        for following_id in followings[follower.id]:
            isolated_users.discard(following_id)

    users_to_remove = list(isolated_users)
    shuffle(users_to_remove)
    print("Found", len(users_to_remove), "isolated users. Deleting excess….")

    for user in tqdm(users_to_remove[USERS_MAX_ISOLATED:]):
        c.delete(
            f"/users/{user}",
            headers={"Authorization": f"Bearer {jwt}"},
        )

    print("Retrieving user list… (again).")
    users = UsersList.model_validate(c.get("/users/").json).users
    assert users
    shuffle(users)

    print("Creating posts and comments….")
    for post_author in tqdm(users):
        if random() < USER_NO_POST_ODDS:
            continue

        for _ in range(randint_norm(USER_MIN_POSTS, USER_MAX_POSTS)):
            post_id = PostId.model_validate(
                c.post(
                    "/posts/",
                    headers={"Authorization": f"Bearer {jwt}"},
                    json=PostInit(
                        author=post_author.id, content=faker.text()
                    ).model_dump(),
                ).json
            ).post_id

            if random() < POST_NO_COMMENT_ODDS:
                continue

            for comment_author in sample(
                users, randint_norm(POST_MIN_COMMENTS, POST_MAX_COMMENTS)
            ):
                c.post(
                    "/comments/",
                    headers={"Authorization": f"Bearer {jwt}"},
                    json=CommentInit(
                        author=comment_author.id,
                        post=post_id,
                        content=faker.text(),
                    ).model_dump(),
                )
