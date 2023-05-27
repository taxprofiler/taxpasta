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


"""Provide a reader for kraken2 profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader
from taxpasta.infrastructure.helpers import raise_parser_warnings

from .kraken2_profile import Kraken2Profile


class Kraken2ProfileReader(ProfileReader):
    """Define a reader for kraken2 profiles."""

    @classmethod
    @raise_parser_warnings
    def read(cls, profile: BufferOrFilepath) -> DataFrame[Kraken2Profile]:
        """
        Read a kraken2 taxonomic profile from the given source.

        Args:
            profile: A source that contains a tab-separated taxonomic profile generated
                by kraken2.

        Returns:
            A data frame representation of the kraken2 profile.

        Raises:
            ValueError: In case the table does not contain exactly six or eight columns.

        """
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=None,
            index_col=False,
            skipinitialspace=True,
        )
        if len(result.columns) == 6:
            result.columns = [
                Kraken2Profile.percent,
                Kraken2Profile.clade_assigned_reads,
                Kraken2Profile.direct_assigned_reads,
                Kraken2Profile.taxonomy_lvl,
                Kraken2Profile.taxonomy_id,
                Kraken2Profile.name,
            ]
        elif len(result.columns) == 8:
            result.columns = [
                Kraken2Profile.percent,
                Kraken2Profile.clade_assigned_reads,
                Kraken2Profile.direct_assigned_reads,
                Kraken2Profile.num_minimizers,
                Kraken2Profile.distinct_minimizers,
                Kraken2Profile.taxonomy_lvl,
                Kraken2Profile.taxonomy_id,
                Kraken2Profile.name,
            ]
        else:
            raise ValueError(
                f"Unexpected kraken2 report format. It has {len(result.columns)} "
                f"columns but only six or eight are expected."
            )
        return result
