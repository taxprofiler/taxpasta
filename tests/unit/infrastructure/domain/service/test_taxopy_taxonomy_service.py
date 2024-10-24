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


"""Test that the taxopy taxonomy service works as expected."""

from collections import OrderedDict
from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from taxpasta.infrastructure.domain.service.taxopy_taxonomy_service import (
    TaxopyTaxonomyService,
)


@pytest.fixture(scope="module")
def tax_service(taxonomy_data_dir: Path) -> TaxopyTaxonomyService:
    """Provide an instance of the taxopy taxonomy service."""
    return TaxopyTaxonomyService.from_taxdump(taxonomy_data_dir)


@pytest.mark.parametrize(
    ("tax_id", "expected"),
    [
        (1, "root"),
        (42, None),
        (86398254, "Pseudomonadales"),
        (432158898, "Ascomycota"),
        (492356122, "Saccharomyces cerevisiae"),
        (1945799576, "Escherichia coli"),
        (1887621118, "Pseudomonas putida"),
    ],
)
def test_get_taxon_name(tax_service: TaxopyTaxonomyService, tax_id: int, expected: str):
    """Expect that we can retrieve the correct taxon name."""
    assert tax_service.get_taxon_name(tax_id) == expected


@pytest.mark.parametrize(
    ("tax_id", "expected"),
    [
        (1, "no rank"),
        (42, None),
        (476817098, "superkingdom"),
        (432158898, "phylum"),
        (329474883, "class"),
        (86398254, "order"),
        (87250111, "family"),
        (933264868, "genus"),
        (1887621118, "species"),
    ],
)
def test_get_taxon_rank(tax_service: TaxopyTaxonomyService, tax_id: int, expected: str):
    """Expect that we can retrieve the correct taxon rank."""
    assert tax_service.get_taxon_rank(tax_id) == expected


@pytest.mark.parametrize(
    ("tax_id", "expected"),
    [
        (1, []),
        (42, None),
        (
            86398254,
            [
                "Bacteria",
                "Proteobacteria",
                "Gammaproteobacteria",
                "Pseudomonadales",
            ],
        ),
        (1199096325, ["Eukaryota", "Ascomycota", "Saccharomycetes"]),
    ],
)
def test_get_taxon_name_lineage(
    tax_service: TaxopyTaxonomyService,
    tax_id: int,
    expected: list[str],
):
    """Expect that we can retrieve the correct taxon name lineage."""
    assert tax_service.get_taxon_name_lineage(tax_id) == expected


@pytest.mark.parametrize(
    ("tax_id", "expected"),
    [
        (1, []),
        (42, None),
        (86398254, [609216830, 1641076285, 329474883, 86398254]),
        (1199096325, [476817098, 432158898, 1199096325]),
    ],
)
def test_get_taxon_identifier_lineage(
    tax_service: TaxopyTaxonomyService,
    tax_id: int,
    expected: list[int],
):
    """Expect that we can retrieve the correct taxon identifier lineage."""
    assert tax_service.get_taxon_identifier_lineage(tax_id) == expected


@pytest.mark.parametrize(
    ("tax_id", "expected"),
    [
        (1, []),
        (42, None),
        (86398254, ["superkingdom", "phylum", "class", "order"]),
        (1199096325, ["superkingdom", "phylum", "class"]),
    ],
)
def test_get_taxon_rank_lineage(
    tax_service: TaxopyTaxonomyService,
    tax_id: int,
    expected: list[str],
):
    """Expect that we can retrieve the correct taxon rank lineage."""
    assert tax_service.get_taxon_rank_lineage(tax_id) == expected


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (
            pd.DataFrame(OrderedDict([("taxonomy_id", [1, 42, 86398254, 1199096325])])),
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", [1, 42, 86398254, 1199096325]),
                        (
                            "lineage",
                            [
                                None,
                                None,
                                "Bacteria;Proteobacteria;Gammaproteobacteria;"
                                "Pseudomonadales",
                                "Eukaryota;Ascomycota;Saccharomycetes",
                            ],
                        ),
                    ],
                ),
            ),
        ),
    ],
)
def test_add_name_lineage(
    tax_service: TaxopyTaxonomyService,
    result: pd.DataFrame,
    expected: pd.DataFrame,
):
    """Expect that we can add name lineages to a result table."""
    assert_frame_equal(tax_service.add_name_lineage(result), expected)


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (
            pd.DataFrame(OrderedDict([("taxonomy_id", [1, 42, 86398254, 1199096325])])),
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", [1, 42, 86398254, 1199096325]),
                        (
                            "id_lineage",
                            [
                                None,
                                None,
                                "609216830;1641076285;329474883;86398254",
                                "476817098;432158898;1199096325",
                            ],
                        ),
                    ],
                ),
            ),
        ),
    ],
)
def test_add_identifier_lineage(
    tax_service: TaxopyTaxonomyService,
    result: pd.DataFrame,
    expected: pd.DataFrame,
):
    """Expect that we can add identifier lineages to a result table."""
    assert_frame_equal(tax_service.add_identifier_lineage(result), expected)


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (
            pd.DataFrame(OrderedDict([("taxonomy_id", [1, 42, 86398254, 1199096325])])),
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", [1, 42, 86398254, 1199096325]),
                        (
                            "rank_lineage",
                            [
                                None,
                                None,
                                "superkingdom;phylum;class;order",
                                "superkingdom;phylum;class",
                            ],
                        ),
                    ],
                ),
            ),
        ),
    ],
)
def test_add_rank_lineage(
    tax_service: TaxopyTaxonomyService,
    result: pd.DataFrame,
    expected: pd.DataFrame,
):
    """Expect that we can add rank lineages to a result table."""
    assert_frame_equal(tax_service.add_rank_lineage(result), expected)


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (
            pd.DataFrame(
                OrderedDict(
                    [("taxonomy_id", [1, 42, 1887621118, 1945799576, 492356122])],
                ),
            ),
            [
                {"taxonomy": [""] * 7},
                {"taxonomy": [""] * 7},
                {
                    "taxonomy": [
                        "Bacteria",
                        "Proteobacteria",
                        "Gammaproteobacteria",
                        "Pseudomonadales",
                        "Pseudomonadaceae",
                        "Pseudomonas",
                        "Pseudomonas putida",
                    ],
                },
                {
                    "taxonomy": [
                        "Bacteria",
                        "Proteobacteria",
                        "Gammaproteobacteria",
                        "Enterobacterales",
                        "Enterobacteriaceae",
                        "Escherichia",
                        "Escherichia coli",
                    ],
                },
                {
                    "taxonomy": [
                        "Eukaryota",
                        "Ascomycota",
                        "Saccharomycetes",
                        "Saccharomycetales",
                        "Saccharomycetaceae",
                        "Saccharomyces",
                        "Saccharomyces cerevisiae",
                    ],
                },
            ],
        ),
    ],
)
def test_format_biom_taxonomy(
    tax_service: TaxopyTaxonomyService,
    result: pd.DataFrame,
    expected: list[dict[str, list[str]]],
):
    """Expect that we can add rank lineages to a result table."""
    assert tax_service.format_biom_taxonomy(result)[0] == expected
