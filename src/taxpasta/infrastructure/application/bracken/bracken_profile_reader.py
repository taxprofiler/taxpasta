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


"""Provide a reader for Bracken profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader
from taxpasta.infrastructure.helpers import raise_parser_warnings

from .bracken_profile import BrackenProfile


class BrackenProfileReader(ProfileReader):
    """Define a reader for Bracken profiles."""

    @classmethod
    @raise_parser_warnings
    def read(cls, profile: BufferOrFilepath) -> DataFrame[BrackenProfile]:
        """
        Read a Bracken taxonomic profile from the given source.

        Args:
            profile: A source that contains a tab-separated taxonomic profile generated
                by Bracken.

        Returns:
            A data frame representation of the Bracken profile.

        """
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            index_col=False,
            skipinitialspace=True,
        )
        cls._check_num_columns(result, BrackenProfile)
        return result
