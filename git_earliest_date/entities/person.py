from __future__ import annotations
import enum
import dataclasses

import dataclasses_json
import git.util


@enum.unique
class PersonKind(enum.Enum):
    AUTHOR = enum.auto()
    COMMITTER = enum.auto()


@dataclasses.dataclass
class PersonInfo(dataclasses_json.DataClassJsonMixin):
    name: str | None
    email: str | None

    @classmethod
    def from_actor(cls, actor: git.util.Actor) -> PersonInfo:
        return PersonInfo(actor.name, actor.email)
