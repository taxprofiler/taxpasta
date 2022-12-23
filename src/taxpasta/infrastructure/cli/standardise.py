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


"""Add the `standardize` command to the taxpasta CLI."""


import logging
from pathlib import Path
from typing import Optional, cast

import typer

from taxpasta.application.error import StandardisationError
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SampleETLApplication,
    StandardProfileFileFormat,
    SupportedProfiler,
)

from .taxpasta import app


logger = logging.getLogger(__name__)


def validate_output_format(
    output: Path, output_format: Optional[str]
) -> StandardProfileFileFormat:
    """
    Detect the output format if it isn't given.

    Args:
        output: Path for the output.
        output_format: The selected file format if any.

    Returns:
        The validated output file format.

    Raises:
        Exit: Early abortion of program when the format cannot be guessed or
            dependencies are missing.

    """
    if output_format is None:
        try:
            result = cast(
                StandardProfileFileFormat,
                StandardProfileFileFormat.guess_format(output),
            )
        except ValueError as error:
            logger.critical(str(error))
            logger.critical(
                "Please rename the output or set the '--output-format' explicitly."
            )
            raise typer.Exit(code=2)
    else:
        result = StandardProfileFileFormat(output_format)
    try:
        StandardProfileFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.critical(str(error))
        raise typer.Exit(code=1)
    return result


@app.command(
    no_args_is_help=True, help="Standardise a taxonomic profile (alias: 'standardize')."
)
@app.command("standardize", hidden=True)
def standardise(
    profile: Path = typer.Argument(  # noqa: B008
        ...,
        metavar="PROFILE",
        help="A file containing a taxonomic profile.",
        show_default=False,
    ),
    profiler: SupportedProfiler = typer.Option(  # noqa: B008
        ...,
        "--profiler",
        "-p",
        case_sensitive=False,
        help="The taxonomic profiler used.",
        show_default=False,
    ),
    output: Path = typer.Option(  # noqa: B008
        ...,
        "--output",
        "-o",
        help="The desired output file. By default, the file extension will be used to "
        "determine the output format.",
        show_default=False,
    ),
    output_format: Optional[StandardProfileFileFormat] = typer.Option(  # noqa: B008
        None,
        case_sensitive=False,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. Will be parsed from the output file name but can be "
        "set explicitly.",
    ),
):
    """Standardise a taxonomic profile."""
    # Perform input validation.
    valid_output_format = validate_output_format(
        output, None if output_format is None else output_format.value
    )
    # Ensure that we can write to the output directory.
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        logger.critical("Failed to create the parent directory for the output.")
        logger.critical(str(error))
        raise typer.Exit(1)

    sample_app = SampleETLApplication(
        profile_reader=ApplicationServiceRegistry.profile_reader(profiler),
        profile_standardiser=ApplicationServiceRegistry.profile_standardisation_service(
            profiler
        ),
    )
    try:
        result = sample_app.etl(profile)
    except StandardisationError as error:
        logger.debug("", exc_info=error)
        logger.critical(
            "Error in sample '%s' with profile '%s'.", error.sample, error.profile
        )
        logger.critical(error.message)
        raise typer.Exit(code=1)

    logger.info("Write result to '%s'.", str(output))
    writer = ApplicationServiceRegistry.standard_profile_writer(valid_output_format)
    try:
        writer.write(result.profile, output)
    except OSError as error:
        logger.critical("Failed to write the output result.")
        logger.critical(str(error))
        raise typer.Exit(1)
