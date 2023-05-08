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


"""Provide a base data frame model for general checks and configuration."""


import pandas as pd
import pandera as pa


class BaseDataFrameModel(pa.DataFrameModel):
    """Define the base data frame model for general checks and configuration."""

    @pa.dataframe_check
    def check_not_empty(cls, profile: pd.DataFrame) -> bool:
        """Check that the read in profile is *not* empty."""
        return not profile.empty

    class Config:
        """Configure the schema model."""

        coerce = False
        ordered = True
        strict = True
