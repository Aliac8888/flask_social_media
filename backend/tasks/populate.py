#!/usr/bin/env python
"""Reset and populate the database with mock data."""

import sys
from collections import defaultdict
from contextlib import suppress
from json import dumps
from logging import getLogger
from math import ceil
from random import randint, random, sample, shuffle

import __init__  # noqa: F401
from bson.objectid import ObjectId
from faker import Faker
from tqdm import tqdm

from server.auth.controller import signup
from server.comments.controller import create_comment
from server.followings.controller import follow_user
from server.posts.controller import create_post
from server.users.controller import delete_user, get_all_users
from server.users.controller_model import DbUser, DbUserExistsError, DbUserNotFoundError
from tasks.setup import setup

USERS_MIN = 500
"""Minimum number of users."""

USERS_MAX = 1000
"""Maximum number of users."""

USERS_MAX_ISOLATED = 100
"""Maximum number of users which are allowed to be isolated."""

USER_GRID_DIMS = 3
"""Number of dimensions of the rectilinear grid used for user followings."""

ONE_WAY_FOLLOW_ODDS = 0.5
"""Odds that a user might follow another nearby user."""

TWO_WAY_FOLLOW_ODDS = 0.15
"""Odds that two nearby users might follow each other."""

NORMAL_APPROX_COUNT = 100
"""Number of uniformly random samples to use to approximate a normal distribution."""

USER_NO_POST_ODDS = 0.25
"""Odds that a user does not make any posts."""

USER_MIN_POSTS = 1
"""Minimum posts a user can make. This excludes users without any posts."""

USER_MAX_POSTS = 5
"""Maximum posts a user can make."""

POST_NO_COMMENT_ODDS = 0.5
"""Odds that a user does not make any comments."""

POST_MIN_COMMENTS = 1
"""Minimum comments a user can make. This excludes users without any comments."""

POST_MAX_COMMENTS = 10
"""Maximum comments a user can make."""

_logger = getLogger(__name__)


def _randint_norm(min_value: int, max_value: int) -> int:
    """Return a random number, approximately following a normal distribution.

    Args:
        min_value (int): Smallest possible value.
        max_value (int): Largest possible value.

    Returns:
        int: The random number.

    """
    # This uses Central Limit Theorem to generate a normal distribution, due to
    # its simplicity.
    values = (randint(min_value, max_value) for _ in range(NORMAL_APPROX_COUNT))  # noqa: S311
    return round(sum(values) / NORMAL_APPROX_COUNT)


def _index_to_pos(index: int, dims: tuple[int, ...]) -> tuple[int, ...]:
    """Convert a linear index into a coordinates.

    Args:
        index (int): Linear index.
        dims (tuple[int, ...]): Rectilinear grid dimensions.

    Returns:
        tuple[int, ...]: Rectilinear grid coordinates.

    """
    pos: list[int] = []

    for i in dims[:-1]:
        pos.append(index // i)
        index %= i

    pos.append(index)

    return tuple(pos)


def _get_user_dims(users_count: int) -> tuple[int, ...]:
    """Get random dimensions for a rectilinear grid.

    Args:
        users_count (int): Number of users to allocate in the grid.

    Returns:
        tuple[int, ...]: Rectilinear grid dimensions.

    """
    while True:
        dims: list[int] = []
        length = users_count
        n_base = ceil(length ** (1 / USER_GRID_DIMS))

        for _ in range(USER_GRID_DIMS - 1):
            n = _randint_norm(n_base // 2, n_base)

            new_length = ceil(length / n)

            if n == 1 or new_length == 1:
                break

            length = new_length
            dims.append(n)

        dims.append(length)

        if len(dims) < USER_GRID_DIMS:
            _logger.warning(
                "Too few user grid dimensions (%s). Retrying….", dumps(dims)
            )
        else:
            _logger.info("User grid dimensions are %s.", dumps(dims))
            return tuple(dims)


def _generate_social_graph(users: list[DbUser]) -> defaultdict[ObjectId, set[ObjectId]]:
    """Generate a random followings graph.

    Args:
        users (list[DbUser]): Users.

    Returns:
        defaultdict[ObjectId, set[ObjectId]]: User followings.

    """
    dims = _get_user_dims(len(users))
    pos_of_obj = {v.id: _index_to_pos(k, dims) for k, v in enumerate(users)}
    obj_of_pos = {v: k for k, v in pos_of_obj.items()}
    followings: defaultdict[ObjectId, set[ObjectId]] = defaultdict(set)

    for follower in users:
        pos = pos_of_obj[follower.id]

        for k, v in enumerate(pos):
            following_pos = (*pos[:k], v - 1, *pos[k + 1 :])
            following = obj_of_pos.get(following_pos)

            if following is None:
                continue

            luck = random()  # noqa: S311

            if luck < ONE_WAY_FOLLOW_ODDS:
                followings[follower.id].add(following)

            if luck < TWO_WAY_FOLLOW_ODDS:
                followings[following].add(follower.id)

    return followings


def populate() -> None:  # noqa: C901, PLR0912
    """Reset and populate the database with mock data."""
    setup()

    faker = Faker()

    _logger.info("Creating users….")

    for _ in tqdm(range(randint(USERS_MIN, USERS_MAX))):  # noqa: S311
        first = faker.first_name()
        last = faker.last_name()

        with suppress(DbUserExistsError):
            signup(
                name=f"{first} {last}",
                email=f"{first}.{last}@example.com".lower(),
                password="",
            )

    _logger.info("\tDone.")
    _logger.info("Retrieving user list….")
    users = get_all_users().root

    if not users:
        _logger.critical("There were no users, somehow.")
        sys.exit(1)

    shuffle(users)

    _logger.info("\tDone.")
    _logger.info("Generating social graph….")
    followings = _generate_social_graph(users)

    _logger.info("\tDone.")
    _logger.info("Following users….")
    for follower_id, followables in tqdm(followings.items()):
        for following_id in followables:
            follow_user(follower_id, following_id)

    _logger.info("\tDone.")
    _logger.info("Finding isolated users….")
    isolated_users = {i.id for i in users}

    for follower in users:
        if follower.id in followings:
            isolated_users.discard(follower.id)

    for follower in users:
        for following_id in followings[follower.id]:
            isolated_users.discard(following_id)

    if isolated_users:
        users_to_remove = list(isolated_users)
        shuffle(users_to_remove)
        _logger.info(
            "\tFound %d isolated users. Deleting excess….", len(users_to_remove)
        )

        for user_id in tqdm(users_to_remove[USERS_MAX_ISOLATED:]):
            with suppress(DbUserNotFoundError):
                delete_user(user_id)

    _logger.info("\tDone.")
    _logger.info("Retrieving user list… (again).")
    users = get_all_users().root

    if not users:
        _logger.critical("There were no users, somehow.")
        sys.exit(1)

    shuffle(users)

    _logger.info("\tDone.")
    _logger.info("Creating posts and comments….")
    for post_author in tqdm(users):
        if random() < USER_NO_POST_ODDS:  # noqa: S311
            continue

        for _ in range(_randint_norm(USER_MIN_POSTS, USER_MAX_POSTS)):
            post_id = create_post(
                author_id=post_author.id,
                content=faker.text(),
            ).id

            if random() < POST_NO_COMMENT_ODDS:  # noqa: S311
                continue

            for comment_author in sample(
                users,
                _randint_norm(POST_MIN_COMMENTS, POST_MAX_COMMENTS),
            ):
                create_comment(
                    author_id=comment_author.id,
                    post_id=post_id,
                    content=faker.text(),
                )

    _logger.info("\tDone.")


if __name__ == "__main__":
    populate()
