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


"""Provide a command object for adding taxonomy information."""

from dataclasses import dataclass
from typing import Optional, TypeVar

from pandera.typing import DataFrame

from taxpasta.domain.model import (
    StandardProfile,
    TidyObservationTable,
    WideObservationTable,
)
from taxpasta.domain.service import TaxonomyService


Table = TypeVar(
    "Table",
    DataFrame[TidyObservationTable],
    DataFrame[WideObservationTable],
    DataFrame[StandardProfile],
)


@dataclass(frozen=True)
class AddTaxInfoCommand:
    """Define the command object for adding taxonomy information."""

    taxonomy_service: Optional[TaxonomyService] = None
    summarise_at: Optional[str] = None
    add_name: bool = False
    add_rank: bool = False
    add_lineage: bool = False
    add_id_lineage: bool = False
    add_rank_lineage: bool = False

    def execute(self, table: Table) -> Table:
        """Execute the command to add taxonomy information."""
        if self.taxonomy_service is None:
            return table
        # The order of the following conditions is chosen specifically to yield a
        # pleasant final output format.
        result = table
        if self.add_rank_lineage:
            result = self.taxonomy_service.add_rank_lineage(result)
        if self.add_id_lineage:
            result = self.taxonomy_service.add_identifier_lineage(result)
        if self.add_lineage:
            result = self.taxonomy_service.add_name_lineage(result)
        if self.add_rank:
            result = self.taxonomy_service.add_rank(result)
        if self.add_name:
            result = self.taxonomy_service.add_name(result)
        return result

    def __post_init__(self) -> None:
        """Perform post initialization validation."""
        no_taxonomy = self.taxonomy_service is None
        if self.summarise_at is not None and no_taxonomy:
            msg = (
                "The summarising feature '--summarise-at' requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
        if self.add_name and no_taxonomy:
            msg = (
                "The '--add-name' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
        if self.add_rank and no_taxonomy:
            msg = (
                "The '--add-rank' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
        if self.add_lineage and no_taxonomy:
            msg = (
                "The '--add-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
        if self.add_id_lineage and no_taxonomy:
            msg = (
                "The '--add-id-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
        if self.add_rank_lineage and no_taxonomy:
            msg = (
                "The '--add-rank-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
            raise ValueError(msg)
