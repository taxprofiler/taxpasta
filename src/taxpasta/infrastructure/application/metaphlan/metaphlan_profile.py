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


"""Provide a description of the metaphlan profile format."""


from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series

from taxpasta.infrastructure.helpers import BaseDataFrameModel


class MetaphlanProfile(BaseDataFrameModel):
    """Define the expected metaphlan profile format."""

    clade_name: Series[str] = pa.Field()
    # MetaPhlan provides the full lineage of tax IDs in this field.
    ncbi_tax_id: Series[str] = pa.Field(alias="NCBI_tax_id")
    relative_abundance: Series[float] = pa.Field(ge=0.0, le=100.0)
    additional_species: Optional[Series[str]] = pa.Field(nullable=True)

    @pa.dataframe_check
    def check_compositionality(cls, profile: pd.DataFrame) -> bool:
        """Check that the percentages per rank add up to a hundred."""
        # Parse the rank from the given lineage.
        rank = profile[cls.clade_name].str.rsplit("|", n=1).str[-1].str[0]
        return profile.empty or bool(
            np.allclose(
                profile.groupby(rank, sort=False)[cls.relative_abundance].sum(),
                100.0,
                atol=1.0,
            )
        )
