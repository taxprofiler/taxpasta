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


"""Provide a description of an observation matrix."""


from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series


class WideObservationTable(pa.DataFrameModel):
    """Define the observation matrix."""

    taxonomy_id: Series[pd.CategoricalDtype] = pa.Field()
    name: Optional[Series[pd.CategoricalDtype]] = pa.Field()
    rank: Optional[Series[pd.CategoricalDtype]] = pa.Field()
    lineage: Optional[Series[pd.CategoricalDtype]] = pa.Field()
    id_lineage: Optional[Series[pd.CategoricalDtype]] = pa.Field()
    rank_lineage: Optional[Series[pd.CategoricalDtype]] = pa.Field()
    # This field uses a regex to match all columns that are not one of the above.
    any_samples: Series[np.int64] = pa.Field(
        ge=0,
        alias="^(?!(taxonomy_id|name|rank|lineage|id_lineage|rank_lineage)$).*",
        regex=True,
    )

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
