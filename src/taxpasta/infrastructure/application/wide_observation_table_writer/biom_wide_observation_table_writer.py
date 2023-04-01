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


"""Provide a Biological Observation Matrix (BIOM) writer."""


from datetime import datetime
from typing import Optional

from biom.table import Table
from biom.util import biom_open
from pandera.typing import DataFrame

from taxpasta.application.service import Filepath, WideObservationTableWriter
from taxpasta.domain.model import WideObservationTable
from taxpasta.domain.service import TaxonomyService


class BIOMWideObservationTableWriter(WideObservationTableWriter):
    """Define the Biological Observation Matrix (BIOM) writer."""

    @classmethod
    def write(
        cls,
        matrix: DataFrame[WideObservationTable],
        target: Filepath,
        taxonomy: Optional[TaxonomyService] = None,
        generated_by: str = "taxpasta",
        **kwargs,
    ) -> None:
        """Write the given data to the given buffer or file."""
        # Drop unclassified reads.
        matrix = matrix.loc[matrix.iloc[:, 0] != 0].copy()
        if taxonomy is not None:
            observation_meta = None
            # FIXME (Moritz): All lists need to be of equal length, i.e., per key in
            #  the dict across all observations (aka samples).
        else:
            observation_meta = None
        result = Table(
            data=matrix.iloc[:, 1:].values,
            observation_ids=matrix.iloc[:, 0].astype(str),
            sample_ids=matrix.columns[1:],
            observation_metadata=observation_meta,
            create_date=datetime.utcnow().isoformat(timespec="microseconds"),
        )
        with biom_open(str(target), permission="w") as handle:
            result.to_hdf5(handle, generated_by=generated_by)
