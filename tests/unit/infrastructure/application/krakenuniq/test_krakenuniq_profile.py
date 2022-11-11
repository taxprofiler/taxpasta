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


"""Test that the schema model validates KrakenUniq profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import KrakenUniqProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "percent",
            "reads",
            "taxReads",
            "kmers",
            "dup",
            "cov",
            "taxID",
            "rank",
            "taxName",
        ),
        pytest.param(
            (
                "percent",
                "reads",
                "taxReads",
                "kmers",
                "dup",
                "cov",
                "taxID",
                "taxName",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'rank' not in dataframe"
            ),
        ),
        pytest.param(
            (
                "percent",
                "taxID",
                "reads",
                "taxReads",
                "kmers",
                "dup",
                "cov",
                "rank" "taxName",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxID' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    KrakenUniqProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "percent": [100, 100],
                "reads": [100, 100],
                "taxReads": [0, 100],
                "kmers": [7556, 7556],
                "dup": [1.3, 1.3],
                "cov": [0.1268, 0.1268],
                "taxID": [100, 2697049],
                "rank": ["no rank", "species"],
                "taxName": [
                    "Severe acute respiratory syndrome-related coronavirus",
                    "Severe acute respiratory syndrome coronavirus 2",
                ],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [100, 100],
                    "reads": [100, 100],
                    "taxReads": [
                        "Severe acute respiratory syndrome coronavirus 2",
                        100,
                    ],
                    "kmers": [7556, 7556],
                    "dup": [1.3, 1.3],
                    "cov": [0.1268, 0.1268],
                    "taxID": [2697049, 100],
                    "taxName": [
                        "Severe acute respiratory syndrome-related coronavirus",
                        "Severe acute respiratory syndrome coronavirus 2",
                    ],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_taxonomy_id(table: pd.DataFrame):
    """Test that the taxonomy_id column is checked."""
    KrakenUniqProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "percent": [100, 100],
                "reads": [100, 100],
                "taxReads": [0, 694009],
                "kmers": [7556, 7556],
                "dup": [1.3, 1.3],
                "cov": [0.1268, 0.1268],
                "taxID": [100, 2697049],
                "rank": ["no rank", "species"],
                "taxName": [
                    "Severe acute respiratory syndrome-related coronavirus",
                    "Severe acute respiratory syndrome coronavirus 2",
                ],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "percent": [100, 100],
                    "reads": [100, 100],
                    "taxReads": ["one hundred", 694009],
                    "kmers": [7556, 7556],
                    "dup": [1.3, 1.3],
                    "cov": [0.1268, 0.1268],
                    "taxID": [100, 2697049],
                    "rank": ["no rank", "species"],
                    "taxName": [
                        "Severe acute respiratory syndrome-related coronavirus",
                        "Severe acute respiratory syndrome coronavirus 2",
                    ],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_count(table: pd.DataFrame):
    """Test that the count column is checked."""
    KrakenUniqProfile.validate(table)
