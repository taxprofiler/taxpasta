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


"""Provide a reader for malt profiles."""

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader

from .malt_profile import MaltProfile


class MaltProfileReader(ProfileReader):
    """Define a reader for MALT-rma2info profiles."""

    LARGE_INTEGER = int(10e6)

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[MaltProfile]:
        """Read a MALT-rma2info taxonomic profile from a file."""
        nb_expected_columns = 2
        result = pd.read_table(
            filepath_or_buffer=profile,
            compression="infer",
            sep="\t",
            names=[MaltProfile.taxonomy_id, MaltProfile.count],
            index_col=False,
        )
        if len(result.columns) != nb_expected_columns:
            raise ValueError(
                f"Unexpected MALT-rma2info report format. It has {len(result.columns)} "
                f"columns but only {nb_expected_columns} are expected."
            )
        return result
