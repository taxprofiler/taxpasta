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


"""Provide a sample merging application."""


from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List, Optional, Tuple, Type

from pandera.errors import SchemaErrors
from pandera.typing import DataFrame

from taxpasta.application.error import StandardisationError
from taxpasta.application.service.profile_reader import ProfileReader
from taxpasta.application.service.profile_standardisation_service import (
    ProfileStandardisationService,
)
from taxpasta.domain.model import (
    Sample,
    StandardProfile,
    TidyObservationTable,
    WideObservationTable,
)
from taxpasta.domain.service import SampleMergingService, TaxonomyService


logger = logging.getLogger(__name__)


class SampleMergingApplication:
    """Define a sample merging application."""

    def __init__(
        self,
        *,
        profile_reader: Type[ProfileReader],
        profile_standardiser: Type[ProfileStandardisationService],
        taxonomy_service: Optional[TaxonomyService] = None,
        **kwargs: dict,
    ):
        """
        Initialize the application for a particular taxonomic profiler.

        Args:
            profile_reader: A profile reader for a specific taxonomic profile format.
            profile_standardiser: A profile standardisation service for a specific
                taxonomic profile format.
            taxonomy_service: A taxonomy service instance. It is assumed that all
                profiles to be handled in the application are based on the given
                taxonomy loaded in the service instance.
            **kwargs: Passed on for inheritance.

        """
        super().__init__(**kwargs)
        self.reader = profile_reader
        self.standardiser = profile_standardiser
        self.taxonomy = taxonomy_service

    def run(
        self,
        profiles: Iterable[Tuple[str, Path]],
        wide_format: bool,
        summarise_at: Optional[str] = None,
        ignore_error: bool = False,
    ) -> DataFrame[WideObservationTable] | DataFrame[TidyObservationTable]:
        """
        Extract and transform profiles into samples, then merge them.

        Args:
            profiles: Pairs of name and profile path.
            wide_format: Whether to create wide or (tidy) long format output.
            summarise_at: The taxonomic rank at which to summarise abundance if any.
            ignore_error: Whether to ignore profiles that contain errors.

        Returns:
            A single table containing all samples in the desired format.

        Raises:
            StandardisationError: If any of the given profiles does not match the
                validation schema.  # noqa: DAR402

        """
        samples = self._etl_samples(profiles, ignore_error)

        if summarise_at is not None:
            samples = self._summarise_samples(samples, summarise_at, ignore_error)

        if wide_format:
            wide_table = SampleMergingService.merge_wide(samples)
            # If any profile did not have all the same taxonomy IDs as the combined
            # table, additional zeroes were introduced.
            if any(
                not wide_table[WideObservationTable.taxonomy_id]
                .isin(sample.profile[StandardProfile.taxonomy_id])
                .all()
                for sample in samples
            ):
                logger.warning(
                    "The merged profiles contained different taxa. Additional "
                    "zeroes were introduced for missing taxa."
                )
            return wide_table
        else:
            return SampleMergingService.merge_long(samples)

    def _etl_samples(
        self, profiles: Iterable[Tuple[str, Path]], ignore_error: bool
    ) -> List[Sample]:
        """Extract, transform, and load profiles into samples."""
        result = []
        for name, profile in profiles:
            try:
                result.append(
                    Sample(
                        name=name,
                        profile=self.standardiser.transform(self.reader.read(profile)),
                    )
                )
            except SchemaErrors as errors:
                if ignore_error:
                    logger.error("Sample %s: %s", name, str(errors))
                    continue
                else:
                    raise StandardisationError(
                        sample=name, profile=profile, message=str(errors.failure_cases)
                    ) from errors
            except ValueError as error:
                if ignore_error:
                    logger.error("Sample %s: %s", name, str(error))
                    continue
                else:
                    raise StandardisationError(
                        sample=name, profile=profile, message=str(error)
                    ) from error
        return result

    def _summarise_samples(
        self, samples: List[Sample], rank: str, ignore_error: bool
    ) -> List[Sample]:
        """Summarise samples at a given taxonomic rank."""
        assert self.taxonomy is not None  # nosec assert_used
        result = []
        for sample in samples:
            try:
                result.append(
                    Sample(
                        name=sample.name,
                        profile=self.taxonomy.summarise_at(sample.profile, rank),
                    )
                )
            except ValueError as error:
                if ignore_error:
                    logger.error("Sample %s: %s", sample.name, str(error))
                    continue
                else:
                    raise
        return result
