import sys
import pathlib
import itertools

from . import logger
from . import get_repo_dirs
from . import get_root_commits
from . import entities
from . import get_earliest_entity


def main() -> None:
    try:
        logger.init_logger(True)

        base_dir = pathlib.Path(sys.argv[1])
        repo_dirs = get_repo_dirs.get_repo_dirs(base_dir)
        repo_infos = (
            get_root_commits.get_root_commits(repo_dir)
            for repo_dir in repo_dirs
        )
        repo_infos_1, repo_infos_2 = itertools.tee(repo_infos, 2)

        for repo_info in repo_infos_1:
            logger.get_logger().debug(repo_info.to_json(ensure_ascii=False))

        earliest_repo = get_earliest_entity.get_earliest_repo(
            repo_infos_2,
            entities.PersonKind.AUTHOR,
        )
        logger.get_logger().debug(earliest_repo.to_json(ensure_ascii=False))
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")  # output a line break after the ^C symbol in a terminal
        sys.exit(1)
