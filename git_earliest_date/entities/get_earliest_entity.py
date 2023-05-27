import typing
import datetime

from . import repo
from . import person
from . import commit


_T = typing.TypeVar("_T")


# Apache License 2.0 / MIT License
# Copyright (C) 2015 Jukka Lehtosalo and contributors
# https://github.com/python/typeshed/tree/1d2ae2598b3891266b0072431c0eb7d53f167396/stdlib/_typeshed
class _SupportsDunderLT(typing.Protocol):
    def __lt__(self, __other: typing.Any) -> bool:
        ...


# Apache License 2.0 / MIT License
# Copyright (C) 2015 Jukka Lehtosalo and contributors
# https://github.com/python/typeshed/tree/1d2ae2598b3891266b0072431c0eb7d53f167396/stdlib/_typeshed
class _SupportsDunderGT(typing.Protocol):
    def __gt__(self, __other: typing.Any) -> bool:
        ...


# Apache License 2.0 / MIT License
# Copyright (C) 2015 Jukka Lehtosalo and contributors
# https://github.com/python/typeshed/tree/1d2ae2598b3891266b0072431c0eb7d53f167396/stdlib/_typeshed
_SupportsRichComparison: typing.TypeAlias = (
    _SupportsDunderLT | _SupportsDunderGT
)


def get_earliest_repo(
    repos: repo.RepoInfoSequence,
    datetime_kind: person.PersonKind,
) -> repo.RepoInfo | None:
    def _repo_key(repo: repo.RepoInfo) -> datetime.datetime:
        earliest_root_commit = repo.get_earliest_root_commit(datetime_kind)
        assert earliest_root_commit is not None

        return earliest_root_commit.get_datetime(datetime_kind)

    nonempty_repos = _filter_nonempty_repos(repos)
    return _min_or_none(nonempty_repos, key=_repo_key)


def get_earliest_commit(
    commits: commit.CommitInfoSequence,
    datetime_kind: person.PersonKind,
) -> commit.CommitInfo | None:
    def _commit_key(commit: commit.CommitInfo) -> datetime.datetime:
        return commit.get_datetime(datetime_kind)

    return _min_or_none(commits, key=_commit_key)


def _filter_nonempty_repos(
    repos: repo.RepoInfoSequence,
) -> repo.RepoInfoSequence:
    return (repo for repo in repos if not repo.is_empty_repo)


def _min_or_none(
    sequence: typing.Iterator[_T],
    *,
    key: typing.Callable[[_T], _SupportsRichComparison],
) -> _T | None:
    # without a separate variable, the mypy tool infers the wrong type
    minimum = min(sequence, key=key, default=None)
    return minimum
