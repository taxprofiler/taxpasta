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


"""Provide a reader for kraken2 profiles."""


from pathlib import Path

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application import ProfileReader

from .kraken2_profile import Kraken2Profile


class Kraken2ProfileReader(ProfileReader):
    """Define a reader for kraken2 profiles."""

    @classmethod
    def read(cls, profile: Path) -> DataFrame[Kraken2Profile]:
        """Read a kraken2 taxonomic profile from a file."""
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=None,
            index_col=False,
        )
        if len(result.columns) == 6:
            result.columns = [
                "percent",
                "clade_assigned_reads",
                "direct_assigned_reads",
                "rank",
                "taxonomy_id",
                "name",
            ]
        elif len(result.columns) == 8:
            result.columns = [
                "percent",
                "clade_assigned_reads",
                "direct_assigned_reads",
                "num_minimizers",
                "distinct_minimizers",
                "rank",
                "taxonomy_id",
                "name",
            ]
        else:
            raise ValueError(
                f"Unexpected kraken2 report format. It has {len(result.columns)} "
                f"columns but only 6 or 8 are expected."
            )
        return result
