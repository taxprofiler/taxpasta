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


"""Provide a standardisation service for kaiju profiles."""
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .kaiju_profile import KaijuProfile


class KaijuProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for kaiju profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(cls, profile: DataFrame[KaijuProfile]) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given kaiju profile.

        Args:
            profile: A taxonomic profile generated by kaiju.

        Returns:
            A standardized profile.

        """
        temp = (
            profile[[KaijuProfile.taxon_id, KaijuProfile.reads]]
            .copy()
            .rename(
                columns={
                    KaijuProfile.taxon_id: StandardProfile.taxonomy_id,
                    KaijuProfile.reads: StandardProfile.count,
                }
            )
        )
        result = temp.loc[temp[StandardProfile.taxonomy_id].notnull(), :].copy()
        result[StandardProfile.taxonomy_id] = result[
            StandardProfile.taxonomy_id
        ].astype(int)
        # Replace missing values (unclassified reads) with zeroes and sum reads.
        return pd.concat(
            [
                result,
                pd.DataFrame(
                    {
                        StandardProfile.taxonomy_id: [0],
                        StandardProfile.count: [
                            temp.loc[
                                temp[StandardProfile.taxonomy_id].isnull(),
                                StandardProfile.count,
                            ].sum()
                        ],
                    }
                ),
            ],
            ignore_index=True,
        )
