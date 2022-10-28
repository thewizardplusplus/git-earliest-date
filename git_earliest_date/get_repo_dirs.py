import pathlib
import typing
import itertools

import termcolor

from . import logger


PathSequence = typing.Iterator[pathlib.Path]


def get_repo_dirs(base_dir_sequence: PathSequence) -> PathSequence:
    yield from (
        repo_dir
        for base_dir in base_dir_sequence
        for repo_dir in _get_repo_dirs_for_one_base(base_dir)
    )


def _get_repo_dirs_for_one_base(base_dir: pathlib.Path) -> PathSequence:
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

    not_repo_dir_sequence = _filter_not_repo_dirs(dir_sequence_2)
    yield from get_repo_dirs(not_repo_dir_sequence)


def _get_subdirs(base_dir: pathlib.Path) -> PathSequence:
    yield from (entity for entity in base_dir.iterdir() if entity.is_dir())


def _filter_repo_dirs(dir_sequence: PathSequence) -> PathSequence:
    yield from (dir for dir in dir_sequence if _is_repo_dir(dir))


def _filter_not_repo_dirs(dir_sequence: PathSequence) -> PathSequence:
    yield from (dir for dir in dir_sequence if not _is_repo_dir(dir))


def _is_repo_dir(dir: pathlib.Path) -> bool:
    return (dir / ".git").exists()
