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


"""Provide a description of the KrakenUniq profile format."""


import pandas as pd
import pandera as pa
from pandera.typing import Series


class KrakenUniqProfile(pa.SchemaModel):
    """Define the expected KrakenUniq profile format."""

    percent: Series[float] = pa.Field(ge=0.0, le=100.0, alias="%")
    reads: Series[int] = pa.Field(ge=0)
    tax_reads: Series[int] = pa.Field(ge=0, alias="taxReads")
    kmers: Series[int] = pa.Field(ge=0)
    duplicates: Series[float] = pa.Field(ge=0.0, alias="dup")
    coverage: Series[float] = pa.Field(ge=0.0, alias="cov")
    tax_id: Series[int] = pa.Field(alias="taxID", ge=0)
    rank: Series[pd.CategoricalDtype] = pa.Field()
    tax_name: Series[str] = pa.Field(alias="taxName")

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
        strict = True
