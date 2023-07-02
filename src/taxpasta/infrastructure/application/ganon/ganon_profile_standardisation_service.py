# Copyright (c) 2023 Moritz E. Beber
# Copyright (c) 2023 Maxime Borry
# Copyright (c) 2023 James A. Fellows Yates
# Copyright (c) 2023 Sofia Stamouli.
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


"""Provide a standardisation service for ganon profiles."""


import logging

import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .ganon_profile import GanonProfile


logger = logging.getLogger(__name__)


class GanonProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for ganon profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(cls, profile: DataFrame[GanonProfile]) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given ganon profile.

        Args:
            profile: A taxonomic profile generated by ganon.

        Returns:
            A standardized profile.

        """
        return (
            profile[[GanonProfile.target, GanonProfile.number_unique]]
            .copy()
            .rename(
                columns={
                    GanonProfile.target: StandardProfile.taxonomy_id,
                    GanonProfile.number_unique: StandardProfile.count,
                }
            )
        )
