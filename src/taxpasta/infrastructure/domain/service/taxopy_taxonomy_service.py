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


"""Provide a taxonomy model based on taxopy."""


from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import networkx as nx
import pandas as pd
import taxopy
from pandera.typing import DataFrame

from taxpasta.domain.model import StandardProfile
from taxpasta.domain.service import ResultTable, TaxonomyService


class TaxopyTaxonomyService(TaxonomyService):
    """Define the taxonomy model based on taxopy."""

    def __init__(self, *, tax_db: taxopy.TaxDb, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)
        self._tax_db = tax_db

    @classmethod
    def from_taxdump(cls, source: Path) -> TaxopyTaxonomyService:
        """"""
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
        """"""
        return table.copy().assign(
            name=lambda df: df[ResultTable.taxonomy_id].map(self._tax_db.taxid2name)
        )

    def add_rank(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""
        return table.copy().assign(
            rank=lambda df: df[ResultTable.taxonomy_id].map(self._tax_db.taxid2rank)
        )

    def add_name_lineage(self, table: DataFrame[ResultTable]) -> DataFrame[ResultTable]:
        """"""
        return table.copy().assign(
            lineage=lambda df: df[ResultTable.taxonomy_id].map(
                self._name_lineage_as_str
            )
        )

    def _name_lineage_as_str(self, taxonomy_id: int) -> str:
        """"""
        taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        return ";".join(taxon.name_lineage)

    def add_taxid_lineage(
        self, table: DataFrame[ResultTable]
    ) -> DataFrame[ResultTable]:
        """"""
        return table.copy().assign(
            lineage=lambda df: df[ResultTable.taxonomy_id].map(
                self._taxid_lineage_as_str
            )
        )

    def _taxid_lineage_as_str(self, taxonomy_id: int) -> str:
        """"""
        taxon = taxopy.Taxon(taxid=taxonomy_id, taxdb=self._tax_db)
        return ";".join([str(tax_id) for tax_id in taxon.taxid_lineage])

    def summarise_at(
        self, profile: DataFrame[StandardProfile], rank: str
    ) -> DataFrame[StandardProfile]:
        """Summarise a standardised abundance profile at a higher taxonomic rank."""
        branching = nx.DiGraph()
        rank2ids = defaultdict(list)
        for tax_id in profile[StandardProfile.taxonomy_id]:
            taxon = taxopy.Taxon(taxid=tax_id, taxdb=self._tax_db)
            rank2ids[taxon.rank].append(taxon.taxid)
            child_id = taxon.taxid
            for parent_id in taxon.taxid_lineage:
                ancestor_rank = self._tax_db.taxid2rank[parent_id]
                rank2ids[ancestor_rank].append(parent_id)
                branching.add_edge(parent_id, child_id)
                if ancestor_rank == rank:
                    # We do not need to summarize further than to the desired rank.
                    break
            else:
                # We did not encounter the desired rank.
                raise ValueError(
                    f"The desired rank '{rank}' is not in the lineage of the taxonomy "
                    f"identifier {taxon.taxid}."
                )
        finalized_rank2ids = dict(rank2ids)
        # A branching is a directed forest (acyclic graph) with each node having, at
        # most, one parent. So the maximum in-degree is equal to one. In our branching,
        # the nodes of desired rank must each be the root node, i.e., with in-degree of
        # zero, of their own arborescence, i.e., a directed tree which is a weakly
        # connected forest, and all the leaf nodes, i.e., with out-degree of zero, in
        # our branching must correspond to the original abundance profile.
        # See https://networkx.org/documentation/stable/reference/algorithms/tree.html
        # for the definitions.
        root_ids = finalized_rank2ids[rank]
        counts = []
        for tax_id in root_ids:
            arborescence = []
            for _, children in nx.dfs_successors(branching, tax_id).items():
                arborescence.extend(children)
            # We could further restrict the arborescence to only the leaf nodes by
            # filtering on the out-degree but instead, we rely on other nodes not being
            # in the abundance profile.
            counts.append(
                profile.loc[
                    profile[StandardProfile.taxonomy_id].isin(arborescence),
                    StandardProfile.count,
                ].sum()
            )
        return pd.DataFrame(
            {
                StandardProfile.taxonomy_id: pd.Series(data=root_ids, dtype="category"),
                StandardProfile.count: counts,
            }
        )
