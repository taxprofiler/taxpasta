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


"""Provide a reader for metaphlan profiles."""

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader

from .metaphlan_profile import MetaphlanProfile


class MetaphlanProfileReader(ProfileReader):
    """Define a reader for Metaphlan profiles."""

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[MetaphlanProfile]:
        """Read a metaphlan taxonomic profile from a file."""
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            skiprows=4,
            header=None,
            index_col=False,
            names=[
                MetaphlanProfile.clade_name,
                MetaphlanProfile.ncbi_tax_id,
                MetaphlanProfile.relative_abundance,
                MetaphlanProfile.additional_species,
            ],
            dtype={MetaphlanProfile.ncbi_tax_id: str},
        )
        cls._check_num_columns(result, MetaphlanProfile)
        return result
