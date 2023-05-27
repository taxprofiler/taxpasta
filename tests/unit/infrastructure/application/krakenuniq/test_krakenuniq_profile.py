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


"""Test that the schema model validates KrakenUniq profiles correctly."""


from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import KrakenUniqProfile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("%", [0.0]),
                    ("reads", [0]),
                    ("taxReads", [0]),
                    ("kmers", [0]),
                    ("dup", [0.0]),
                    ("cov", [0.0]),
                    ("taxID", [0]),
                    ("rank", ["no rank"]),
                    ("taxName", ["root"]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("%", [0.0]),
                        ("reads", [0]),
                        ("taxReads", [0]),
                        ("kmers", [0]),
                        ("dup", [0.0]),
                        ("cov", [0.0]),
                        ("taxID", [0]),
                        ("taxName", ["root"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'rank' not in dataframe"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("%", [0.0]),
                        ("taxID", [0]),
                        ("reads", [0]),
                        ("taxReads", [0]),
                        ("kmers", [0]),
                        ("dup", [0.0]),
                        ("cov", [0.0]),
                        ("rank", ["no rank"]),
                        ("taxName", ["root"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxID' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    KrakenUniqProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("%", [100.0, 100.0]),
                    ("reads", [100, 100]),
                    ("taxReads", [0, 100]),
                    ("kmers", [7556, 7556]),
                    ("dup", [1.3, 1.3]),
                    ("cov", [0.1268, 0.1268]),
                    ("taxID", [0, 2697049]),
                    ("rank", ["no rank", "species"]),
                    (
                        "taxName",
                        [
                            "Severe acute respiratory syndrome-related coronavirus",
                            "Severe acute respiratory syndrome coronavirus 2",
                        ],
                    ),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("%", [100.0, 100.0]),
                        ("reads", [100, 100]),
                        ("taxReads", [0, 100]),
                        ("kmers", [7556, 7556]),
                        ("dup", [1.3, 1.3]),
                        ("cov", [0.1268, 0.1268]),
                        ("taxID", [2697049, "100"]),
                        ("rank", ["no rank", "species"]),
                        (
                            "taxName",
                            [
                                "Severe acute respiratory syndrome-related coronavirus",
                                "Severe acute respiratory syndrome coronavirus 2",
                            ],
                        ),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'taxID' to have type",
            ),
        ),
    ],
)
def test_taxonomy_id(profile: pd.DataFrame):
    """Test that the taxonomy_id column is checked."""
    KrakenUniqProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("%", [100.0, 100.0]),
                    ("reads", [100, 100]),
                    ("taxReads", [0, 100]),
                    ("kmers", [7556, 7556]),
                    ("dup", [1.3, 1.3]),
                    ("cov", [0.1268, 0.1268]),
                    ("taxID", [0, 2697049]),
                    ("rank", ["no rank", "species"]),
                    (
                        "taxName",
                        [
                            "Severe acute respiratory syndrome-related coronavirus",
                            "Severe acute respiratory syndrome coronavirus 2",
                        ],
                    ),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("%", [100.0, 100.0]),
                        ("reads", [100, 100]),
                        ("taxReads", ["0", 100]),
                        ("kmers", [7556, 7556]),
                        ("dup", [1.3, 1.3]),
                        ("cov", [0.1268, 0.1268]),
                        ("taxID", [0, 2697049]),
                        ("rank", ["no rank", "species"]),
                        (
                            "taxName",
                            [
                                "Severe acute respiratory syndrome-related coronavirus",
                                "Severe acute respiratory syndrome coronavirus 2",
                            ],
                        ),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="expected series 'taxReads' to have type"
            ),
        ),
    ],
)
def test_count(profile: pd.DataFrame):
    """Test that the count column is checked."""
    KrakenUniqProfile.validate(profile)
