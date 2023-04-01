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


"""Test that the schema model validates kraken2 profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import Kraken2Profile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "percent",
            "clade_assigned_reads",
            "direct_assigned_reads",
            "taxonomy_lvl",
            "taxonomy_id",
            "name",
        ),
        (
            "percent",
            "clade_assigned_reads",
            "direct_assigned_reads",
            "num_minimizers",
            "distinct_minimizers",
            "taxonomy_lvl",
            "taxonomy_id",
            "name",
        ),
        pytest.param(
            (
                "percent",
                "clade_assigned_reads",
                "direct_assigned_reads",
                "name",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' not in dataframe"
            ),
        ),
        pytest.param(
            (
                "percent",
                "clade_assigned_reads",
                "direct_assigned_reads",
                "num_minimizers",
                "distinct_minimizers",
                "taxonomy_lvl",
                "taxonomy_id",
                "name",
                "rank",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'rank' not in DataFrameSchema"
            ),
        ),
        pytest.param(
            (
                "percent",
                "taxonomy_lvl",
                "clade_assigned_reads",
                "taxonomy_id",
                "direct_assigned_reads",
                "name",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    Kraken2Profile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "percent": [99.1, 0.9],
                "clade_assigned_reads": [0, 0],
                "direct_assigned_reads": [0, 0],
                "taxonomy_lvl": ["U", "R"],
                "taxonomy_id": ["0", "1"],
                "name": ["unclassified", "root"],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [99.1, 2.9],
                    "clade_assigned_reads": [0, 0],
                    "direct_assigned_reads": [0, 0],
                    "taxonomy_lvl": ["U", "R"],
                    "taxonomy_id": ["0", "1"],
                    "name": ["unclassified", "root"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [79.1, 1.9],
                    "clade_assigned_reads": [0, 0],
                    "direct_assigned_reads": [0, 0],
                    "taxonomy_lvl": ["U", "R"],
                    "taxonomy_id": ["0", "1"],
                    "name": ["unclassified", "root"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_percent(table: pd.DataFrame):
    """Test that the percent column is checked."""
    Kraken2Profile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "percent": [99.1, 0.9],
                "clade_assigned_reads": [0, 0],
                "direct_assigned_reads": [0, 0],
                "taxonomy_lvl": ["U", "R"],
                "taxonomy_id": ["0", "1"],
                "name": ["unclassified", "root"],
            }
        ),
        pd.DataFrame(
            {
                "percent": [99.1, 0.9],
                "clade_assigned_reads": [42, 10_000_000],
                "direct_assigned_reads": [0, 0],
                "taxonomy_lvl": ["U", "R"],
                "taxonomy_id": ["0", "1"],
                "name": ["unclassified", "root"],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [99.1, 0.9],
                    "clade_assigned_reads": [-1, 0],
                    "direct_assigned_reads": [0, 0],
                    "taxonomy_lvl": ["U", "R"],
                    "taxonomy_id": ["0", "1"],
                    "name": ["unclassified", "root"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_clade_assigned_reads(table: pd.DataFrame):
    """Test that the clade_assigned_reads column is checked."""
    Kraken2Profile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "percent": [99.1, 0.9],
                "clade_assigned_reads": [0, 0],
                "direct_assigned_reads": [0, 0],
                "taxonomy_lvl": ["U", "R"],
                "taxonomy_id": ["0", "1"],
                "name": ["unclassified", "root"],
            }
        ),
        pd.DataFrame(
            {
                "percent": [99.1, 0.9],
                "clade_assigned_reads": [0, 0],
                "direct_assigned_reads": [42, 10_000_000],
                "taxonomy_lvl": ["U", "R"],
                "taxonomy_id": ["0", "1"],
                "name": ["unclassified", "root"],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [99.1, 0.9],
                    "clade_assigned_reads": [0, 0],
                    "direct_assigned_reads": [-1, 0],
                    "taxonomy_lvl": ["U", "R"],
                    "taxonomy_id": ["0", "1"],
                    "name": ["unclassified", "root"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_direct_assigned_reads(table: pd.DataFrame):
    """Test that the direct_assigned_reads column is checked."""
    Kraken2Profile.validate(table)
