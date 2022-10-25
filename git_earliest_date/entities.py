from __future__ import annotations
import dataclasses
import datetime
import pathlib

import git
import termcolor


@dataclasses.dataclass
class RepoInfo:
    repo_dir: pathlib.Path
    root_commits: list[CommitInfo]

    @property
    def is_empty_repo(self) -> bool:
        return len(self.root_commits) == 0


@dataclasses.dataclass
class CommitInfo:
    hash: str
    author: PersonInfo
    author_datetime: datetime.datetime
    committer: PersonInfo
    committer_datetime: datetime.datetime
    message: str

    @classmethod
    def _from_commit(cls, commit: git.objects.commit.Commit) -> CommitInfo:
        hash = commit.binsha.hex()
        author = PersonInfo._from_actor(commit.author)
        committer = PersonInfo._from_actor(commit.committer)
        message = _get_commit_message(commit)

        return CommitInfo(
            hash,
            author,
            commit.authored_datetime,
            committer,
            commit.committed_datetime,
            message,
        )


@dataclasses.dataclass
class PersonInfo:
    name: str | None
    email: str | None

    @classmethod
    def _from_actor(cls, actor: git.util.Actor) -> PersonInfo:
        return PersonInfo(actor.name, actor.email)


def _get_commit_message(commit: git.objects.commit.Commit) -> str:
    if isinstance(commit.message, str):
        return commit.message
    elif isinstance(commit.message, bytes):
        return commit.message.decode(commit.encoding)
    else:
        formatted_message_type = termcolor.colored(type(commit.message), "red")
        raise RuntimeError(
            "the commit message has "
            + f"an unexpected type {formatted_message_type}",
        )
