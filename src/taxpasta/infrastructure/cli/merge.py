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


"""Add the `merge` command to the taxpasta CLI."""


import logging
from pathlib import Path
from typing import List, Optional, Union, cast

import pandera.errors
import typer
from pandera.typing import DataFrame

from taxpasta.application import SampleMergingApplication
from taxpasta.application.error import StandardisationError
from taxpasta.domain.service import TaxonomyService
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SampleSheet,
    SupportedProfiler,
    TableReaderFileFormat,
    TidyObservationTableFileFormat,
    WideObservationTableFileFormat,
)

from .taxpasta import app


logger = logging.getLogger(__name__)


def validate_observation_matrix_format(
    output: Path, output_format: Optional[str]
) -> WideObservationTableFileFormat:
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
                WideObservationTableFileFormat,
                WideObservationTableFileFormat.guess_format(output),
            )
        except ValueError as error:
            logger.critical(str(error))
            logger.critical(
                "Please rename the output or set the '--output-format' explicitly."
            )
            raise typer.Exit(code=2)
    else:
        result = WideObservationTableFileFormat(output_format)
    try:
        WideObservationTableFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.critical(str(error))
        raise typer.Exit(code=1)
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

    Raises:
        Exit: Early abortion of program when the format cannot be guessed or
            dependencies are missing.

    """
    if output_format is None:
        try:
            result = cast(
                TidyObservationTableFileFormat,
                TidyObservationTableFileFormat.guess_format(output),
            )
        except ValueError as error:
            logger.critical(str(error))
            logger.critical(
                "Please rename the output or set the '--output-format' explicitly."
            )
            raise typer.Exit(code=2)
    else:
        result = TidyObservationTableFileFormat(output_format)
    try:
        TidyObservationTableFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.critical(str(error))
        raise typer.Exit(code=1)
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

    Raises:
        Exit: Early abortion of program when the format cannot be guessed or
            dependencies are missing.

    """
    if sample_format is None:
        try:
            result = cast(
                TableReaderFileFormat,
                TableReaderFileFormat.guess_format(sample_sheet),
            )
        except ValueError as error:
            logger.critical(str(error))
            logger.critical(
                "Please rename the sample sheet or set the '--samplesheet-format' "
                "explicitly."
            )
            raise typer.Exit(code=2)
    else:
        result = sample_format
    try:
        TableReaderFileFormat.check_dependencies(result)
    except RuntimeError as error:
        logger.debug("", exc_info=error)
        logger.critical(str(error))
        raise typer.Exit(code=1)
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

    Raises:
        Exit: Early abortion of program when there is a schema error.

    """
    reader = ApplicationServiceRegistry.table_reader(sample_format)
    result = reader.read(sample_sheet)
    try:
        SampleSheet.validate(result, lazy=True)
    except pandera.errors.SchemaErrors as errors:
        logger.debug("", exc_info=errors)
        logger.critical("Parsing the sample sheet '%s' failed.", str(sample_sheet))
        logger.critical(errors.failure_cases)
        raise typer.Exit(code=1)
    return result


@app.command()
def merge(
    profiles: Optional[List[Path]] = typer.Argument(  # noqa: B008
        None,
        metavar="[PROFILE1 PROFILE2 [...]]",
        help="Two or more files containing taxonomic profiles. Required unless there is"
        " a sample sheet. Filenames will be parsed as sample names.",
        show_default=False,
    ),
    profiler: SupportedProfiler = typer.Option(  # noqa: B008
        ...,
        "--profiler",
        "-p",
        case_sensitive=False,
        help="The taxonomic profiler used. All provided profiles must come from the "
        "same tool!",
        show_default=False,
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
    output: Path = typer.Option(  # noqa: B008
        ...,
        "--output",
        "-o",
        help="The desired output file. By default, the file extension will be used to "
        "determine the output format, but when setting the format explicitly using "
        "the --output-format option, automatic detection is disabled.",
        show_default=False,
    ),
    output_format: Optional[
        WideObservationTableFileFormat
    ] = typer.Option(  # noqa: B008
        None,
        case_sensitive=False,
        help="The desired output format. Depending on the choice, additional package "
        "dependencies may apply. By default it will be parsed from the output file "
        "name but it can be set explicitly and will then disable the automatic "
        "detection.",
    ),
    wide_format: bool = typer.Option(  # noqa: B008
        True,
        "--wide/--long",
        help="Output merged abundance data in either wide or (tidy) long format. "
        "Ignored when the desired output format is BIOM.",
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
    name: bool = typer.Option(  # noqa: B008
        False,
        "--add-name",
        help="Add the taxon name to the output.",
    ),
    rank: bool = typer.Option(  # noqa: B008
        False,
        "--add-rank",
        help="Add the taxon rank to the output.",
    ),
    lineage: bool = typer.Option(  # noqa: B008
        False,
        "--add-lineage",
        help="Add the taxon's entire lineage to the output. These are taxon names "
        "separated by semi-colons.",
    ),
    id_lineage: bool = typer.Option(  # noqa: B008
        False,
        "--add-id-lineage",
        help="Add the taxon's entire lineage to the output. These are taxon "
        "identifiers separated by semi-colons.",
    ),
) -> None:
    """Standardise and merge two or more taxonomic profiles."""
    # Perform input validation.
    valid_output_format: Union[
        TidyObservationTableFileFormat, WideObservationTableFileFormat
    ]
    # When a BIOM output format is chosen, the result can only be a wide format BIOM.
    if output.suffix.lower() == ".biom" or (
        output_format is not None
        and output_format is WideObservationTableFileFormat.BIOM
    ):
        try:
            WideObservationTableFileFormat.check_dependencies(
                WideObservationTableFileFormat.BIOM
            )
        except RuntimeError as error:
            logger.debug("", exc_info=error)
            logger.critical(str(error))
            raise typer.Exit(code=1)
        valid_output_format = WideObservationTableFileFormat.BIOM
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

    taxonomy_service: Optional[TaxonomyService] = None
    if taxonomy is not None:
        from taxpasta.infrastructure.domain.service.taxopy_taxonomy_service import (
            TaxopyTaxonomyService,
        )

        taxonomy_service = TaxopyTaxonomyService.from_taxdump(taxonomy)

    if summarise_at is not None:
        if taxonomy is None:
            logger.critical(
                "The summarising feature '--summarise-at' requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise typer.Exit(code=2)

    if name:
        if taxonomy is None:
            logger.critical(
                "The '--add-name' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise typer.Exit(code=2)

    if rank:
        if taxonomy is None:
            logger.critical(
                "The '--add-rank' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise typer.Exit(code=2)

    if lineage:
        if taxonomy is None:
            logger.critical(
                "The '--add-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise typer.Exit(code=2)

    if id_lineage:
        if taxonomy is None:
            logger.critical(
                "The '--add-id-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise typer.Exit(code=2)

    # Ensure that we can write to the output directory.
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        logger.critical("Failed to create the parent directory for the output.")
        logger.critical(str(error))
        raise typer.Exit(1)

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
            raise typer.Exit(code=2)
        elif len(profiles) == 1:
            logger.critical(
                "Only a single profile was provided. Please provide at least two."
            )
            raise typer.Exit(code=2)
        # Parse sample names from file names.
        data = [(prof.stem, prof) for prof in profiles]

    merging_app = SampleMergingApplication(
        profile_reader=ApplicationServiceRegistry.profile_reader(profiler),
        profile_standardiser=ApplicationServiceRegistry.profile_standardisation_service(
            profiler
        ),
        taxonomy_service=taxonomy_service,
    )
    try:
        result = merging_app.run(data, wide_format, summarise_at=summarise_at)
    except StandardisationError as error:
        logger.debug("", exc_info=error)
        logger.critical(
            "Error in sample '%s' with profile '%s'.", error.sample, error.profile
        )
        logger.critical(error.message)
        raise typer.Exit(code=1)
    except ValueError as error:
        logger.debug("", exc_info=error)
        logger.critical(str(error))
        raise typer.Exit(code=1)

    # The order of the following conditions is chosen specifically to yield a pleasant
    # output format.

    if id_lineage and valid_output_format is not WideObservationTableFileFormat.BIOM:
        assert taxonomy_service is not None  # nosec assert_used
        result = taxonomy_service.add_identifier_lineage(result)

    if lineage and valid_output_format is not WideObservationTableFileFormat.BIOM:
        assert taxonomy_service is not None  # nosec assert_used
        result = taxonomy_service.add_name_lineage(result)

    if rank and valid_output_format is not WideObservationTableFileFormat.BIOM:
        assert taxonomy_service is not None  # nosec assert_used
        result = taxonomy_service.add_rank(result)

    if name and valid_output_format is not WideObservationTableFileFormat.BIOM:
        assert taxonomy_service is not None  # nosec assert_used
        result = taxonomy_service.add_name(result)

    logger.info("Write result to '%s'.", str(output))
    if wide_format:
        assert isinstance(  # nosec assert_used
            valid_output_format, WideObservationTableFileFormat
        )
        writer = ApplicationServiceRegistry.wide_observation_table_writer(
            valid_output_format
        )
    else:
        assert isinstance(  # nosec assert_used
            valid_output_format, TidyObservationTableFileFormat
        )
        writer = ApplicationServiceRegistry.tidy_observation_table_writer(
            valid_output_format  # type: ignore
        )
    try:
        if (
            taxonomy is not None
            and valid_output_format is WideObservationTableFileFormat.BIOM
        ):
            writer.write(result, output, taxonomy=taxonomy_service)
        else:
            writer.write(result, output)
    except OSError as error:
        logger.critical("Failed to write the output result.")
        logger.critical(str(error))
        raise typer.Exit(1)
