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


"""Test that the schema model validates mOTUs profiles correctly."""

from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import MotusProfile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("consensus_taxonomy", ["bac"]),
                    ("ncbi_tax_id", [2]),
                    ("read_count", [1]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("consensus_taxonomy", ["bac"]),
                        ("ncbi_tax_id", [2]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'read_count' not in dataframe",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("consensus_taxonomy", ["bac"]),
                        ("read_count", [1]),
                        ("ncbi_tax_id", [2]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'read_count' out-of-order",
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    MotusProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    (
                        "consensus_taxonomy",
                        [
                            "Leptospira alexanderi [ref_mOTU_v3_00001]",
                            "Leptospira weilii [ref_mOTU_v3_00002]",
                        ],
                    ),
                    ("ncbi_tax_id", [100053, 28184]),
                    ("read_count", [0, 0]),
                ],
            ),
        ),
    ],
)
def test_taxonomy_id(profile: pd.DataFrame):
    """Test that the taxID column is checked."""
    MotusProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    (
                        "consensus_taxonomy",
                        [
                            "Leptospira alexanderi [ref_mOTU_v3_00001]",
                            "Leptospira weilii [ref_mOTU_v3_00002]",
                        ],
                    ),
                    ("ncbi_tax_id", [100053, 28184]),
                    ("read_count", [0, 0]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        (
                            "consensus_taxonomy",
                            [
                                "Leptospira alexanderi [ref_mOTU_v3_00001]",
                                "Leptospira weilii [ref_mOTU_v3_00002]",
                            ],
                        ),
                        ("ncbi_tax_id", [100053, 28184]),
                        ("read_count", ["0", 0]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'read_count' to have type",
            ),
        ),
    ],
)
def test_count(profile: pd.DataFrame):
    """Test that the count column is checked."""
    MotusProfile.validate(profile)
