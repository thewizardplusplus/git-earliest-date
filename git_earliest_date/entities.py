from __future__ import annotations
import dataclasses
import datetime
import pathlib
import enum

import dataclasses_json
import git
import termcolor

from . import fields


@dataclasses.dataclass
class RepoInfo(dataclasses_json.DataClassJsonMixin):
    repo_dir: pathlib.Path = fields.path_field()
    root_commits: list[CommitInfo]  # type: ignore[misc]

    @property
    def is_empty_repo(self) -> bool:
        return len(self.root_commits) == 0

    def get_earliest_root_commit(self, datetime_kind: PersonKind) -> CommitInfo:
        # I use a local import because of a circular import
        from . import get_earliest_entity

        return get_earliest_entity.get_earliest_commit(
            self.root_commits,
            datetime_kind,
        )


@dataclasses.dataclass
class CommitInfo(dataclasses_json.DataClassJsonMixin):
    hash: str
    author: PersonInfo
    author_datetime: datetime.datetime = fields.datetime_field()
    committer: PersonInfo  # type: ignore[misc]
    committer_datetime: datetime.datetime = fields.datetime_field()
    message: str  # type: ignore[misc]

    def get_person(self, kind: PersonKind) -> PersonInfo:
        match kind:
            case PersonKind.AUTHOR:
                return self.author
            case PersonKind.COMMITTER:
                return self.committer

    def get_datetime(self, kind: PersonKind) -> datetime.datetime:
        match kind:
            case PersonKind.AUTHOR:
                return self.author_datetime
            case PersonKind.COMMITTER:
                return self.committer_datetime

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
class PersonInfo(dataclasses_json.DataClassJsonMixin):
    name: str | None
    email: str | None

    @classmethod
    def _from_actor(cls, actor: git.util.Actor) -> PersonInfo:
        return PersonInfo(actor.name, actor.email)


@enum.unique
class PersonKind(enum.Enum):
    AUTHOR = enum.auto()
    COMMITTER = enum.auto()


def _get_commit_message(commit: git.objects.commit.Commit) -> str:
    match commit.message:
        case str():
            return commit.message
        case bytes():
            return commit.message.decode(commit.encoding)
        case _:
            message_type = type(commit.message)
            formatted_message_type = termcolor.colored(message_type, "red")
            raise RuntimeError(
                "the commit message has "
                + f"an unexpected type {formatted_message_type}",
            )
