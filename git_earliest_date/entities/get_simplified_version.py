import typing

from . import person


class DataClassJSONProtocol(typing.Protocol):
    def to_json(
        self,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        indent: int | str | None = None,
        # package `dataclasses_json` contains errors in the type hints here,
        # so I have to make them too, to make the protocol work
        separators: tuple[str, str] = None,  # type: ignore[assignment]
        default: typing.Callable[[typing.Any], typing.Any] = None,  # type: ignore[assignment]
        sort_keys: bool = False,
        **kw: typing.Any,
    ) -> str:
        ...


class SupportsSimplifying(typing.Protocol):
    def get_simplified_version(
        self,
        kind: person.PersonKind,
    ) -> DataClassJSONProtocol:
        ...


# TODO: replace to `Intersection[dataclasses_json.DataClassJsonMixin, SupportsSimplifying]`
# after fixing issue https://github.com/python/typing/issues/213
class DataClassJSONSupportingSimplifying(
    DataClassJSONProtocol,
    SupportsSimplifying,
    typing.Protocol,
):
    ...


def get_simplified_version(
    data: DataClassJSONSupportingSimplifying,
    kind: person.PersonKind | None,
) -> DataClassJSONProtocol:
    return data.get_simplified_version(kind) if kind is not None else data
