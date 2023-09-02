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


"""Provide a sample handling application."""


from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Optional, Type

from pandera.errors import SchemaErrors
from pandera.typing import DataFrame

from taxpasta.application.error import StandardisationError
from taxpasta.application.service import ProfileReader, ProfileStandardisationService
from taxpasta.domain.model import (
    Sample,
    StandardProfile,
    TidyObservationTable,
    WideObservationTable,
)
from taxpasta.domain.service import SampleMergingService, TaxonomyService


logger = logging.getLogger(__name__)


class SampleHandlingApplication:
    """Define the sample handling application."""

    def __init__(
        self,
        *,
        profile_reader: Type[ProfileReader],
        profile_standardiser: Type[ProfileStandardisationService],
        taxonomy_service: Optional[TaxonomyService] = None,
        **kwargs: dict,
    ):
        """
        Initialize the sample handling application.

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
        self.taxonomy_service = taxonomy_service

    def etl_sample(self, name: str, profile: Path) -> Sample:
        """
        Extract, transform, and load a profile into a sample.

        Args:
            name: A name for the sample.
            profile: The path to a taxonomic profile.

        Returns:
            A sample.

        Raises:
            StandardisationError: If the given profile does not match the validation
                schema.

        """
        try:
            result = self.standardiser.transform(self.reader.read(profile))
        except SchemaErrors as errors:
            if errors.data.empty:
                raise StandardisationError(
                    sample=name, profile=profile, message="Profile is empty."
                ) from errors
            else:
                raise StandardisationError(
                    sample=name, profile=profile, message=str(errors.failure_cases)
                ) from errors
        except ValueError as error:
            raise StandardisationError(
                sample=name, profile=profile, message=str(error)
            ) from error

        return Sample(name=name, profile=result)

    def summarise_sample(self, sample: Sample, rank: str) -> Sample:
        """Summarise a sample at a higher taxonomic rank."""
        assert self.taxonomy_service is not None  # nosec assert_used
        return Sample(
            name=sample.name,
            profile=self.taxonomy_service.summarise_at(sample.profile, rank),
        )

    def merge_samples(
        self,
        samples: Iterable[Sample],
        wide_format: bool,
    ) -> DataFrame[WideObservationTable] | DataFrame[TidyObservationTable]:
        """
        Merge two or more  samples into a single table.

        Args:
            samples: Two or more samples.
            wide_format: Whether to create wide or (tidy) long format output.

        Returns:
            A single table containing all samples in the desired format.

        """
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
