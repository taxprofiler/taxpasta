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


"""Provide a taxonomy model."""


from abc import ABC, abstractmethod
from typing import TypeVar

from pandera.typing import DataFrame

from ..model import StandardProfile, TidyObservationTable, WideObservationTable


ResultTable = TypeVar("ResultTable", TidyObservationTable, WideObservationTable)


class TaxonomyService(ABC):
    """Define a taxonomy model."""

    def __init__(self, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)

    @abstractmethod
    def add_name(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""

    @abstractmethod
    def add_rank(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""

    @abstractmethod
    def add_name_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""

    @abstractmethod
    def add_identifier_lineage(
        self, table: DataFrame[ResultTable]
    ) -> DataFrame[ResultTable]:
        """"""

    def add_taxonomy(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""
        return table.pipe(self.add_name).pipe(self.add_rank).pipe(self.add_name_lineage)

    @abstractmethod
    def summarise_at(
        self, profile: DataFrame[StandardProfile], rank: str
    ) -> DataFrame[StandardProfile]:
        """Summarise a standardised abundance profile at a higher taxonomic rank."""
