import typing
import pathlib
import datetime
import collections.abc
import dataclasses

import dataclasses_json
from dataclasses_json.core import Json


CustomJSONField: typing.TypeAlias = (
    None
    | dataclasses_json.DataClassJsonMixin
    | collections.abc.Collection[dataclasses_json.DataClassJsonMixin]
    | collections.abc.Mapping[typing.Any, dataclasses_json.DataClassJsonMixin]
)

_T = typing.TypeVar("_T")


# the actual return type is `dataclasses.Field[pathlib.Path]`;
# for an explanation, see the `_field_with_json_encoder()` function below
def path_field() -> pathlib.Path:
    def _path_encoder(path: pathlib.Path) -> Json:
        return str(path)

    return _field_with_json_encoder(_path_encoder)


# the actual return type is `dataclasses.Field[datetime.datetime]`;
# for an explanation, see the `_field_with_json_encoder()` function below
def datetime_field() -> datetime.datetime:
    def _datetime_encoder(datetime: datetime.datetime) -> Json:
        return datetime.isoformat(timespec="microseconds")

    return _field_with_json_encoder(_datetime_encoder)


# the actual return type is `dataclasses.Field[CustomJSONField]`;
# for an explanation, see the `_field_with_json_encoder()` function below
def custom_json_field() -> CustomJSONField:
    def _custom_json_field_encoder(value: CustomJSONField) -> Json:
        match value:
            case collections.abc.Mapping():
                return {
                    item_key: item_value.to_dict()
                    for item_key, item_value in value.items()
                }
            case collections.abc.Collection():
                return [item.to_dict() for item in value]
            case dataclasses_json.DataClassJsonMixin():
                return value.to_dict()
            case _:
                return None

    return _field_with_json_encoder(_custom_json_field_encoder)


# the actual return type is "dataclasses.Field[_T]", but I want to help
# type checkers to understand the magic that happens at runtime;
# see also https://github.com/python/typeshed/blob/7dd4d0882da704afd6bec77aca99c88377eef742/stdlib/3.7/dataclasses.pyi#L34
def _field_with_json_encoder(json_encoder: typing.Callable[[_T], Json]) -> _T:
    json_config = dataclasses_json.config(encoder=json_encoder)
    return typing.cast(_T, dataclasses.field(metadata=json_config))
