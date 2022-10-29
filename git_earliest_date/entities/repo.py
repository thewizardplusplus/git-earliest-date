import typing
import dataclasses
import pathlib

import dataclasses_json

from . import fields
from . import commit
from . import person


JSONObject: typing.TypeAlias = dict[str, dataclasses_json.core.Json]


@dataclasses.dataclass
class RepoInfo(dataclasses_json.DataClassJsonMixin):
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

    # override the method in order to add computable properties to JSON
    # TODO: remove after fixing issue https://github.com/lidatong/dataclasses-json/issues/176
    def to_dict(self, encode_json: bool = False) -> JSONObject:
        data = super().to_dict(encode_json=encode_json)

        data["is_empty_repo"] = self.is_empty_repo
        data["author_earliest_root_commit"] = _to_dict_or_none(
            self.author_earliest_root_commit,
        )
        data["committer_earliest_root_commit"] = _to_dict_or_none(
            self.committer_earliest_root_commit,
        )

        return data


RepoInfoSequence: typing.TypeAlias = typing.Iterator[RepoInfo]


@dataclasses.dataclass
class RepoInfoGroup(dataclasses_json.DataClassJsonMixin):
    repos: list[RepoInfo]

    @property
    def is_empty(self) -> bool:
        return len(self.repos) == 0

    def get_earliest_repo(self, datetime_kind: person.PersonKind) -> RepoInfo:
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

        self._add_earliest_repo_to_dict(data, person.PersonKind.AUTHOR)
        self._add_earliest_repo_to_dict(data, person.PersonKind.COMMITTER)

        return data

    def _add_earliest_repo_to_dict(
        self,
        data: JSONObject,
        datetime_kind: person.PersonKind,
    ) -> None:
        key = datetime_kind.name.lower() + "_earliest_repo"
        data[key] = (
            self.get_earliest_repo(datetime_kind).to_dict()
            if not self.is_empty
            else None
        )


def _to_dict_or_none(
    value: dataclasses_json.DataClassJsonMixin | None,
) -> JSONObject | None:
    return value.to_dict() if value is not None else None
