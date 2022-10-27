import typing
import datetime

from . import entities


def get_earliest_commit(
    commits: typing.Iterable[entities.CommitInfo],
    datetime_kind: entities.PersonKind,
) -> entities.CommitInfo:
    def _commit_key(commit: entities.CommitInfo) -> datetime.datetime:
        return commit.get_datetime(datetime_kind)

    earliest_commit = min(commits, key=_commit_key, default=None)
    if earliest_commit is None:
        raise RuntimeError("the commit sequence is empty")

    return earliest_commit
