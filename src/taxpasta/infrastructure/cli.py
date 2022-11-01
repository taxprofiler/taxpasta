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


import logging
from enum import Enum, unique
from pathlib import Path
from typing import List, Optional, Union

import pandera.errors
import typer
from pandera.typing import DataFrame

import taxpasta
from taxpasta.application import SampleMergingApplication

from .application import (
    ApplicationServiceRegistry,
    ObservationMatrixFileFormat,
    SampleSheet,
    SupportedProfiler,
    TableReaderFileFormat,
    TidyObservationTableFileFormat,
)


logger = logging.getLogger("taxpasta")


@unique
class LogLevel(str, Enum):
    """Define the choices for the log level option."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def validate_observation_matrix_format(
    output: Path, output_format: Optional[str]
) -> ObservationMatrixFileFormat:
    """
    Detect the output format if it isn't given.

    Args:
        output: Path for the output.
        output_format: The selected file format if any.

    Returns:
        The validated output file format.

    """
    if output_format is None:
        try:
            result = ObservationMatrixFileFormat.guess_format(output)
        except ValueError as error:
            logger.error(
                "%s\nPlease rename the output or set the --output-format explicitly.",
                error.args[0],
            )
            typer.Exit(2)
    else:
        result = ObservationMatrixFileFormat(output_format)
    try:
        ObservationMatrixFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.error(str(error))
        typer.Exit(1)
    return result


def validate_tidy_observation_table_format(
    output: Path, output_format: Optional[str]
) -> TidyObservationTableFileFormat:
    """
    Detect the output format if it isn't given.

    Args:
        output: Path for the output.
        output_format: The selected file format if any.

    Returns:
        The validated output file format.

    """
    if output_format is None:
        try:
            result = TidyObservationTableFileFormat.guess_format(output)
        except ValueError as error:
            logger.error(
                "%s\nPlease rename the output or set the --output-format explicitly.",
                error.args[0],
            )
            typer.Exit(2)
    else:
        result = TidyObservationTableFileFormat(output_format)
    try:
        TidyObservationTableFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.error(str(error))
        typer.Exit(1)
    return result


def validate_sample_format(
    sample_sheet: Path, sample_format: Optional[TableReaderFileFormat]
) -> TableReaderFileFormat:
    """
    Detect the sample sheet format if it isn't given.

    Args:
        sample_sheet: Path to the sample sheet.
        sample_format: The selected file format if any.

    Returns:
        The validated sample sheet format.

    """
    if sample_format is None:
        try:
            result = TableReaderFileFormat.guess_format(sample_sheet)
        except ValueError as error:
            logger.error(
                "%s\nPlease rename the sample sheet or set the --sample-format "
                "explicitly.",
                error.args[0],
            )
            typer.Exit(2)
    else:
        result = sample_format
    try:
        TableReaderFileFormat.check_dependencies(result)
    except ImportError as error:
        logger.debug("", exc_info=error)
        logger.error(str(error))
        typer.Exit(1)
    return result


def read_sample_sheet(
    sample_sheet: Path, sample_format: TableReaderFileFormat
) -> DataFrame[SampleSheet]:
    """
    Extract and validate the sample sheet.

    Args:
        sample_sheet: Path to the sample sheet.
        sample_format: The determined file format.

    Returns:
        A pandas data frame in the form of a sample sheet.

    """
    reader = ApplicationServiceRegistry.table_reader(sample_format)
    result = reader.read(sample_sheet)
    try:
        SampleSheet.validate(result, lazy=True)
    except pandera.errors.SchemaErrors as error:
        logger.error(str(error))
        typer.Exit(1)
    return result


app = typer.Typer(
    help="TAXonomic Profile Aggregation and STAndardisation",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(is_set: bool) -> None:
    """
    Print the tool version if desired.

    Args:
        is_set: Whether the version was requested as a command line option.

    """
    if is_set:
        print(taxpasta.__version__)
        typer.Exit()


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


@app.command()
def consensus():
    """Form a consensus for the same sample but from different taxonomic profiles."""
    raise NotImplementedError("Coming soon™")


@app.command()
def merge(
    profiles: Optional[List[Path]] = typer.Argument(  # noqa: B008
        None,
        metavar="[PROFILE1 PROFILE2 [...]]",
        help="Two or more files containing taxonomic profiles. Required unless there is"
        " a sample sheet. Filenames will be parsed as sample names.",
    ),
    profiler: SupportedProfiler = typer.Option(  # noqa: B008
        ...,
        "--profiler",
        "-p",
        case_sensitive=False,
        help="The taxonomic profiler used. All provided profiles must come from the "
        "same tool!",
    ),
    sample_sheet: Optional[Path] = typer.Option(  # noqa: B008
        None,
        "--samplesheet",
        "-s",
        help="A table with a header and two columns: the first "
        "column named 'sample' which can be any string and the second column named "
        "'profile' which "
        "must be a file path to an actual taxonomic abundance profile. If this option "
        "is provided, any arguments are ignored.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    samplesheet_format: Optional[TableReaderFileFormat] = typer.Option(  # noqa: B008
        None,
        case_sensitive=False,
        help="The file format of the sample sheet. Depending on the choice, additional "
        "package dependencies may apply. Will be parsed from the sample sheet "
        "file name but can be set explicitly.",
    ),
    wide_format: bool = typer.Option(  # noqa: B008
        True,
        "--wide/--long",
        help="Output merged abundance data in either wide or (tidy) long format. "
        "Ignored when the desired output format is BIOM.",
    ),
    output: Path = typer.Option(  # noqa: B008
        ...,
        "--output",
        "-o",
        help="The desired output file. By default, the file extension will be used to "
        "determine the output format.",
    ),
    output_format: Optional[ObservationMatrixFileFormat] = typer.Option(  # noqa: B008
        None,
        case_sensitive=False,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. Will be parsed from the output file name but can be "
        "set explicitly.",
    ),
):
    """Merge two or more taxonomic profiles into a single table."""
    # Perform input validation.
    valid_output_format: Union[
        TidyObservationTableFileFormat, ObservationMatrixFileFormat
    ]
    # When a BIOM output format is chosen, the result can only be a wide format BIOM.
    if output.suffix.lower() == ".biom" or (
        output_format is not None and output_format is ObservationMatrixFileFormat.BIOM
    ):
        valid_output_format = ObservationMatrixFileFormat.BIOM
        wide_format = True
    else:
        if wide_format:
            valid_output_format = validate_observation_matrix_format(
                output, None if output_format is None else output_format.value
            )
        else:
            valid_output_format = validate_tidy_observation_table_format(
                output, None if output_format is None else output_format.value
            )
    # Ensure that we can write to the output directory.
    output.parent.mkdir(parents=True, exist_ok=True)

    # Extract and transform sample data.
    if sample_sheet is not None:
        valid_sample_format = validate_sample_format(sample_sheet, samplesheet_format)
        logger.info("Read sample sheet from '%s'.", str(sample_sheet))
        sheet = read_sample_sheet(sample_sheet, valid_sample_format)
        data = [(row.sample, row.profile) for row in sheet.itertuples(index=False)]
    else:
        if not profiles:
            logger.critical(
                "Neither a sample sheet nor any profiles were provided. Please adjust "
                "the command."
            )
            return 2
        elif len(profiles) == 1:
            logger.critical(
                "Only a single profile was provided. Please provide at least two."
            )
            return 2
        # Parse sample names from file names.
        data = [(prof.stem, prof) for prof in profiles]

    merging_app = SampleMergingApplication(
        profile_reader=ApplicationServiceRegistry.profile_reader(profiler),
        profile_standardiser=ApplicationServiceRegistry.profile_standardisation_service(
            profiler
        ),
    )
    try:
        result = merging_app.run(data, wide_format)
    except pandera.errors.SchemaErrors as errors:
        logger.error(errors.failure_cases)
        return 1

    logger.info("Write result to '%s'.", str(output))
    if wide_format:
        assert isinstance(  # nosec assert_used
            valid_output_format, ObservationMatrixFileFormat
        )
        writer = ApplicationServiceRegistry.observation_matrix_writer(
            valid_output_format
        )
    else:
        assert isinstance(  # nosec assert_used
            valid_output_format, TidyObservationTableFileFormat
        )
        writer = ApplicationServiceRegistry.tidy_observation_table_writer(
            valid_output_format  # type: ignore
        )
    writer.write(result, output)
