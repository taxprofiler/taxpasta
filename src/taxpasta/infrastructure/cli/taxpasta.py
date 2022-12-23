# Copyright (c) 2022 Moritz E. Beber
# Copyright (c) 2022 Maxime Borry
# Copyright (c) 2022 James A. Fellows Yates
# Copyright (c) 2022 Sofia Stamouli.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a command-line interface (CLI) for taxpasta functionality."""


import logging
from enum import Enum, unique
from typing import Optional

import typer

import taxpasta


logger = logging.getLogger("taxpasta")


@unique
class LogLevel(str, Enum):
    """Define the choices for the log level option."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


app = typer.Typer(
    help="TAXonomic Profile Aggregation and STAndardisation",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(is_set: bool) -> None:
    """
    Print the tool version if desired.

    Args:
        is_set: Whether the version was requested as a command line option.

    Raises:
        Exit: With default code 0 to signal normal program end.

    """
    if is_set:
        print(taxpasta.__version__)
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def initialize(
    context: typer.Context,
    version: Optional[bool] = typer.Option(  # noqa: B008
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print only the current tool version and exit.",
    ),
    log_level: LogLevel = typer.Option(  # noqa: B008
        LogLevel.INFO.name,
        "--log-level",
        "-l",
        case_sensitive=False,
        help="Set the desired log level.",
    ),
):
    """Initialize logging and rich printing if available."""
    try:
        from rich.logging import RichHandler

        logging.basicConfig(
            level=log_level.name,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[typer])],
        )
    except ModuleNotFoundError:
        logging.basicConfig(level=log_level.name, format="[%(levelname)s] %(message)s")
