import typing
import datetime

from . import entities


RepoInfoSequence = typing.Iterator[entities.RepoInfo]
CommitInfoSequence = typing.Iterator[entities.CommitInfo]


def get_earliest_repo(
    repos: RepoInfoSequence,
    datetime_kind: entities.PersonKind,
) -> entities.RepoInfo:
    def _repo_key(repo: entities.RepoInfo) -> datetime.datetime:
        earliest_root_commit = repo.get_earliest_root_commit(datetime_kind)
        return earliest_root_commit.get_datetime(datetime_kind)

    nonempty_repos = _filter_nonempty_repos(repos)
    earliest_repo = min(nonempty_repos, key=_repo_key, default=None)
    if earliest_repo is None:
        raise RuntimeError("the repo sequence is empty")

    return earliest_repo


def get_earliest_commit(
    commits: CommitInfoSequence,
    datetime_kind: entities.PersonKind,
) -> entities.CommitInfo:
    def _commit_key(commit: entities.CommitInfo) -> datetime.datetime:
        return commit.get_datetime(datetime_kind)

    earliest_commit = min(commits, key=_commit_key, default=None)
    if earliest_commit is None:
        raise RuntimeError("the commit sequence is empty")

    return earliest_commit


def _filter_nonempty_repos(repos: RepoInfoSequence) -> RepoInfoSequence:
    yield from (repo for repo in repos if not repo.is_empty_repo)
