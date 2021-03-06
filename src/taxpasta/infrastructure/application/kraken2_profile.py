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


class Kraken2Profile(pa.SchemaModel):
    """Define the expected kraken2 profile format."""

    percentage: Series[float] = pa.Field(ge=0.0, le=100.0)
    clade_assigned_reads: Series[int] = pa.Field(ge=0)
    direct_assigned_reads: Series[int] = pa.Field(ge=0)
    taxonomy_lvl: Series[pd.CategoricalDtype] = pa.Field()
    taxonomy_id: Series[pd.CategoricalDtype] = pa.Field()
    name: Series[str] = pa.Field()

    @classmethod
    @pa.check("percentage", name="compositionality")
    def check_compositionality(cls, percentage: Series[float]) -> bool:
        """Check that the percentages add up to a hundred."""
        # Kraken2 reports percentages only to the second decimal, so we expect
        # some deviation.
        return bool(np.isclose(percentage.sum(), 100.0, atol=0.01))

    class Config:
        coerce = True
        ordered = True
        strict = True
