import sys
import itertools

from . import options as options_module
from . import logger
from . import get_repo_dirs
from . import get_root_commits
from .entities import get_simplified_version
from .entities import repo


def main() -> None:
    try:
        options = options_module.parse_options()
        logger.init_logger(options.verbose > 0)

        repo_dirs = get_repo_dirs.get_repo_dirs(iter(options.base_dirs))
        repo_infos = (
            get_root_commits.get_root_commits(repo_dir)
            for repo_dir in repo_dirs
        )
        repo_infos_1, repo_infos_2 = itertools.tee(repo_infos, 2)

        if options.verbose > 1:
            for repo_info in repo_infos_1:
                result = get_simplified_version.get_simplified_version(
                    repo_info,
                    options.by_kind,
                )
                logger.get_logger().debug(result.to_json(ensure_ascii=False))

        repo_info_group = repo.RepoInfoGroup(list(repo_infos_2))
        result = get_simplified_version.get_simplified_version(
            repo_info_group,
            options.by_kind,
        )
        print(result.to_json(ensure_ascii=False))
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")  # output a line break after the ^C symbol in a terminal
        sys.exit(1)
