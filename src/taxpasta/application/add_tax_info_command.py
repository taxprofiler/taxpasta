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
from typing import Optional

from taxpasta.domain.model import Sample
from taxpasta.domain.service import TaxonomyService


@dataclass(frozen=True)
class AddTaxInfoCommand:
    """Define a command object for adding taxonomy information."""

    taxonomy_service: Optional[TaxonomyService] = None
    summarise_at: Optional[str] = None
    add_name: bool = False
    add_rank: bool = False
    add_lineage: bool = False
    add_id_lineage: bool = False
    add_rank_lineage: bool = False

    def execute(self, sample: Sample) -> Sample:
        """Execute the command to add taxonomy information."""
        if self.taxonomy_service is None:
            return sample
        # The order of the following conditions is chosen specifically to yield a
        # pleasant final output format.
        result = sample
        if self.add_rank_lineage:
            result = Sample(
                name=result.name,
                profile=self.taxonomy_service.add_rank_lineage(result.profile),
            )
        if self.add_id_lineage:
            result = Sample(
                name=result.name,
                profile=self.taxonomy_service.add_identifier_lineage(result.profile),
            )
        if self.add_lineage:
            result = Sample(
                name=result.name,
                profile=self.taxonomy_service.add_name_lineage(result.profile),
            )
        if self.add_rank:
            result = Sample(
                name=result.name, profile=self.taxonomy_service.add_rank(result.profile)
            )
        if self.add_name:
            result = Sample(
                name=result.name, profile=self.taxonomy_service.add_name(result.profile)
            )
        return result

    def __post_init__(self) -> None:
        """Perform post initialization validation."""
        no_taxonomy = self.taxonomy_service is None
        if self.summarise_at is not None and no_taxonomy:
            raise ValueError(
                "The summarising feature '--summarise-at' requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
        if self.add_name and no_taxonomy:
            raise ValueError(
                "The '--add-name' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
        if self.add_rank and no_taxonomy:
            raise ValueError(
                "The '--add-rank' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
        if self.add_lineage and no_taxonomy:
            raise ValueError(
                "The '--add-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
        if self.add_id_lineage and no_taxonomy:
            raise ValueError(
                "The '--add-id-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
        if self.add_rank_lineage and no_taxonomy:
            raise ValueError(
                "The '--add-rank-lineage' option requires a taxonomy. Please "
                "provide one using the option '--taxonomy'."
            )
