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


"""Test that the schema model validates diamond profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import DiamondProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "query_id",
            "taxonomy_id",
            "e_value",
        ),
        pytest.param(
            (
                "query_id",
                "taxonomy_id",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'e_value' not in dataframe",
            ),
        ),
        pytest.param(
            (
                "taxonomy_id",
                "query_id",
                "e_value",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_id' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    DiamondProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "query_id": [
                    "shigella_dysenteriae_958/1",
                    "shigella_dysenteriae_1069/1",
                ],
                "taxonomy_id": [511145, 511145],
                "e_value": [2.46e-08, 2.37e-07],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "query_id": [
                        "shigella_dysenteriae_958/1",
                        "shigella_dysenteriae_1069/1",
                    ],
                    "taxonomy_id": ["abcd", 511145],
                    "e_value": [2.46e-08, 2.37e-07],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_taxonomy_id(table: pd.DataFrame):
    """Test that the taxonomy_id column is checked."""
    DiamondProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "query_id": [
                    "shigella_dysenteriae_958/1",
                    "shigella_dysenteriae_1069/1",
                ],
                "taxonomy_id": [511145, 511145],
                "e_value": [2.46e-08, 2.37e-07],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "query_id": [
                        "shigella_dysenteriae_958/1",
                        "shigella_dysenteriae_1069/1",
                    ],
                    "taxonomy_id": [511145, 511145],
                    "e_value": [2.46e-08, 2.37e07],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_e_value(table: pd.DataFrame):
    """Test that the reads column is checked."""
    DiamondProfile.validate(table)
