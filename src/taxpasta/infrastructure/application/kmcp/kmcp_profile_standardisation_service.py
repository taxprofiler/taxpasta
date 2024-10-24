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


"""Provide a standardisation service for KMCP profiles."""

import logging

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .kmcp_profile import KMCPProfile


logger = logging.getLogger(__name__)


class KMCPProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for KMCP profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(cls, profile: DataFrame[KMCPProfile]) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given KMCP profile.

        Args:
            profile: A taxonomic profile generated by KMCP.

        Returns:
            A standardized profile.

        """
        temp = (
            profile[[KMCPProfile.taxid, KMCPProfile.reads]]
            .copy()
            .rename(
                columns={
                    KMCPProfile.taxid: StandardProfile.taxonomy_id,
                    KMCPProfile.reads: StandardProfile.count,
                },
            )
        )
        result = temp.loc[temp[StandardProfile.taxonomy_id].notna(), :].copy()
        result[StandardProfile.taxonomy_id] = result[
            StandardProfile.taxonomy_id
        ].astype(int)
        # Replace missing values (unclassified reads) with ID zero and sum reads.
        return pd.concat(
            [
                result,
                pd.DataFrame(
                    {
                        StandardProfile.taxonomy_id: [0],
                        StandardProfile.count: [
                            temp.loc[
                                temp[StandardProfile.taxonomy_id].isna(),
                                StandardProfile.count,
                            ].sum(),
                        ],
                    },
                    dtype=int,
                ),
            ],
            ignore_index=True,
        )
