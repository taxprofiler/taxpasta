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


"""Provide a standardisation service for mOTUs profiles."""


import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .motus_profile import MotusProfile


class MotusProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for mOTUs profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(cls, profile: DataFrame[MotusProfile]) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given mOTUs profile.

        Args:
            profile: A taxonomic profile generated by mOTUs.

        Returns:
            A standardized profile.

        """
        temp = (
            profile.loc[
                profile[MotusProfile.read_count] > 0,
                [MotusProfile.ncbi_tax_id, MotusProfile.read_count],
            ]
            .copy()
            .rename(
                columns={
                    MotusProfile.ncbi_tax_id: StandardProfile.taxonomy_id,
                    MotusProfile.read_count: StandardProfile.count,
                }
            )
        )
        # Split profile into entries with known and unknown tax ID.
        # Ignore entries with zero read count.
        result = (
            temp.loc[temp[StandardProfile.taxonomy_id].notnull(), :]
            .copy()
            .assign(
                **{
                    StandardProfile.taxonomy_id: lambda df: df[
                        StandardProfile.taxonomy_id
                    ].astype(int)
                }
            )
            # FIXME (Moritz): Apparently, mOTUs profiles can contain duplicate tax IDs.
            #  Clarify with Sofia and Maxime. For now, sum up read counts.
            #  https://github.com/taxprofiler/taxpasta/issues/46
            .groupby(StandardProfile.taxonomy_id, as_index=False, sort=False)
            .sum()
        )
        # Sum up all remaining read counts without tax ID to be 'unassigned'.
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
                    },
                    dtype=int,
                ),
            ],
            ignore_index=True,
        )
