import dataclasses
import pathlib
import argparse

from . import __version__


@dataclasses.dataclass
class OptionGroup:
    verbose: bool = False
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
        "-V",
        "--verbose",
        action="store_true",
        help="verbose logging",
    )

    parser.add_argument(
        "base_dirs",
        type=pathlib.Path,
        nargs="*",
        default=[pathlib.Path(".")],
        help="a list of base directories with repositories",
    )

    return parser.parse_args(namespace=OptionGroup())
