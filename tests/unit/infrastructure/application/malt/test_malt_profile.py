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


"""Test that the schema model validates MALT-rma2info profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import MaltProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "taxonomy_id",
            "count",
        ),
        pytest.param(
            (
                "taxonomy_id",
                "query_id",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'query_id' not in DataFrameSchema",
            ),
        ),
        pytest.param(
            (
                "count",
                "taxonomy_id",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'count' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    MaltProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "taxonomy_id": [20, 21.0],
                "count": [21.0, 9.0],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "taxonomy_id": [20, 21.0],
                    "count": ["shigella_dysenteriae", 9.0],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_taxonomy_id(table: pd.DataFrame):
    """Test that the taxonomy_id column is checked."""
    MaltProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "taxonomy_id": [20, 21.0],
                "count": [21.0, 9.0],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "taxonomy_id": [20, 21.0],
                    "count": [29, "fourty one"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_count(table: pd.DataFrame):
    """Test that the count column is checked."""
    MaltProfile.validate(table)
