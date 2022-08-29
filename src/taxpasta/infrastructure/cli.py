# Copyright (c) 2022, Moritz E. Beber, Maxime Borry, Jianhong Ou, Sofia Stamouli.
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


from enum import Enum, unique
from pathlib import Path
from typing import List, Optional

import typer

from taxpasta.application.sample_merging_application import SampleMergingApplication


@unique
class SupportedProfiler(Enum):

    kraken2 = "kraken2"
    bracken = "bracken"


@unique
class SupportedOutputFormat(Enum):

    TSV = "TSV"
    CSV = "CSV"
    ODS = "ODS"
    excel = "excel"
    arrow = "arrow"


app = typer.Typer(
    help="TAXonomic Profile Aggregation and STAndardisation",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(is_set: bool) -> None:
    if is_set:
        import taxpasta._version

        get_versions = getattr(taxpasta._version, "get_versions", None)

        if get_versions:
            print(get_versions().get("version", "undefined"))
        else:
            print("undefined")
        typer.Exit()


@app.callback(invoke_without_command=True)
def initialize(
    context: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    """Initialize logging and rich printing if available."""


@app.command()
def consensus():
    raise NotImplementedError("Coming soon™")


@app.command()
def merge(
    profiles: List[Path] = typer.Argument(
        ...,
        metavar="PROFILE [...]",
        help="Either a single file which should be a table with two columns, the first "
        "column named 'sample' which can be any string and the second column named "
        "'profile' which "
        "must be a file path to an actual taxonomic abundance profile; or at least two "
        "file "
        "paths to profiles in which case the filenames will be parsed as sample names.",
    ),
    profiler: SupportedProfiler = typer.Option(
        ...,
        case_sensitive=False,
        help="The taxonomic profiler used. All provided profiles must come from the "
        "same tool!",
    ),
    wide_format: bool = typer.Option(
        True,
        "--wide/--long",
        help="Output merged abundance data in either wide or (tidy) long format.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="The desired output file. By default, the file extension will be used to "
        "determine the output format.",
    ),
    output_format: Optional[SupportedOutputFormat] = typer.Option(
        None,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. Will be parsed from the output file name but can be "
        "set explicitly.",
    ),
):
    if len(profiles) == 1:
        # Parse table of samples.
        pass
    else:
        # TODO: create application service registry
        # TODO: use enum to get profile reader
        pass
    samples = []
    if wide_format:
        result = SampleMergingApplication.merge_wide(samples)
    else:
        result = SampleMergingApplication.merge_long(samples)
    # TODO: Write result to output in correct format
