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


"""Test that the schema model validates bracken profiles correctly."""


from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import BrackenProfile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("name", ["root"]),
                    ("taxonomy_id", [1]),
                    ("taxonomy_lvl", ["root"]),
                    ("kraken_assigned_reads", [100]),
                    ("added_reads", [0]),
                    ("new_est_reads", [100]),
                    ("fraction_total_reads", [1.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["root"]),
                        ("taxonomy_id", [1]),
                        ("kraken_assigned_reads", [100]),
                        ("added_reads", [0]),
                        ("new_est_reads", [100]),
                        ("fraction_total_reads", [1.0]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' not in dataframe"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["root"]),
                        ("taxonomy_id", [1]),
                        ("taxonomy_lvl", ["root"]),
                        ("kraken_assigned_reads", [100]),
                        ("added_reads", [0]),
                        ("new_est_reads", [100]),
                        ("fraction_total_reads", [1.0]),
                        ("foo", [1.0]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'foo' not in DataFrameSchema"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["root"]),
                        ("taxonomy_lvl", ["root"]),
                        ("added_reads", [0]),
                        ("kraken_assigned_reads", [100]),
                        ("taxonomy_id", [1]),
                        ("new_est_reads", [100]),
                        ("fraction_total_reads", [1.0]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'taxonomy_lvl' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    BrackenProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("name", ["Faecalibacterium prausnitzii", "Escherichia coli"]),
                    ("taxonomy_id", [1964, 1104]),
                    ("taxonomy_lvl", ["R7", "R7"]),
                    ("kraken_assigned_reads", [100, 0]),
                    ("added_reads", [0, 0]),
                    ("new_est_reads", [100, 0]),
                    ("fraction_total_reads", [1.0, 0.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["Faecalibacterium prausnitzii", "Escherichia coli"]),
                        ("taxonomy_id", [1964, 1104]),
                        ("taxonomy_lvl", ["R7", "R7"]),
                        ("kraken_assigned_reads", [100, 0]),
                        ("added_reads", [0, 0]),
                        ("new_est_reads", [100, 0]),
                        ("fraction_total_reads", [0.991, 0.119]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="<Check compositionality>"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["Faecalibacterium prausnitzii", "Escherichia coli"]),
                        ("taxonomy_id", [1964, 1104]),
                        ("taxonomy_lvl", ["R7", "R7"]),
                        ("kraken_assigned_reads", [100, 0]),
                        ("added_reads", [0, 0]),
                        ("new_est_reads", [100, 0]),
                        ("fraction_total_reads", [0.791, 0.009]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="<Check compositionality>"
            ),
        ),
    ],
)
@pytest.mark.filterwarnings("error::UserWarning")
def test_fraction_total_reads(profile: pd.DataFrame):
    """Test that the fraction column is checked."""
    BrackenProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("name", ["Faecalibacterium prausnitzii", "Escherichia coli"]),
                    ("taxonomy_id", [1964, 1104]),
                    ("taxonomy_lvl", ["R7", "R7"]),
                    ("kraken_assigned_reads", [42, 10_000_000]),
                    ("added_reads", [42, 10_000_000]),
                    ("new_est_reads", [84, 20_000_000]),
                    ("fraction_total_reads", [1.0, 0.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("name", ["Faecalibacterium prausnitzii", "Escherichia coli"]),
                        ("taxonomy_id", [1964, 1104]),
                        ("taxonomy_lvl", ["R7", "R7"]),
                        ("kraken_assigned_reads", [42, 10_000_000]),
                        ("added_reads", [42, 10_000_000]),
                        ("new_est_reads", [84, 10_000_000]),
                        ("fraction_total_reads", [1.0, 0.0]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="<Check check_added_reads_consistency>"
            ),
        ),
    ],
)
def test_added_reads_consistency(profile: pd.DataFrame):
    """Test that the reads added by Bracken are consistent."""
    BrackenProfile.validate(profile)
