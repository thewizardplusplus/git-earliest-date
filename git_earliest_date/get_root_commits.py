import pathlib

import git.repo.base
import termcolor

from .entities import repo as repo_module
from .entities import commit
from . import logger


def get_root_commits(repo_dir: pathlib.Path) -> repo_module.RepoInfo:
    formatted_repo_dir = termcolor.colored(str(repo_dir), "yellow")
    logger.get_logger().debug(f"was found repo {formatted_repo_dir}")

    repo = git.repo.base.Repo(repo_dir)
    if _is_repo_empty(repo):
        logger.get_logger().warn(f"repo {formatted_repo_dir} is empty")

        return repo_module.RepoInfo(repo_dir, [])

    absolute_repo_dir = repo_dir.resolve(strict=True)
    root_commits = _find_root_commits(repo)
    return repo_module.RepoInfo(absolute_repo_dir, root_commits)


def _is_repo_empty(repo: git.repo.base.Repo) -> bool:
    return not repo.head.is_valid()


def _find_root_commits(repo: git.repo.base.Repo) -> list[commit.CommitInfo]:
    return [
        commit.CommitInfo.from_commit(root_commit)
        for root_commit in repo.iter_commits(max_parents=0)
    ]
