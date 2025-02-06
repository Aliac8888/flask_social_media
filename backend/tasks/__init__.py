"""Prepare the python path for other scripts."""

from logging import DEBUG, INFO, basicConfig
from os import chdir, getenv
from pathlib import Path
from sys import path

root = Path(__file__).parent.parent
"""Backend root directory."""

# Note: This will break relative paths in argv if user was not in the working
# directory already.
chdir(root)

# See https://stackoverflow.com/questions/14132789
path.append(str(root))

# Logger does not log lower than `WARNING` by default. The default format is
# also not pleasant to look at.
basicConfig(
    level=DEBUG if getenv("SOCIAL_BE_DEBUG") else INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
)
