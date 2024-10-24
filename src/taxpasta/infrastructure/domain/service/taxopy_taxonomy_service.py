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

import logging
from collections import defaultdict
from typing import TYPE_CHECKING

import pandas as pd
import taxopy
from taxopy.exceptions import TaxidError

from taxpasta.domain.model import StandardProfile
from taxpasta.domain.service import ResultTable, TaxonomyService


if TYPE_CHECKING:
    from pathlib import Path

    from pandera.typing import DataFrame


logger = logging.getLogger(__name__)


class TaxopyTaxonomyService(TaxonomyService):
    """Define the taxonomy service based on taxopy."""

    def __init__(self, *, tax_db: taxopy.TaxDb, **kwargs) -> None:
        """Initialize a taxonomy service instance with a taxopy database."""
        super().__init__(**kwargs)
        self._tax_db = tax_db

    @classmethod
    def from_taxdump(cls, source: Path) -> TaxopyTaxonomyService:
        """Create a service instance from a directory path containing taxdump info."""
        merged = source / "merged.dmp"
        return cls(
            tax_db=taxopy.TaxDb(
                names_dmp=str(source / "names.dmp"),
                nodes_dmp=str(source / "nodes.dmp"),
                merged_dmp=str(merged) if merged.is_file() else None,
                keep_files=True,
            ),
        )

    def get_taxon_name(self, taxonomy_id: int) -> str | None:
        """Return the name of a given taxonomy identifier."""
        return self._tax_db.taxid2name.get(taxonomy_id)

    def get_taxon_rank(self, taxonomy_id: int) -> str | None:
        """Return the rank of a given taxonomy identifier."""
        return self._tax_db.taxid2rank.get(taxonomy_id)

    def get_taxon_name_lineage(self, taxonomy_id: int) -> list[str] | None:
        """
        Return the lineage of a given taxonomy identifier as names.

        Only names with associated ranks are included.

        """
        try:
            taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        except TaxidError:
            return None
        # We reverse the ordering of the ranks and ignore the root by starting at the
        # second-highest rank.
        return [name for _, name in taxon.ranked_name_lineage[-2::-1]]

    def get_taxon_identifier_lineage(self, taxonomy_id: int) -> list[int] | None:
        """
        Return the lineage of a given taxonomy identifier as identifiers.

        Only identifiers with associated ranks are included.

        """
        try:
            taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        except TaxidError:
            return None
        # We reverse the ordering of the lineage and ignore the root by starting at the
        # second-highest rank.
        return [name for _, name in taxon.ranked_taxid_lineage[-2::-1]]

    def get_taxon_rank_lineage(self, taxonomy_id: int) -> list[str] | None:
        """Return the lineage of a given taxonomy identifier as ranks."""
        try:
            taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        except TaxidError:
            return None
        # We reverse the ordering of the ranks and ignore the root by starting at the
        # second-highest rank.
        return taxon.rank_lineage[-2::-1]

    def add_name(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon name to the given table."""
        result = table.copy()
        result.insert(
            1,
            "name",
            table.taxonomy_id.map(self._tax_db.taxid2name),
        )
        return result

    def add_rank(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon rank to the given table."""
        result = table.copy()
        result.insert(
            1,
            "rank",
            table.taxonomy_id.map(self._tax_db.taxid2rank),
        )
        return result

    def add_name_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage to the given table."""
        result = table.copy()
        result.insert(
            1,
            "lineage",
            table.taxonomy_id.map(self._name_lineage_as_str),
        )
        return result

    def _name_lineage_as_str(self, taxonomy_id: int) -> str | None:
        """Return the lineage of a taxon as concatenated names."""
        if lineage := self.get_taxon_name_lineage(taxonomy_id):
            return ";".join(lineage)

        return None

    def add_identifier_lineage(
        self,
        table: DataFrame[ResultTable],
    ) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage as identifiers to the given table."""
        result = table.copy()
        result.insert(
            1,
            "id_lineage",
            table.taxonomy_id.map(self._taxid_lineage_as_str),
        )
        return result

    def _taxid_lineage_as_str(self, taxonomy_id: int) -> str | None:
        """Return the lineage of a taxon as concatenated identifiers."""
        if lineage := self.get_taxon_identifier_lineage(taxonomy_id):
            return ";".join(str(tax_id) for tax_id in lineage)

        return None

    def add_rank_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """Add a column for the taxon lineage as ranks to the given table."""
        result = table.copy()
        result.insert(
            1,
            "rank_lineage",
            table.taxonomy_id.map(self._rank_lineage_as_str),
        )
        return result

    def _rank_lineage_as_str(self, taxonomy_id: int) -> str | None:
        """Return the rank lineage of a taxon as concatenated identifiers."""
        if lineage := self.get_taxon_rank_lineage(taxonomy_id):
            return ";".join(lineage)

        return None

    def format_biom_taxonomy(
        self,
        table: DataFrame[ResultTable],
    ) -> tuple[list[dict[str, list[str]]], list[str]]:
        """Format the taxonomy as BIOM observation metadata."""
        lineages = [self._get_rank_name_lineage(tax_id) for tax_id in table.taxonomy_id]
        longest_lineage = max(lineages, key=len)
        max_ranks = [rank for rank, _ in longest_lineage]
        return [
            {"taxonomy": self._pad_lineage(lineage, max_ranks)} for lineage in lineages
        ], max_ranks

    def _get_rank_name_lineage(self, taxonomy_id: int) -> list[tuple[str, str]]:
        try:
            taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        except TaxidError:
            return []
        return taxon.ranked_name_lineage[-2::-1]

    def _pad_lineage(
        self,
        lineage: list[tuple[str, str]],
        max_ranks: list[str],
    ) -> list[str]:
        """Pad a lineage to match the length of the longest lineage."""
        # Poor implementation of aligning ranks. We pad missing ranks with empty
        # strings.
        lineage_idx = 0
        ranks_idx = 0
        result = []
        while lineage_idx < len(lineage) and ranks_idx < len(max_ranks):
            rank, name = lineage[lineage_idx]
            if rank == max_ranks[ranks_idx]:
                result.append(name)
                lineage_idx += 1
                ranks_idx += 1
            else:
                result.append("")
                ranks_idx += 1
        # We pad any remaining ranks with empty strings.
        return result + [""] * (len(max_ranks) - len(result))

    def summarise_at(
        self,
        profile: DataFrame[StandardProfile],
        rank: str,
    ) -> DataFrame[StandardProfile]:
        """Summarise a standardised abundance profile at a higher taxonomic rank."""
        branching = defaultdict(list)
        for tax_id in profile[StandardProfile.taxonomy_id]:
            # For now, we ignore the identifier zero (unclassified).
            if tax_id == 0:
                continue
            taxon = taxopy.Taxon(taxid=tax_id, taxdb=self._tax_db)
            if taxon.rank == rank:
                branching[taxon.taxid].append(taxon.taxid)
                continue
            for parent_id in taxon.taxid_lineage:
                ancestor_rank = self._tax_db.taxid2rank[parent_id]
                if ancestor_rank == rank:
                    # We do not need to summarize further than to the desired rank.
                    branching[parent_id].append(taxon.taxid)
                    break
            else:
                # We did not encounter the desired rank. Likely, the taxon is situated
                # above the desired rank in the taxonomy.
                logger.debug(
                    "The desired rank '%s' is not in the lineage of the taxon %d - %s.",
                    rank,
                    taxon.taxid,
                    taxon.name,
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
                ].sum(),
            )
        return pd.DataFrame(
            {
                StandardProfile.taxonomy_id: pd.Series(data=root_ids, dtype="category"),
                StandardProfile.count: counts,
            },
        )
