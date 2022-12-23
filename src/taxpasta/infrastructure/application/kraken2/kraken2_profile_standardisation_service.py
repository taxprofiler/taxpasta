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


"""Provide a standardisation service for kraken2 profiles."""


import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .kraken2_profile import Kraken2Profile


class Kraken2ProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for kraken2 profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(
        cls, profile: DataFrame[Kraken2Profile]
    ) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given kraken2 profile.

        Args:
            profile: A taxonomic profile generated by kraken2.

        Returns:
            A standardized profile.

        """
        result = profile[
            [Kraken2Profile.taxonomy_id, Kraken2Profile.direct_assigned_reads]
        ].copy()
        result.columns = [StandardProfile.taxonomy_id, StandardProfile.count]
        result[StandardProfile.taxonomy_id] = result[
            StandardProfile.taxonomy_id
        ].astype(str)
        return result
