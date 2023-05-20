import dataclasses
import pathlib
import argparse

from .entities import person
from . import __version__


@dataclasses.dataclass
class OptionGroup:
    verbose: int = 0
    by_kind: person.PersonKind | None = None
    base_dirs: list[pathlib.Path] = dataclasses.field(default_factory=list)


def parse_options() -> OptionGroup:
    parser = argparse.ArgumentParser(
        prog=__package__.replace("_", "-"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-k",
        "--by-kind",
        type=_parse_person_kind,
        choices=list(person.PersonKind),
        help="filter the results by person kind",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="count",
        default=0,
        help=(
            "verbose logging; can be specified several times: "
            + "the more times, the more verbose"
        ),
    )

    parser.add_argument(
        "base_dirs",
        metavar="base-dirs",
        type=pathlib.Path,
        nargs="*",
        default=[pathlib.Path(".")],
        help="a list of base directories with repositories",
    )

    return parser.parse_args(namespace=OptionGroup())


def _parse_person_kind(kind_as_str: str) -> person.PersonKind:
    try:
        return person.PersonKind[kind_as_str.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(f"unknown person kind {kind_as_str!r}")
