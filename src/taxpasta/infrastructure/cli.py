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

import pandas as pd
import typer

from taxpasta.application import SampleMergingService
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SampleSheet,
    SupportedProfiler,
)


@unique
class SupportedOutputFormat(Enum):

    TSV = "TSV"
    CSV = "CSV"
    ODS = "ODS"
    XLSX = "XLSX"
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
        case_sensitive=False,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. Will be parsed from the output file name but can be "
        "set explicitly.",
    ),
):
    # Perform input validation.
    # Ensure that we can write to the output directory.
    output.parent.mkdir(parents=True, exist_ok=True)
    # Detect the output format if it isn't given.
    if output_format is None:
        # Set of all suffixes without the dot.
        suffixes = {suffix[1:].upper() for suffix in output.suffixes}
        # Mapping of supported output formats.
        supported_formats = {
            option.name.upper(): option for option in SupportedOutputFormat
        }
        common = suffixes.intersection(supported_formats)
        if not common:
            raise ValueError(
                f"Unrecognized output file type extension {''.join(output.suffixes)}. "
                f"Please rename the output or set the --output-format explicitly."
            )
        elif len(common) > 1:
            raise ValueError(
                f"Ambiguous output file type extension {''.join(output.suffixes)}. "
                f"Please rename the output or set the --output-format explicitly."
            )
        else:
            output_format = supported_formats[common.pop()]
    #
    reader = ApplicationServiceRegistry.profile_reader(profiler)
    standardiser = ApplicationServiceRegistry.profile_standardisation_service(profiler)
    # Extract and transform sample data.
    if len(profiles) == 1:
        # Parse sample sheet.
        sheet = pd.read_table(profiles[0], sep="\t")
        assert len(sheet) > 1, "Need at least two samples to merge any profiles."
        SampleSheet.validate(sheet)
        data = [
            (row.sample, Path(row.profile)) for row in sheet.itertuples(index=False)
        ]
    else:
        # Parse sample names from filenames.
        data = [(prof.name, prof) for prof in profiles]
    samples = [
        (name, standardiser.transform(reader.read(profile))) for name, profile in data
    ]
    if wide_format:
        result = SampleMergingService.merge_wide(samples)
    else:
        result = SampleMergingService.merge_long(samples)
    # TODO: Write result to output in correct format
    if output_format is SupportedOutputFormat.TSV:
        result.to_csv(output, sep="\t", index=False)
    elif output_format is SupportedOutputFormat.CSV:
        result.to_csv(output, index=False)
    elif output_format is SupportedOutputFormat.XLSX:
        result.to_excel(output, index=False, engine="openpyxl")
    elif output_format is SupportedOutputFormat.ODS:
        result.to_excel(output, index=False, engine="odf")
    elif output_format is SupportedOutputFormat.arrow:
        result.to_feather(output)
