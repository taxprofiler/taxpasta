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


class KmcpProfile(BaseDataFrameModel):
    """Define the expected kmcp profile format."""

    ref: Series[str] = pa.Field()
    percentage: Series[float] = pa.Field(ge=0.0, le=100.0)
    coverage:  Series[float] = pa.Field(ge=0.0, nullable=True)
    score: Series[float] = pa.Field(ge=0.0, le=100.0)
    chunksFrac:  Series[float] = pa.Field(ge=0.0, le=1.0)
    chunksRelDepth:  Series[float] = pa.Field(ge=0.0, le=100.0)
    chunksRelDepthStd:  Series[float] = pa.Field(ge=0.0, le=100.0)
    reads: Series[int] = pa.Field(ge=0)
    ureads: Series[int] = pa.Field(ge=0)
    hicureads: Series[int] = pa.Field(ge=0)
    refsize: Series[int] = pa.Field(ge=0)
    refname: Series[str] = pa.Field(nullable=True)
    taxid: Series[int] = pa.Field(ge=0)
    rank: Series[str] = pa.Field(nullable=True)
    taxname: Series[str] = pa.Field(nullable=True)
    taxpath: Series[str] = pa.Field(nullable=True)
    taxpathsn: Series[str] = pa.Field(nullable=True)


    @pa.check("percentage", name="compositionality")
    def check_compositionality(cls, percentage: Series[float]) -> bool:
        """Check that the percentages add up to a hundred."""
        # KMCP profile reports percentages with sixth decimals
        return percentage.empty or bool(np.isclose(percentage.sum(), 100.0, atol=1.0))
