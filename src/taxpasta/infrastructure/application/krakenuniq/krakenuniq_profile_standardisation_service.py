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


"""Provide a standardisation service for KrakenUniq profiles."""


import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application import ProfileStandardisationService
from taxpasta.domain import StandardProfile

from .krakenuniq_profile import KrakenUniqProfile


class KrakenUniqProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for krakenUniq profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(
        cls, profile: DataFrame[KrakenUniqProfile]
    ) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given krakenUniq profile.

        Args:
            profile: A taxonomic profile generated by KrakenUniq.

        Returns:
            A standardized profile.

        """
        result = profile[
            [KrakenUniqProfile.taxID, KrakenUniqProfile.taxReads]
        ].copy()
        result.columns = [StandardProfile.taxonomy_id, StandardProfile.count]
        return result
