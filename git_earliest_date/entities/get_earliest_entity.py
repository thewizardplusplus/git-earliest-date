import datetime

from . import repo
from . import person
from . import commit


def get_earliest_repo(
    repos: repo.RepoInfoSequence,
    datetime_kind: person.PersonKind,
) -> repo.RepoInfo | None:
    def _repo_key(repo: repo.RepoInfo) -> datetime.datetime:
        earliest_root_commit = repo.get_earliest_root_commit(datetime_kind)
        assert earliest_root_commit is not None

        return earliest_root_commit.get_datetime(datetime_kind)

    nonempty_repos = _filter_nonempty_repos(repos)
    # without a separate variable, the mypy tool infers the wrong type
    earliest_repo = min(nonempty_repos, key=_repo_key, default=None)
    return earliest_repo


def get_earliest_commit(
    commits: commit.CommitInfoSequence,
    datetime_kind: person.PersonKind,
) -> commit.CommitInfo | None:
    def _commit_key(commit: commit.CommitInfo) -> datetime.datetime:
        return commit.get_datetime(datetime_kind)

    # without a separate variable, the mypy tool infers the wrong type
    earliest_commit = min(commits, key=_commit_key, default=None)
    return earliest_commit


def _filter_nonempty_repos(
    repos: repo.RepoInfoSequence,
) -> repo.RepoInfoSequence:
    yield from (repo for repo in repos if not repo.is_empty_repo)
