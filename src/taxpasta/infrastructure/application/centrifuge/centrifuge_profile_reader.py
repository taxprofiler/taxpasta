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


"""Provide a reader for Centrifuge profiles."""


import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application import BufferOrFilepath, ProfileReader

from .centrifuge_profile import CentrifugeProfile


class CentrifugeProfileReader(ProfileReader):
    """Define a reader for centrifuge profiles."""

    @classmethod
    def read(cls, profile: BufferOrFilepath) -> DataFrame[CentrifugeProfile]:
        """
        Read a centrifuge taxonomic profile from the given source.

        Args:
            profile: A source that contains a tab-separated taxonomic profile generated
                by centrifuge.

        Returns:
            A data frame representation of the centrifuge profile.

        Raises:
            ValueError: In case the table does not contain exactly six.

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
                CentrifugeProfile.percent,
                CentrifugeProfile.clade_assigned_reads,
                CentrifugeProfile.direct_assigned_reads,
                CentrifugeProfile.taxonomy_level,
                CentrifugeProfile.taxonomy_id,
                CentrifugeProfile.name,
            ]
        else:
            raise ValueError(
                f"Unexpected centrifuge report format. It has {len(result.columns)} "
                f"columns but only 6 are expected."
            )
        return result
