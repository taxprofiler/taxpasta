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


"""Provide a reader for kmcp profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader
from taxpasta.infrastructure.helpers import raise_parser_warnings

from .kmcp_profile import KmcpProfile


class KmcpProfileReader(ProfileReader):
    """Define a reader for kmcp profiles."""

    @classmethod
    @raise_parser_warnings
    def read(cls, profile: BufferOrFilepath) -> DataFrame[KmcpProfile]:
        """
        Read a kmcp taxonomic profile from the given source.

        Args:
            profile: A source that contains a tab-separated taxonomic profile generated
                by kmcp.

        Returns:
            A data frame representation of the kmcp profile.

        """
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=0,
            index_col=False,
            dtype={
                KmcpProfile.chunks_fraction: float,
                KmcpProfile.chunks_relative_depth: float,
            },

        )
        cls._check_num_columns(result, KmcpProfile)
        return result
