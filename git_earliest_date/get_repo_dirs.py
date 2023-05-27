import typing
import pathlib
import enum
import itertools

import termcolor

from . import logger


PathSequence: typing.TypeAlias = typing.Iterator[pathlib.Path]


@enum.unique
class _RepoStatus(enum.Enum):
    IS_NOT_REPO = enum.auto()
    IS_REPO = enum.auto()


def get_repo_dirs(base_dir_sequence: PathSequence) -> PathSequence:
    return (
        repo_dir
        for base_dir in base_dir_sequence
        for repo_dir in _get_repo_dirs_for_one_base(base_dir)
    )


def _get_repo_dirs_for_one_base(base_dir: pathlib.Path) -> PathSequence:
    formatted_base_dir = termcolor.colored(str(base_dir), "yellow")
    logger.get_logger().debug(f"was specified base dir {formatted_base_dir}")

    if not base_dir.is_dir():
        raise RuntimeError(f"path {formatted_base_dir} is not a dir")

    if _get_repo_status(base_dir) == _RepoStatus.IS_REPO:
        logger.get_logger().warn(f"path {formatted_base_dir} is a repo itself")

        yield base_dir
        return

    dir_sequence = _get_subdirs(base_dir)
    dir_sequence_1, dir_sequence_2 = itertools.tee(dir_sequence, 2)

    yield from _select_dirs_by_repo_status(dir_sequence_1, _RepoStatus.IS_REPO)

    not_repo_dir_sequence = _select_dirs_by_repo_status(
        dir_sequence_2,
        _RepoStatus.IS_NOT_REPO,
    )
    yield from get_repo_dirs(not_repo_dir_sequence)


def _get_subdirs(base_dir: pathlib.Path) -> PathSequence:
    return (entity for entity in base_dir.iterdir() if entity.is_dir())


def _select_dirs_by_repo_status(
    dir_sequence: PathSequence,
    repo_status: _RepoStatus,
) -> PathSequence:
    return (dir for dir in dir_sequence if _get_repo_status(dir) == repo_status)


def _get_repo_status(dir: pathlib.Path) -> _RepoStatus:
    if (dir / ".git").exists():
        return _RepoStatus.IS_REPO

    return _RepoStatus.IS_NOT_REPO
