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


"""Provide a description of the kraken2 profile format."""


import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Series
from typing import Dict, Optional

RANK_PREFIXES = dict(
    {
        "k": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
    }
)


class MetaphlanProfile(pa.SchemaModel):
    """Define the expected metaphlan profile format."""

    clade_name: Series[str] = pa.Field()
    taxonomy_id: Series[str] = pa.Field()
    relative_abundance: Series[float] = pa.Field(ge=0.0, le=100.0)
    additional_species: Optional[Series[str]] = pa.Field(nullable=True)
    rank: Series[pd.CategoricalDtype] = pa.Field(isin=RANK_PREFIXES.values())
    count: Series[int] = pa.Field()

    @classmethod
    @pa.check("relative_abundance", groupby="rank", name="compositionality")
    def check_compositionality(
        cls, grouped_value: Dict[pd.CategoricalDtype, Series[float]]
    ) -> bool:
        """Check that the percentages add up to a hundred."""
        is_compositional = True
        for r in RANK_PREFIXES.values():
            if not np.isclose(grouped_value[r].sum(), 100.0, atol=1.0):
                return False
        return is_compositional

    class Config:
        coerce = True
        ordered = True
        strict = True
