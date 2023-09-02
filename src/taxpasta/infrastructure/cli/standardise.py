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

from taxpasta.application import AddTaxInfoCommand, SampleHandlingApplication
from taxpasta.application.error import StandardisationError
from taxpasta.domain.service import TaxonomyService
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
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
        "determine the output format, but when setting the format explicitly using "
        "the --output-format option, automatic detection is disabled.",
        show_default=False,
    ),
    output_format: Optional[StandardProfileFileFormat] = typer.Option(  # noqa: B008
        None,
        case_sensitive=False,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. By default it will be parsed from the output file "
        "name but it can be set explicitly and will then disable the automatic "
        "detection.",
    ),
    summarise_at: Optional[str] = typer.Option(  # noqa: B008
        None,
        "--summarise-at",
        "--summarize-at",
        help="Summarise abundance profiles at higher taxonomic rank. The provided "
        "option must match a rank in the taxonomy exactly. This is akin to the clade "
        "assigned reads provided by, for example, kraken2, where the abundances of a "
        "whole taxonomic branch are assigned to a taxon at the desired rank. Please "
        "note that abundances above the selected rank are simply ignored. No attempt "
        "is made to redistribute those down to the desired rank. Some tools, like "
        "Bracken, were designed for this purpose but it doesn't seem like a problem we "
        "can generally solve here.",
    ),
    taxonomy: Optional[Path] = typer.Option(  # noqa: B008
        None,
        help="The path to a directory containing taxdump files. At least nodes.dmp and "
        "names.dmp are required. A merged.dmp file is optional.",
    ),
    add_name: bool = typer.Option(  # noqa: B008
        False,
        "--add-name",
        help="Add the taxon name to the output.",
    ),
    add_rank: bool = typer.Option(  # noqa: B008
        False,
        "--add-rank",
        help="Add the taxon rank to the output.",
    ),
    add_lineage: bool = typer.Option(  # noqa: B008
        False,
        "--add-lineage",
        help="Add the taxon's entire lineage to the output. These are taxon names "
        "separated by semi-colons.",
    ),
    add_id_lineage: bool = typer.Option(  # noqa: B008
        False,
        "--add-id-lineage",
        help="Add the taxon's entire lineage to the output. These are taxon "
        "identifiers separated by semi-colons.",
    ),
    add_rank_lineage: bool = typer.Option(  # noqa: B008
        False,
        "--add-rank-lineage",
        help="Add the taxon's entire rank lineage to the output. These are taxon "
        "ranks separated by semi-colons.",
    ),
) -> None:
    """Standardise a taxonomic profile."""
    # Perform input validation.
    valid_output_format = validate_output_format(
        output, None if output_format is None else output_format.value
    )

    taxonomy_service: Optional[TaxonomyService] = None
    if taxonomy is not None:
        from taxpasta.infrastructure.domain.service.taxopy_taxonomy_service import (
            TaxopyTaxonomyService,
        )

        taxonomy_service = TaxopyTaxonomyService.from_taxdump(taxonomy)

    try:
        tax_info_command = AddTaxInfoCommand(
            taxonomy_service=taxonomy_service,
            summarise_at=summarise_at,
            add_name=add_name,
            add_rank=add_rank,
            add_lineage=add_lineage,
            add_id_lineage=add_id_lineage,
            add_rank_lineage=add_rank_lineage,
        )
    except ValueError as exc:
        logger.critical(str(exc))
        raise typer.Exit(code=2)

    # Ensure that we can write to the output directory.
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        logger.critical("Failed to create the parent directory for the output.")
        logger.critical(str(error))
        raise typer.Exit(1)

    handling_app = SampleHandlingApplication(
        profile_reader=ApplicationServiceRegistry.profile_reader(profiler),
        profile_standardiser=ApplicationServiceRegistry.profile_standardisation_service(
            profiler
        ),
        taxonomy_service=taxonomy_service,
    )
    try:
        sample = handling_app.etl_sample(profile.stem, profile)
    except StandardisationError as error:
        logger.debug("", exc_info=error)
        logger.critical(
            "Error in sample '%s' with profile '%s'.", error.sample, error.profile
        )
        logger.critical(error.message)
        raise typer.Exit(code=1)

    if summarise_at:
        try:
            sample = handling_app.summarise_sample(sample, summarise_at)
        except ValueError as error:
            logger.debug("", exc_info=error)
            logger.critical("Error in sample '%s'.", sample.name)
            logger.critical(str(error))
            raise typer.Exit(code=1)

    result = tax_info_command.execute(sample)

    logger.info("Write result to '%s'.", str(output))
    writer = ApplicationServiceRegistry.standard_profile_writer(valid_output_format)
    try:
        writer.write(result.profile, output)
    except OSError as error:
        logger.critical("Failed to write the output result.")
        logger.critical(str(error))
        raise typer.Exit(1)
