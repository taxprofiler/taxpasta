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


"""Provide a standardisation service for kraken2 profiles."""


import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application import ProfileStandardisationService
from taxpasta.domain import StandardProfile

from .metaphlan_profile import MetaphlanProfile


class MetaphlanProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for metaphlan profiles."""

    @classmethod
    @pa.check_types
    def transform(
        cls, profile: DataFrame[MetaphlanProfile]
    ) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given kraken2 profile.

        Args:
            profile: A taxonomic profile generated by kraken2.

        Returns:
            A standardized profile.

        """
        result = profile[
            [MetaphlanProfile.taxonomy_id, MetaphlanProfile.relative_abundance]
        ].copy()
        result.columns = ["taxonomy_id", "count"]
        return result
