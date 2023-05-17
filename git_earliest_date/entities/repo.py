import typing
import abc
import dataclasses
import pathlib

import dataclasses_json
from dataclasses_json.core import Json

from . import fields
from . import commit
from . import person


JSONObject: typing.TypeAlias = dict[str, Json]


class BaseRepoInfo(dataclasses_json.DataClassJsonMixin):
    @property
    @abc.abstractmethod
    def is_empty_repo(self) -> bool:
        ...

    # override the method in order to add computable properties to JSON
    # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)
        data["is_empty_repo"] = self.is_empty_repo

        return data


@dataclasses.dataclass
class SimplifiedRepoInfo(BaseRepoInfo):
    repo_dir: pathlib.Path = fields.path_field()
    earliest_root_commit: commit.SimplifiedCommitInfo | None  # type: ignore[misc]

    @property
    def is_empty_repo(self) -> bool:
        return self.earliest_root_commit is None


@dataclasses.dataclass
class RepoInfo(BaseRepoInfo):
    repo_dir: pathlib.Path = fields.path_field()
    root_commits: list[commit.CommitInfo]  # type: ignore[misc]

    @property
    def is_empty_repo(self) -> bool:
        return len(self.root_commits) == 0

    @property
    def author_earliest_root_commit(self) -> commit.CommitInfo | None:
        return self.get_earliest_root_commit(person.PersonKind.AUTHOR)

    @property
    def committer_earliest_root_commit(self) -> commit.CommitInfo | None:
        return self.get_earliest_root_commit(person.PersonKind.COMMITTER)

    def get_earliest_root_commit(
        self,
        datetime_kind: person.PersonKind,
    ) -> commit.CommitInfo | None:
        # I use a local import because of a circular import
        from . import get_earliest_entity

        return get_earliest_entity.get_earliest_commit(
            iter(self.root_commits),
            datetime_kind,
        )

    def get_simplified_version(
        self,
        kind: person.PersonKind,
    ) -> SimplifiedRepoInfo:
        earliest_root_commit = self.get_earliest_root_commit(kind)
        if earliest_root_commit is None:
            return SimplifiedRepoInfo(self.repo_dir, None)

        return SimplifiedRepoInfo(
            self.repo_dir,
            earliest_root_commit.get_simplified_version(kind),
        )

    # override the method in order to add computable properties to JSON
    # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)
        data["author_earliest_root_commit"] = _to_dict_or_none(
            self.author_earliest_root_commit,
        )
        data["committer_earliest_root_commit"] = _to_dict_or_none(
            self.committer_earliest_root_commit,
        )

        return data


RepoInfoSequence: typing.TypeAlias = typing.Iterator[RepoInfo]


class BaseRepoInfoGroup(dataclasses_json.DataClassJsonMixin):
    @property
    @abc.abstractmethod
    def is_empty(self) -> bool:
        ...

    # override the method in order to add computable properties to JSON
    # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)
        data["is_empty"] = self.is_empty

        return data


@dataclasses.dataclass
class SimplifiedRepoInfoGroup(BaseRepoInfoGroup):
    earliest_repo: SimplifiedRepoInfo | None = typing.cast(
        SimplifiedRepoInfo | None,
        fields.custom_json_field(),
    )

    @property
    def is_empty(self) -> bool:
        return self.earliest_repo is None


@dataclasses.dataclass
class RepoInfoGroup(BaseRepoInfoGroup):
    repos: list[RepoInfo] = typing.cast(
        list[RepoInfo],
        fields.custom_json_field(),
    )

    @property
    def is_empty(self) -> bool:
        return len(self.repos) == 0

    @property
    def author_earliest_repo(self) -> RepoInfo | None:
        return self.get_earliest_repo(person.PersonKind.AUTHOR)

    @property
    def committer_earliest_repo(self) -> RepoInfo | None:
        return self.get_earliest_repo(person.PersonKind.COMMITTER)

    def get_earliest_repo(
        self,
        datetime_kind: person.PersonKind,
    ) -> RepoInfo | None:
        # I use a local import because of a circular import
        from . import get_earliest_entity

        return get_earliest_entity.get_earliest_repo(
            iter(self.repos),
            datetime_kind,
        )

    def get_simplified_version(
        self,
        kind: person.PersonKind,
    ) -> SimplifiedRepoInfoGroup:
        earliest_repo = self.get_earliest_repo(kind)
        if earliest_repo is None:
            return SimplifiedRepoInfoGroup(None)

        return SimplifiedRepoInfoGroup(
            earliest_repo.get_simplified_version(kind),
        )

    # override the method in order to add computable properties to JSON
    # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)
        data["author_earliest_repo"] = _to_dict_or_none(
            self.author_earliest_repo,
        )
        data["committer_earliest_repo"] = _to_dict_or_none(
            self.committer_earliest_repo,
        )

        return data


def _to_dict_or_none(
    value: dataclasses_json.DataClassJsonMixin | None,
) -> JSONObject | None:
    return value.to_dict() if value is not None else None
