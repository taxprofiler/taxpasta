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


"""Provide a reader for metaphlan profiles."""

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application import ProfileReader, ProfileSource

from .metaphlan_profile import RANK_PREFIXES, MetaphlanProfile


class MetaphlanProfileReader(ProfileReader):
    """Define a reader for Metaphlan profiles."""

    LARGE_INTEGER = int(10e6)

    @classmethod
    def read(cls, profile: ProfileSource) -> DataFrame[MetaphlanProfile]:
        """Read a metaphlan taxonomic profile from a file."""
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=None,
            index_col=False,
            comment="#",
        )
        if len(result.columns) == 4:
            result.columns = [
                "clade_name",
                "taxonomy_id",
                "relative_abundance",
                "additional_species",
            ]
        else:
            raise ValueError(
                f"Unexpected metaphlan report format. It has {len(result.columns)} "
                f"columns but only 4 are expected."
            )

        result = result.assign(
            rank=result.clade_name.str.split("|").str[-1].str[0].map(RANK_PREFIXES),
            count=result.relative_abundance.map(lambda x: int(x * cls.LARGE_INTEGER)),
        )
        return result