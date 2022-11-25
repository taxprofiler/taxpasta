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


"""Provide a sample ETL application."""


from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Type

from pandera.errors import SchemaErrors

from taxpasta.application.error import StandardisationError
from taxpasta.application.service import ProfileReader, ProfileStandardisationService
from taxpasta.domain.model import Sample


logger = logging.getLogger(__name__)


class SampleETLApplication:
    """Define the sample ETL application."""

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

    def etl(self, profile: Path, name: Optional[str] = None) -> Sample:
        """
        Extract, transform, and load a profile into a sample.

        Args:
            profile: A taxonomic profile.
            name: An optional name for the sample. Otherwise, the profile's filename is
                used.

        Returns:
            A sample.

        Raises:
            StandardisationError: If the given profile does not match the validation
                schema.  # noqa: DAR402

        """
        if name is None:
            name = profile.stem
        try:
            return Sample(
                name=name,
                profile=self.standardiser.transform(self.reader.read(profile)),
            )
        except SchemaErrors as errors:
            raise StandardisationError(
                sample=profile.stem, profile=profile, message=str(errors.failure_cases)
            ) from errors