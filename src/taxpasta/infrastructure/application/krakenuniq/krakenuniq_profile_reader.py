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


"""Provide a reader for KrakenUniq profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader

from .krakenuniq_profile import KrakenUniqProfile


class KrakenUniqProfileReader(ProfileReader):
    """Define a reader for KrakenUniq profiles."""

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[KrakenUniqProfile]:
        """
        Read a krakenUniq taxonomic profile from the given source.

        Args:
            profile: A source that contains a tab-separated taxonomic profile generated
                by KrakenUniq.

        Returns:
            A data frame representation of the KrakenUniq profile.

        Raises:
            ValueError: In case the table does not contain exactly nine columns.

        """
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            header=0,
            index_col=False,
            comment="#",
            dtype={"taxID": str},
            skipinitialspace=True,
        )
        if len(result.columns) == 9:
            result.columns = [
                KrakenUniqProfile.percent,
                KrakenUniqProfile.reads,
                KrakenUniqProfile.taxReads,
                KrakenUniqProfile.kmers,
                KrakenUniqProfile.dup,
                KrakenUniqProfile.cov,
                KrakenUniqProfile.taxID,
                KrakenUniqProfile.rank,
                KrakenUniqProfile.taxName,
            ]
        else:
            raise ValueError(
                f"Unexpected KrakenUniq report format. It has {len(result.columns)} "
                f"columns but only 9 are expected."
            )
        return result