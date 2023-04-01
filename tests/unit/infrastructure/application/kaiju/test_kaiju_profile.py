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


"""Test that the schema model validates kaiju profiles correctly."""


from typing import Collection

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import KaijuProfile


@pytest.mark.parametrize(
    "columns",
    [
        (
            "file",
            "percent",
            "reads",
            "taxon_id",
            "taxon_name",
        ),
        pytest.param(
            (
                "file",
                "percent",
                "reads",
                "taxon_name",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'taxon_id' not in dataframe",
            ),
        ),
        pytest.param(
            (
                "file",
                "taxon_id",
                "reads",
                "percent",
                "taxon_name",
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxon_id' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(columns: Collection[str]):
    """Test that column names and order are validated."""
    KaijuProfile.validate(pd.DataFrame(columns=columns, data=[]))


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "file": [
                    "barcode41_se-barcode41-kaiju.tsv",
                    "barcode41_se-barcode41-kaiju.tsv",
                ],
                "percent": [99.1, 0.9],
                "reads": [0, 0],
                "taxon_id": [-1, 1],
                "taxon_name": ["unclassified", "Viruses"],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "file": [
                        "barcode41_se-barcode41-kaiju.tsv",
                        "barcode41_se-barcode41-kaiju.tsv",
                    ],
                    "percent": [99.1, 2.9],
                    "reads": [0, 0],
                    "taxon_id": [-1, 1],
                    "taxon_name": ["unclassified", "Viruses"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "file": [
                        "barcode41_se-barcode41-kaiju.tsv",
                        "barcode41_se-barcode41-kaiju.tsv",
                    ],
                    "percent": [79.1, 1.9],
                    "reads": [0, 0],
                    "taxon_id": [-1, 1],
                    "taxon_name": ["unclassified", "Viruses"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_percent(table: pd.DataFrame):
    """Test that the percent column is checked."""
    KaijuProfile.validate(table)


@pytest.mark.parametrize(
    "table",
    [
        pd.DataFrame(
            {
                "file": [
                    "barcode41_se-barcode41-kaiju.tsv",
                    "barcode41_se-barcode41-kaiju.tsv",
                ],
                "percent": [99.1, 0.9],
                "reads": [0, 0],
                "taxon_id": [-1, 1],
                "taxon_name": ["unclassified", "Viruses"],
            }
        ),
        pd.DataFrame(
            {
                "file": [
                    "barcode41_se-barcode41-kaiju.tsv",
                    "barcode41_se-barcode41-kaiju.tsv",
                ],
                "percent": [99.1, 0.9],
                "reads": [42, 10_000_000],
                "taxon_id": [-1, 1],
                "taxon_name": ["unclassified", "Viruses"],
            }
        ),
        pytest.param(
            pd.DataFrame(
                {
                    "file": [
                        "barcode41_se-barcode41-kaiju.tsv",
                        "barcode41_se-barcode41-kaiju.tsv",
                    ],
                    "percent": [99.1, 0.9],
                    "reads": [-1, 0],
                    "taxon_id": [-1, 1],
                    "taxon_name": ["unclassified", "Viruses"],
                }
            ),
            marks=pytest.mark.raises(exception=SchemaError),
        ),
    ],
)
def test_reads(table: pd.DataFrame):
    """Test that the reads column is checked."""
    KaijuProfile.validate(table)
