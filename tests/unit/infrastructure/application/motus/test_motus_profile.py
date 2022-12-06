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


"""Test that the schema model validates mOTUs profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import MotusProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "consensus_taxonomy"
            "NCBI_tax_id",
            "read_count",
        ),
        pytest.param(
            (
                "consensus_taxonomy"
                "NCBI_tax_id",
                "query_id",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'query_id' not in dataframe"
            ),
        ),
        pytest.param(
            (
                "consensus_taxonomy"
                "read_count",
                "NCBI_tax_id",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'NCBI_tax_id' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    MotusProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "consensus_taxonomy": ["Leptospira alexanderi [ref_mOTU_v3_00001]","Leptospira weilii [ref_mOTU_v3_00002]" ],
                "NCBI_tax_id": [100053, 28184],
                "read_count": [0, 0],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "consensus_taxonomy": ["Leptospira alexanderi [ref_mOTU_v3_00001]","Leptospira weilii [ref_mOTU_v3_00002]" ],
                    "NCBI_tax_id": [ "Leptospira alexanderi [ref_mOTU_v3_00001]", 28184 ],
                    "read_count": [0, 0],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_taxonomy_id(table: pd.DataFrame):
    """Test that the taxID column is checked."""
    MotusProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "consensus_taxonomy": ["Leptospira alexanderi [ref_mOTU_v3_00001]","Leptospira weilii [ref_mOTU_v3_00002]" ],
                "NCBI_tax_id": [100053, 28184],
                "read_count": [0, 0],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "consensus_taxonomy": ["Leptospira alexanderi [ref_mOTU_v3_00001]","Leptospira weilii [ref_mOTU_v3_00002]" ],
                    "NCBI_tax_id": [100053, 28184],
                    "read_count": ["zero", 0],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_count(table: pd.DataFrame):
    """Test that the count column is checked."""
    MotusProfile.validate(table)
