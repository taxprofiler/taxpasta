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


"""Provide a description of the Bracken profile format."""


import numpy as np
import pandera as pa
from pandera.typing import DataFrame, Series

from taxpasta.infrastructure.helpers import BaseDataFrameModel


class BrackenProfile(BaseDataFrameModel):
    """Define the expected Bracken profile format."""

    name: Series[str] = pa.Field()
    taxonomy_id: Series[int] = pa.Field(ge=0)
    taxonomy_lvl: Series[str] = pa.Field()
    kraken_assigned_reads: Series[int] = pa.Field(ge=0)
    added_reads: Series[int] = pa.Field(ge=0)
    new_est_reads: Series[int] = pa.Field(ge=0)
    fraction_total_reads: Series[float] = pa.Field(ge=0.0, le=1.0)

    @pa.check("fraction_total_reads", name="compositionality")
    def check_compositionality(cls, fraction_total_reads: Series[float]) -> bool:
        """Check that the fractions of reads add up to one."""
        # Bracken reports fractions with five decimals but rounding errors accumulate.
        return fraction_total_reads.empty or bool(
            np.isclose(fraction_total_reads.sum(), 1.0, atol=0.02)
        )

    @pa.dataframe_check
    def check_added_reads_consistency(cls, profile: DataFrame) -> Series[bool]:
        """Check that Bracken added reads are consistent."""
        return (
            profile[cls.kraken_assigned_reads] + profile[cls.added_reads]
            == profile[cls.new_est_reads]
        )
