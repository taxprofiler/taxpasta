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


"""Provide a description of the ganon profile format."""


import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series

from taxpasta.infrastructure.helpers import BaseDataFrameModel


class GanonProfile(BaseDataFrameModel):
    """Define the expected ganon profile format."""

    rank: Series[str] = pa.Field()
    target: Series[int] = pa.Field(
        ge=0
    )  ## TODO: problem - unclassified gets assigned `-`
    lineage: Series[str] = pa.Field()  ## note - unclassified gets assigned `-`
    name: Series[str] = pa.Field()
    nr_unique: Series[int] = pa.Field(ge=0)
    nr_shared: Series[int] = pa.Field(ge=0)
    nr_children: Series[int] = pa.Field(ge=0)
    nr_cumulative: Series[int] = pa.Field(ge=0)
    pc_cumulative: Series[float] = pa.Field(ge=0.0, le=100.0)

    @pa.dataframe_check
    def check_compositionality(cls, profile: pd.DataFrame) -> bool:
        """Check that the percent of 'unclassified' and 'root' add up to a hundred."""
        ## TODO: may need tweak tolerance amount, based on experience
        ## ganon reports percentage to 5 decimal places
        return profile.empty or bool(
            np.isclose(
                profile.loc[
                    profile[cls.rank].isin(["unclassified", "root"]), cls.pc_cumulative
                ].sum(),
                100.0,
                atol=0.001,
            )
        )
