import pathlib
import typing
import itertools

import termcolor

from . import logger


PathSequence = typing.Iterator[pathlib.Path]


def get_repo_dirs(base_dir: pathlib.Path) -> PathSequence:
    formatted_base_dir = termcolor.colored(str(base_dir), "yellow")
    logger.get_logger().debug(f"was specified base dir {formatted_base_dir}")

    if not base_dir.is_dir():
        raise RuntimeError(f"path {formatted_base_dir} is not a dir")

    if _is_repo_dir(base_dir):
        logger.get_logger().warn(f"path {formatted_base_dir} is a repo itself")

        yield base_dir
        return

    dir_sequence = _get_subdirs(base_dir)
    dir_sequence_1, dir_sequence_2 = itertools.tee(dir_sequence, 2)

    yield from _filter_repo_dirs(dir_sequence_1)
    yield from (
        repo_dir
        for dir in _filter_not_repo_dirs(dir_sequence_2)
        for repo_dir in get_repo_dirs(dir)
    )


def _get_subdirs(base_dir: pathlib.Path) -> PathSequence:
    yield from (entity for entity in base_dir.iterdir() if entity.is_dir())


def _filter_repo_dirs(dir_sequence: PathSequence) -> PathSequence:
    yield from (dir for dir in dir_sequence if _is_repo_dir(dir))


def _filter_not_repo_dirs(dir_sequence: PathSequence) -> PathSequence:
    yield from (dir for dir in dir_sequence if not _is_repo_dir(dir))


def _is_repo_dir(dir: pathlib.Path) -> bool:
    return (dir / ".git").exists()
