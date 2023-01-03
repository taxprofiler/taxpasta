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


"""Provide a description of the kaiju profile format."""

import numpy as np
import pandera as pa
from pandera.typing import Series


class KaijuProfile(pa.SchemaModel):
    """Define the expected kaiju profile format."""

    file: Series[str] = pa.Field()
    percent: Series[float] = pa.Field(ge=0.0, le=100.0)
    reads: Series[int] = pa.Field(ge=0)
    # Pandas cannot handle missing integer values. Thus, we read this column as string.
    taxon_id: Series[str] = pa.Field(nullable=True)
    taxon_name: Series[str] = pa.Field()

    @pa.check("percent", name="compositionality")
    @classmethod
    def check_compositionality(cls, percent: Series[float]) -> bool:
        """Check that the percentages add up to a hundred."""
        # Kaiju reports percentages with sixth decimals
        return len(percent) == 0 or bool(np.isclose(percent.sum(), 100.0, atol=1e-06))

    @pa.check("file", name="unique_filename")
    @classmethod
    def check_unique_filename(cls, file_col: Series[str]) -> bool:
        """Check that Kaiju filename is unique."""
        return len(file_col) == 0 or file_col.nunique() == 1

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
        strict = True
