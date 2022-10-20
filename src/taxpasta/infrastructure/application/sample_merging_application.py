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


from pathlib import Path
from typing import Iterable, Tuple

from pandera.typing import DataFrame

from taxpasta.domain import Sample, SampleMergingService

from .application_service_registry import ApplicationServiceRegistry
from .supported_profiler import SupportedProfiler


class SampleMergingApplication:
    """Define a sample merging application."""

    def __init__(self, *, profiler: SupportedProfiler, **kwargs):
        """
        Initialize the application for a particular taxonomic profiler.

        Args:
            profiler: One of the supported profilers.
            **kwargs: Passed on for inheritance.

        """
        super().__init__(**kwargs)
        self.reader = ApplicationServiceRegistry.profile_reader(profiler)
        self.standardiser = ApplicationServiceRegistry.profile_standardisation_service(
            profiler
        )

    def run(self, profiles: Iterable[Tuple[str, Path]], wide_format: bool) -> DataFrame:
        """
        Extract and transform profiles into samples, then merge them.

        Args:
            profiles: Pairs of name and profile path.
            wide_format: Whether to create wide or (tidy) long format output.

        Returns:
            A single table containing all samples in the desired format.

        """
        samples = [
            Sample(
                name=name,
                profile=self.standardiser.transform(self.reader.read(profile)),
            )
            for name, profile in profiles
        ]

        if wide_format:
            return SampleMergingService.merge_wide(samples)
        else:
            return SampleMergingService.merge_long(samples)
