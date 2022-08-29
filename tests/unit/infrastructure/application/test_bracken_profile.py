# Copyright (c) 2022, Moritz E. Beber, Maxime Borry, Jianhong Ou, Sofia Stamouli.
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

from taxpasta.infrastructure.application import BrackenProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "name",
            "taxonomy_id",
            "taxonomy_lvl",
            "kraken_assigned_reads",
            "added_reads",
            "new_est_reads",
            "fraction_total_reads",
        ),
        pytest.param(
            (
                "name",
                "taxonomy_id",
                "kraken_assigned_reads",
                "added_reads",
                "new_est_reads",
                "fraction_total_reads",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' not in dataframe"
            ),
        ),
        pytest.param(
            (
                "name",
                "taxonomy_id",
                "taxonomy_lvl",
                "kraken_assigned_reads",
                "added_reads",
                "new_est_reads",
                "fraction_total_reads",
                "foo",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'foo' not in DataFrameSchema"
            ),
        ),
        pytest.param(
            (
                "name",
                "taxonomy_lvl",
                "added_reads",
                "fraction_total_reads",
                "taxonomy_id",
                "new_est_reads",
                "kraken_assigned_reads",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    BrackenProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                "taxonomy_id": ["1964", "1104"],
                "taxonomy_lvl": ["R7", "R7"],
                "kraken_assigned_reads": [0, 0],
                "added_reads": [0, 0],
                "new_est_reads": [0, 0],
                "fraction_total_reads": [0.991, 0.009],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                    "taxonomy_id": ["1964", "1104"],
                    "taxonomy_lvl": ["R7", "R7"],
                    "kraken_assigned_reads": [0, 0],
                    "added_reads": [0, 0],
                    "new_est_reads": [0, 0],
                    "fraction_total_reads": [0.991, 0.019],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                    "taxonomy_id": ["1964", "1104"],
                    "taxonomy_lvl": ["R7", "R7"],
                    "kraken_assigned_reads": [0, 0],
                    "added_reads": [0, 0],
                    "new_est_reads": [0, 0],
                    "fraction_total_reads": [0.791, 0.009],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_fraction_total_reads(table: pd.DataFrame):
    """Test that the fraction column is checked."""
    BrackenProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                "taxonomy_id": ["1964", "1104"],
                "taxonomy_lvl": ["R7", "R7"],
                "kraken_assigned_reads": [0, 0],
                "added_reads": [0, 0],
                "new_est_reads": [0, 0],
                "fraction_total_reads": [1.0, 0.0],
            }
        ),
        pd.DataFrame(
            {
                "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                "taxonomy_id": ["1964", "1104"],
                "taxonomy_lvl": ["R7", "R7"],
                "kraken_assigned_reads": [42, 10_000_000],
                "added_reads": [42, 10_000_000],
                "new_est_reads": [84, 20_000_000],
                "fraction_total_reads": [1.0, 0.0],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "name": ["Faecalibacterium prausnitzii", "Escherichia coli"],
                    "taxonomy_id": ["1964", "1104"],
                    "taxonomy_lvl": ["R7", "R7"],
                    "kraken_assigned_reads": [42, 10_000_000],
                    "added_reads": [42, 10_000_000],
                    "new_est_reads": [84, 10_000_000],
                    "fraction_total_reads": [1.0, 0.0],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_added_reads_consistency(table: pd.DataFrame):
    """Test that the reads added by Bracken are consistent."""
    BrackenProfile.validate(table)
