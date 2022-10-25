import sys
import pathlib

from . import logger
from . import get_repo_dirs
from . import get_root_commits


def main() -> None:
    try:
        logger.init_logger(True)

        base_dir = pathlib.Path(sys.argv[1])
        repo_dirs = get_repo_dirs.get_repo_dirs(base_dir)
        repo_infos = (
            get_root_commits.get_root_commits(repo_dir)
            for repo_dir in repo_dirs
        )
        nonempty_repo_infos = (
            repo_info for repo_info in repo_infos if not repo_info.is_empty_repo
        )
        for repo_info in nonempty_repo_infos:
            logger.get_logger().debug(repo_info)
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")  # output a line break after the ^C symbol in a terminal
        sys.exit(1)
