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


"""Provide a description of the kraken2 profile format."""


from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series

from taxpasta.infrastructure.helpers import BaseDataFrameModel


class Kraken2Profile(BaseDataFrameModel):
    """Define the expected kraken2 profile format."""

    percent: Series[float] = pa.Field(ge=0.0, le=100.0)
    clade_assigned_reads: Series[int] = pa.Field(ge=0)
    direct_assigned_reads: Series[int] = pa.Field(ge=0)
    num_minimizers: Optional[Series[int]] = pa.Field(ge=0)
    distinct_minimizers: Optional[Series[int]] = pa.Field(ge=0)
    taxonomy_lvl: Series[str] = pa.Field()
    taxonomy_id: Series[int] = pa.Field(ge=0)
    name: Series[str] = pa.Field()

    @pa.dataframe_check
    def check_compositionality(cls, profile: pd.DataFrame) -> bool:
        """Check that the percent of 'unclassified' and 'root' add up to a hundred."""
        # Kraken2 reports percentages only to the second decimal, so we expect
        # some deviation.
        # If 100% of reads are assigned, unclassified reads are not reported at all.
        return profile.empty or bool(
            np.isclose(
                profile.loc[
                    profile[cls.taxonomy_lvl].isin(["U", "R"]), cls.percent
                ].sum(),
                100.0,
                atol=1.0,
            )
        )
