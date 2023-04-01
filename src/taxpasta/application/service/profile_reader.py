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


"""Provide an abstract base class for reading taxonomic profiles."""


from abc import ABC, abstractmethod
from typing import Type

import pandas as pd
import pandera as pa

from ._types import BufferOrFilepath


class ProfileReader(ABC):
    """Define an abstract base class for reading taxonomic profiles."""

    @classmethod
    @abstractmethod
    def read(cls, profile: BufferOrFilepath) -> pd.DataFrame:
        """Read a taxonomic profile from the given source."""

    @classmethod
    def _check_num_columns(
        cls, profile: pd.DataFrame, schema_model: Type[pa.DataFrameModel]
    ) -> None:
        """Perform a strict test on the number of columns."""
        num_cols = len(schema_model.to_schema().columns)
        if len(profile.columns) != num_cols:
            raise ValueError(
                f"Unexpected report format. It has {len(profile.columns)} columns but "
                f"only {num_cols} are expected."
            )
