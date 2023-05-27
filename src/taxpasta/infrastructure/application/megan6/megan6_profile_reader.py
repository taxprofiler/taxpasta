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


"""Provide a reader for megan6 profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader
from taxpasta.infrastructure.helpers import raise_parser_warnings

from .megan6_profile import Megan6Profile


class Megan6ProfileReader(ProfileReader):
    """Define a reader for MEGAN6 rma2info profiles."""

    @classmethod
    @raise_parser_warnings
    def read(cls, profile: BufferOrFilepath) -> DataFrame[Megan6Profile]:
        """Read a MEGAN6 rma2info taxonomic profile from a file."""
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            names=[Megan6Profile.taxonomy_id, Megan6Profile.count],
            index_col=False,
        )
        cls._check_num_columns(result, Megan6Profile)
        return result
