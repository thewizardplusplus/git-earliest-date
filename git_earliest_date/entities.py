from __future__ import annotations
import dataclasses
import datetime
import pathlib
import enum
import typing

import dataclasses_json
import git
import termcolor

from . import fields


JSONObject = dict[str, dataclasses_json.core.Json]


@dataclasses.dataclass
class RepoInfoGroup(dataclasses_json.DataClassJsonMixin):
    repos: list[RepoInfo]

    @property
    def is_empty(self) -> bool:
        return len(self.repos) == 0

    def get_earliest_repo(self, datetime_kind: PersonKind) -> RepoInfo:
        # I use a local import because of a circular import
        from . import get_earliest_entity

        return get_earliest_entity.get_earliest_repo(
            iter(self.repos),
            datetime_kind,
        )

    # override the method in order to add computable properties to JSON
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)

        # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
        data["is_empty"] = self.is_empty

        self._add_earliest_repo_to_dict(data, PersonKind.AUTHOR)
        self._add_earliest_repo_to_dict(data, PersonKind.COMMITTER)

        return data

    def _add_earliest_repo_to_dict(
        self,
        data: JSONObject,
        datetime_kind: PersonKind,
    ) -> None:
        key = datetime_kind.name.lower() + "_earliest_repo"
        data[key] = (
            self.get_earliest_repo(datetime_kind).to_dict()
            if not self.is_empty
            else None
        )


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
            iter(self.root_commits),
            datetime_kind,
        )

    # override the method in order to add computable properties to JSON
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)

        # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
        data["is_empty_repo"] = self.is_empty_repo

        self._add_earliest_root_commit_to_dict(data, PersonKind.AUTHOR)
        self._add_earliest_root_commit_to_dict(data, PersonKind.COMMITTER)

        return data

    def _add_earliest_root_commit_to_dict(
        self,
        data: JSONObject,
        datetime_kind: PersonKind,
    ) -> None:
        key = datetime_kind.name.lower() + "_earliest_root_commit"
        data[key] = (
            self.get_earliest_root_commit(datetime_kind).to_dict()
            if not self.is_empty_repo
            else None
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
        return self._get_attribute_by_kind(kind)

    def get_datetime(self, kind: PersonKind) -> datetime.datetime:
        return self._get_attribute_by_kind(kind, suffix="_datetime")

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

    def _get_attribute_by_kind(
        self,
        kind: PersonKind,
        *,
        suffix: str = "",
    ) -> typing.Any:
        name = kind.name.lower() + suffix
        return getattr(self, name)


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
