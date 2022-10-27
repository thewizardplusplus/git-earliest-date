import typing
import datetime

from . import entities


def get_earliest_repo(
    repos: typing.Iterable[entities.RepoInfo],
    datetime_kind: entities.PersonKind,
) -> entities.RepoInfo:
    def _repo_key(repo: entities.RepoInfo) -> datetime.datetime:
        earliest_root_commit = repo.get_earliest_root_commit(datetime_kind)
        return earliest_root_commit.get_datetime(datetime_kind)

    earliest_repo = min(repos, key=_repo_key, default=None)
    if earliest_repo is None:
        raise RuntimeError("the repo sequence is empty")

    return earliest_repo


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
