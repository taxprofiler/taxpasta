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


"""Provide an abstract taxonomy service interface."""


from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar

from pandera.typing import DataFrame

from ..model import StandardProfile, TidyObservationTable, WideObservationTable


ResultTable = TypeVar(
    "ResultTable", TidyObservationTable, WideObservationTable, StandardProfile
)


class TaxonomyService(ABC):
    """Define the abstract taxonomy service interface."""

    def __init__(self, **kwargs) -> None:
        """Initialize a taxonomy service instance."""
        super().__init__(**kwargs)

    @abstractmethod
    def get_taxon_name(self, taxonomy_id: int) -> Optional[str]:
        """Return the name of a given taxonomy identifier."""

    @abstractmethod
    def get_taxon_rank(self, taxonomy_id: int) -> Optional[str]:
        """Return the rank of a given taxonomy identifier."""

    @abstractmethod
    def get_taxon_name_lineage(self, taxonomy_id: int) -> Optional[List[str]]:
        """Return the lineage of a given taxonomy identifier as names."""

    @abstractmethod
    def get_taxon_identifier_lineage(self, taxonomy_id: int) -> Optional[List[int]]:
        """Return the lineage of a given taxonomy identifier as identifiers."""

    @abstractmethod
    def add_name(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon name to the given table."""

    @abstractmethod
    def add_rank(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon rank to the given table."""

    @abstractmethod
    def add_name_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage to the given table."""

    @abstractmethod
    def add_identifier_lineage(
        self, table: DataFrame[ResultTable]
    ) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage as identifiers to the given table."""

    @abstractmethod
    def summarise_at(
        self, profile: DataFrame[StandardProfile], rank: str
    ) -> DataFrame[StandardProfile]:
        """Summarise a standardised abundance profile at a higher taxonomic rank."""
