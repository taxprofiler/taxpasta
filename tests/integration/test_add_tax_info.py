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


"""Test the command object for adding taxonomy information."""


from pathlib import Path

import pandas as pd
import pytest
from pandera.typing import DataFrame

from taxpasta.application import AddTaxInfoCommand
from taxpasta.domain.model import StandardProfile
from taxpasta.infrastructure.domain.service.taxopy_taxonomy_service import (
    TaxopyTaxonomyService,
)


@pytest.fixture(scope="module")
def tax_service(taxonomy_data_dir: Path) -> TaxopyTaxonomyService:
    """Provide an instance of the taxopy taxonomy service."""
    return TaxopyTaxonomyService.from_taxdump(taxonomy_data_dir)


@pytest.fixture(scope="module")
def profile() -> DataFrame[StandardProfile]:
    """Provide a generic profile to modify."""
    return pd.DataFrame({"taxonomy_id": [1, 476817098, 609216830], "count": [1, 2, 3]})


def test_add_name(tax_service: TaxopyTaxonomyService, profile: pd.DataFrame):
    """Test that a column with taxon names is added."""
    command = AddTaxInfoCommand(add_name=True, taxonomy_service=tax_service)
    result = command.execute(profile)
    assert "name" in result.columns
    assert result["name"].tolist() == ["root", "Eukaryota", "Bacteria"]


def test_add_rank(tax_service: TaxopyTaxonomyService, profile: pd.DataFrame):
    """Test that a column with taxon ranks is added."""
    command = AddTaxInfoCommand(add_rank=True, taxonomy_service=tax_service)
    result = command.execute(profile)
    assert "rank" in result.columns
    assert result["rank"].tolist() == ["no rank", "superkingdom", "superkingdom"]


def test_add_lineage(tax_service: TaxopyTaxonomyService, profile: pd.DataFrame):
    """Test that a column with taxon lineages is added."""
    command = AddTaxInfoCommand(add_lineage=True, taxonomy_service=tax_service)
    result = command.execute(profile)
    assert "lineage" in result.columns
    assert result["lineage"].tolist() == [None, "Eukaryota", "Bacteria"]


def test_add_id_lineage(tax_service: TaxopyTaxonomyService, profile: pd.DataFrame):
    """Test that a column with taxon identifier lineages is added."""
    command = AddTaxInfoCommand(add_id_lineage=True, taxonomy_service=tax_service)
    result = command.execute(profile)
    assert "id_lineage" in result.columns
    assert result["id_lineage"].tolist() == [None, "476817098", "609216830"]


def test_add_rank_lineage(tax_service: TaxopyTaxonomyService, profile: pd.DataFrame):
    """Test that a column with taxon rank lineages is added."""
    command = AddTaxInfoCommand(add_rank_lineage=True, taxonomy_service=tax_service)
    result = command.execute(profile)
    assert "rank_lineage" in result.columns
    assert result["rank_lineage"].tolist() == [
        None,
        "superkingdom",
        "superkingdom",
    ]
