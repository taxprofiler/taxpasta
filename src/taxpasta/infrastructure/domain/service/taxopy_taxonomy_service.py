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


"""Provide a taxonomy service based on taxopy."""


from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd
import taxopy
from pandera.typing import DataFrame

from taxpasta.domain.model import StandardProfile
from taxpasta.domain.service import ResultTable, TaxonomyService


class TaxopyTaxonomyService(TaxonomyService):
    """Define the taxonomy service based on taxopy."""

    def __init__(self, *, tax_db: taxopy.TaxDb, **kwargs) -> None:
        """Initialize a taxonomy service instance with a taxopy database."""
        super().__init__(**kwargs)
        self._tax_db = tax_db

    @classmethod
    def from_taxdump(cls, source: Path) -> TaxopyTaxonomyService:
        """Create a service instance from a directory path containing taxdump info."""
        return cls(
            tax_db=taxopy.TaxDb(
                nodes_dmp=str(source / "nodes.dmp"),
                names_dmp=str(source / "names.dmp"),
                merged_dmp=str(source / "merged.dmp")
                if (source / "merged.dmp").is_file()
                else None,
            )
        )

    def add_name(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon name to the given table."""
        return table.copy().assign(
            name=lambda df: df.taxonomy_id.map(self._tax_db.taxid2name)
        )

    def add_rank(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon rank to the given table."""
        return table.copy().assign(
            rank=lambda df: df.taxonomy_id.map(self._tax_db.taxid2rank)
        )

    def add_name_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage to the given table."""
        return table.copy().assign(
            lineage=lambda df: df.taxonomy_id.map(self._name_lineage_as_str)
        )

    def _name_lineage_as_str(self, taxonomy_id: int) -> str:
        """Return the lineage of a taxon as concatenated names."""
        taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        return ";".join(taxon.name_lineage)

    def add_identifier_lineage(
        self, table: DataFrame[ResultTable]
    ) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage as identifiers to the given table."""
        return table.copy().assign(
            lineage=lambda df: df.taxonomy_id.map(self._taxid_lineage_as_str)
        )

    def _taxid_lineage_as_str(self, taxonomy_id: int) -> str:
        """Return the lineage of a taxon as concatenated identifiers."""
        taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        return ";".join([str(tax_id) for tax_id in taxon.taxid_lineage])

    def summarise_at(
        self, profile: DataFrame[StandardProfile], rank: str
    ) -> DataFrame[StandardProfile]:
        """Summarise a standardised abundance profile at a higher taxonomic rank."""
        branching = defaultdict(list)
        for tax_id in profile[StandardProfile.taxonomy_id]:
            # For now, we ignore the identifier zero (unclassified).
            if tax_id == 0:
                continue
            taxon = taxopy.Taxon(taxid=tax_id, taxdb=self._tax_db)
            for parent_id in taxon.taxid_lineage:
                ancestor_rank = self._tax_db.taxid2rank[parent_id]
                if ancestor_rank == rank:
                    # We do not need to summarize further than to the desired rank.
                    branching[parent_id].append(taxon.taxid)
                    break
            else:
                # We did not encounter the desired rank.
                raise ValueError(
                    f"The desired rank '{rank}' is not in the lineage of the taxonomy "
                    f"identifier {taxon.taxid}."
                )
        finalized = dict(branching)
        root_ids = sorted(finalized)
        counts = []
        for root_id in root_ids:
            leaves = finalized[root_id]
            counts.append(
                profile.loc[
                    profile[StandardProfile.taxonomy_id].isin(leaves),
                    StandardProfile.count,
                ].sum()
            )
        return pd.DataFrame(
            {
                StandardProfile.taxonomy_id: pd.Series(data=root_ids, dtype="category"),
                StandardProfile.count: counts,
            }
        )
