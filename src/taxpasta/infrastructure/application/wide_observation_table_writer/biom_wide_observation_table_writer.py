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

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from biom.table import Table
from biom.util import biom_open

from taxpasta import __version__
from taxpasta.application.service import Filepath, WideObservationTableWriter


if TYPE_CHECKING:
    from pandera.typing import DataFrame

    from taxpasta.domain.model import WideObservationTable
    from taxpasta.domain.service import TaxonomyService

GENERATED_BY = f"taxpasta=={__version__}"


class BIOMWideObservationTableWriter(WideObservationTableWriter):
    """Define the Biological Observation Matrix (BIOM) writer."""

    @classmethod
    def write(
        cls,
        matrix: DataFrame[WideObservationTable],
        target: Filepath,
        taxonomy: TaxonomyService | None = None,
        generated_by: str = GENERATED_BY,
        **kwargs,  # noqa: ARG003
    ) -> None:
        """Write the given data to the given buffer or file."""
        # Drop unclassified reads.
        matrix = matrix.loc[matrix.iloc[:, 0] != 0].copy()
        if taxonomy is not None:
            observation_meta, ranks = taxonomy.format_biom_taxonomy(matrix)
            observation_group_meta = {"ranks": ("csv", ";".join(ranks))}
        else:
            observation_meta = None
            observation_group_meta = None
        result = Table(
            data=matrix.iloc[:, 1:].values,
            observation_ids=matrix.iloc[:, 0].astype(str),
            sample_ids=matrix.columns[1:].astype(str),
            observation_metadata=observation_meta,
            observation_group_metadata=observation_group_meta,
            create_date=datetime.now(tz=timezone.utc).isoformat(
                timespec="microseconds",
            ),
        )
        with biom_open(str(target), permission="w") as handle:
            result.to_hdf5(handle, generated_by=generated_by)
