# Copyright (c) 2022 Moritz E. Beber
# Copyright (c) 2022 Maxime Borry
# Copyright (c) 2022 James Fellows Yates
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


"""Provide a reader for diamond profiles."""

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader

from .diamond_profile import DiamondProfile


class DiamondProfileReader(ProfileReader):
    """Define a reader for Diamond profiles."""

    LARGE_INTEGER = int(10e6)

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[DiamondProfile]:
        """Read a diamond taxonomic profile from a file."""
        nb_expected_columns = 3
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=None,
            index_col=False,
            comment="#",
        )
        if len(result.columns) == nb_expected_columns:
            result.columns = [
                DiamondProfile.query_id,
                DiamondProfile.taxonomy_id,
                DiamondProfile.e_value,
            ]
        else:
            raise ValueError(
                f"Unexpected diamond report format. It has {len(result.columns)} "
                f"columns but only {nb_expected_columns} are expected."
            )
        return result
