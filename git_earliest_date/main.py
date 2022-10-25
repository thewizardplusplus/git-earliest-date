import sys
import pathlib

from . import logger
from . import get_repo_dirs


def main() -> None:
    try:
        logger.init_logger(True)

        base_dir = pathlib.Path(sys.argv[1])
        repo_dirs = get_repo_dirs.get_repo_dirs(base_dir)
        for repo_dir in repo_dirs:
            logger.get_logger().debug(repo_dir)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")  # output a line break after the ^C symbol in a terminal
        sys.exit(1)
