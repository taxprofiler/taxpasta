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


"""Provide a description of the KrakenUniq profile format."""


import pandas as pd
import pandera as pa
from pandera.typing import Series


class KrakenUniqProfile(pa.SchemaModel):
    """Define the expected KrakenUniq profile format."""

    percent: Series[float] = pa.Field(ge=0.0, le=100.0)
    reads: Series[int] = pa.Field(ge=0)
    taxReads: Series[int] = pa.Field(ge=0)
    kmers: Series[int] = pa.Field(ge=0)
    dup: Series[float] = pa.Field(ge=0.0)
    cov: Series[float] = pa.Field(ge=0.0)
    taxID: Series[pd.CategoricalDtype] = pa.Field()
    rank: Series[pd.CategoricalDtype] = pa.Field()
    taxName: Series[str] = pa.Field()

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
        strict = True
