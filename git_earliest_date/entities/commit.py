from __future__ import annotations
import dataclasses
import datetime
import typing

import dataclasses_json
import git.objects.commit

from . import person
from . import fields


@dataclasses.dataclass
class SimplifiedCommitInfo(dataclasses_json.DataClassJsonMixin):
    hash: str
    person: person.PersonInfo
    datetime: datetime.datetime = fields.datetime_field()
    message: str  # type: ignore[misc]


@dataclasses.dataclass
class CommitInfo(dataclasses_json.DataClassJsonMixin):
    hash: str
    author: person.PersonInfo
    author_datetime: datetime.datetime = fields.datetime_field()
    committer: person.PersonInfo  # type: ignore[misc]
    committer_datetime: datetime.datetime = fields.datetime_field()
    message: str  # type: ignore[misc]

    @classmethod
    def from_commit(cls, commit: git.objects.commit.Commit) -> CommitInfo:
        hash = commit.binsha.hex()
        author = person.PersonInfo.from_actor(commit.author)
        committer = person.PersonInfo.from_actor(commit.committer)
        message = _get_commit_message(commit)

        return CommitInfo(
            hash,
            author,
            commit.authored_datetime,
            committer,
            commit.committed_datetime,
            message,
        )

    def get_person(self, kind: person.PersonKind) -> person.PersonInfo:
        return typing.cast(person.PersonInfo, self._get_attribute_by_kind(kind))

    def get_datetime(self, kind: person.PersonKind) -> datetime.datetime:
        return typing.cast(
            datetime.datetime,
            self._get_attribute_by_kind(kind, suffix="_datetime"),
        )

    def get_simplified_version(
        self,
        kind: person.PersonKind,
    ) -> SimplifiedCommitInfo:
        return SimplifiedCommitInfo(
            self.hash,
            self.get_person(kind),
            self.get_datetime(kind),
            self.message,
        )

    def _get_attribute_by_kind(
        self,
        kind: person.PersonKind,
        *,
        suffix: str = "",
    ) -> typing.Any:
        name = kind.name.lower() + suffix
        return getattr(self, name)


CommitInfoSequence: typing.TypeAlias = typing.Iterator[CommitInfo]


def _get_commit_message(commit: git.objects.commit.Commit) -> str:
    match commit.message:
        case str():
            return commit.message
        case bytes():
            return commit.message.decode(commit.encoding)
