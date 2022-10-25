import typing
import pathlib
import datetime
import dataclasses

import dataclasses_json


_T = typing.TypeVar("_T")


# the actual return type is `dataclasses.Field[pathlib.Path]`;
# for an explanation, see the `_field_with_json_encoder()` function below
def path_field() -> pathlib.Path:
    def _path_encoder(path: pathlib.Path) -> str:
        return str(path)

    return _field_with_json_encoder(_path_encoder)


# the actual return type is `dataclasses.Field[datetime.datetime]`;
# for an explanation, see the `_field_with_json_encoder()` function below
def datetime_field() -> datetime.datetime:
    def _datetime_encoder(datetime: datetime.datetime) -> str:
        return datetime.isoformat(timespec="microseconds")

    return _field_with_json_encoder(_datetime_encoder)


# the actual return type is "dataclasses.Field[_T]", but I want to help
# type checkers to understand the magic that happens at runtime;
# see also https://github.com/python/typeshed/blob/7dd4d0882da704afd6bec77aca99c88377eef742/stdlib/3.7/dataclasses.pyi#L34
def _field_with_json_encoder(json_encoder: typing.Callable[[_T], str]) -> _T:
    json_config = dataclasses_json.config(encoder=json_encoder)
    return dataclasses.field(metadata=json_config)
