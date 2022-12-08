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


"""Provide a reader for motus profiles."""

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader

from .motus_profile import MotusProfile


class MotusProfileReader(ProfileReader):
    """Define a reader for mOTUS profiles."""

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[MotusProfile]:
        """Read a mOTUs taxonomic profile from a file."""
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            skiprows=3,
            header=None,
            names=["taxonomy", "tax_id", "read_count"],
            index_col=False,
            dtype={"tax_id": str},
        )

        if len(result.columns) != 3:
            raise ValueError(
                f"Unexpected mOTUs report format. It has {len(result.columns)} "
                f"columns but only 3 are expected."
            )

        return result
