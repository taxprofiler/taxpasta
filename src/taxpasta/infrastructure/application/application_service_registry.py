# flake8: noqa
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


"""Provide an application service registry."""


from typing import Type

from taxpasta.application import ProfileReader, ProfileStandardisationService

from .supported_profiler import SupportedProfiler


class ApplicationServiceRegistry:
    """Define an application service registry."""

    @classmethod
    def profile_reader(cls, profiler: SupportedProfiler) -> Type[ProfileReader]:
        """Return a profile reader of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileReader

            return BrackenProfileReader
        elif profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileReader

            return CentrifugeProfileReader
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileReader

            return Kraken2ProfileReader
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileReader

            return KaijuProfileReader
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileReader

            return MetaphlanProfileReader

    @classmethod
    def profile_standardisation_service(
        cls, profiler: SupportedProfiler
    ) -> Type[ProfileStandardisationService]:
        """Return a profile standardisation service of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileStandardisationService

            return BrackenProfileStandardisationService
        elif profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileStandardisationService

            return CentrifugeProfileStandardisationService
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileStandardisationService

            return KaijuProfileStandardisationService
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileStandardisationService

            return Kraken2ProfileStandardisationService
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileStandardisationService

            return MetaphlanProfileStandardisationService

    @classmethod
    def output_writer(cls):
        """Return a result writer of the correct type."""
        raise NotImplementedError()
