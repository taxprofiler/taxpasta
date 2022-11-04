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


"""Provide a sample merging application."""


from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Tuple, Type

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
from taxpasta.domain.service import SampleMergingService


logger = logging.getLogger(__name__)


class SampleMergingApplication:
    """Define a sample merging application."""

    def __init__(
        self,
        *,
        profile_reader: Type[ProfileReader],
        profile_standardiser: Type[ProfileStandardisationService],
        **kwargs: dict,
    ):
        """
        Initialize the application for a particular taxonomic profiler.

        Args:
            profile_reader: A profile reader for a specific taxonomic profile format.
            profile_standardiser: A profile standardisation service for a specific
                taxonomic profile format.
            **kwargs: Passed on for inheritance.

        """
        super().__init__(**kwargs)
        self.reader = profile_reader
        self.standardiser = profile_standardiser

    def run(
        self,
        profiles: Iterable[Tuple[str, Path]],
        wide_format: bool,
        ignore_error: bool = False,
    ) -> DataFrame[WideObservationTable] | DataFrame[TidyObservationTable]:
        """
        Extract and transform profiles into samples, then merge them.

        Args:
            profiles: Pairs of name and profile path.
            wide_format: Whether to create wide or (tidy) long format output.
            ignore_error: Whether to ignore profiles that contain errors.

        Returns:
            A single table containing all samples in the desired format.

        Raises:
            StandardisationError: If any of the given profiles does not match the
                validation schema.

        """
        samples = []
        for name, profile in profiles:
            try:
                samples.append(
                    Sample(
                        name=name,
                        profile=self.standardiser.transform(self.reader.read(profile)),
                    )
                )
            except SchemaErrors as errors:
                if ignore_error:
                    continue
                else:
                    raise StandardisationError(
                        sample=name, profile=profile, message=str(errors.failure_cases)
                    ) from errors
            except ValueError as error:
                if ignore_error:
                    continue
                else:
                    raise StandardisationError(
                        sample=name, profile=profile, message=str(error.args)
                    ) from error

        if wide_format:
            wide_table = SampleMergingService.merge_wide(samples)
            # If any profile did not have all the same taxonomy IDs as the combined
            # table, additional zeroes were introduced.
            if any(
                not sample.profile[StandardProfile.taxonomy_id]
                .isin(wide_table[WideObservationTable.taxonomy_id])
                .all()
                for sample in samples
            ):
                logger.warning(
                    "The merged profiles contained different taxa. Additional "
                    "zeroes were introduced for missing taxa."
                )
            return
        else:
            return SampleMergingService.merge_long(samples)
