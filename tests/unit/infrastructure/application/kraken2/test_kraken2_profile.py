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

from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import Kraken2Profile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [100.0]),
                    ("clade_assigned_reads", [100]),
                    ("direct_assigned_reads", [100]),
                    ("taxonomy_lvl", ["R"]),
                    ("taxonomy_id", [1]),
                    ("name", ["root"]),
                ],
            ),
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [100.0]),
                    ("clade_assigned_reads", [100]),
                    ("direct_assigned_reads", [100]),
                    ("num_minimizers", [1]),
                    ("distinct_minimizers", [1]),
                    ("taxonomy_lvl", ["R"]),
                    ("taxonomy_id", [1]),
                    ("name", ["root"]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [100.0]),
                        ("clade_assigned_reads", [100]),
                        ("direct_assigned_reads", [100]),
                        ("taxonomy_id", [1]),
                        ("name", ["root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'taxonomy_lvl' not in dataframe",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [100.0]),
                        ("clade_assigned_reads", [100]),
                        ("direct_assigned_reads", [100]),
                        ("num_minimizers", [1]),
                        ("distinct_minimizers", [1]),
                        ("taxonomy_lvl", ["R"]),
                        ("taxonomy_id", [1]),
                        ("name", ["root"]),
                        ("rank", ["R"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'rank' not in DataFrameSchema",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [100.0]),
                        ("taxonomy_lvl", ["R"]),
                        ("clade_assigned_reads", [100]),
                        ("direct_assigned_reads", [100]),
                        ("taxonomy_id", [1]),
                        ("name", ["root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'taxonomy_lvl' out-of-order",
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    Kraken2Profile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [99.1, 0.9]),
                    ("clade_assigned_reads", [100, 1]),
                    ("direct_assigned_reads", [100, 1]),
                    ("taxonomy_lvl", ["U", "R"]),
                    ("taxonomy_id", [0, 1]),
                    ("name", ["unclassified", "root"]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [99.1, 2.9]),
                        ("clade_assigned_reads", [100, 1]),
                        ("direct_assigned_reads", [100, 1]),
                        ("taxonomy_lvl", ["U", "R"]),
                        ("taxonomy_id", [0, 1]),
                        ("name", ["unclassified", "root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(exception=SchemaError, message="compositionality"),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [79.1, 1.9]),
                        ("clade_assigned_reads", [100, 1]),
                        ("direct_assigned_reads", [100, 1]),
                        ("taxonomy_lvl", ["U", "R"]),
                        ("taxonomy_id", [0, 1]),
                        ("name", ["unclassified", "root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(exception=SchemaError, message="compositionality"),
        ),
    ],
)
@pytest.mark.filterwarnings("error::UserWarning")
def test_percent(profile: pd.DataFrame):
    """Test that the percent column is checked."""
    Kraken2Profile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [99.1, 0.9]),
                    ("clade_assigned_reads", [100, 1]),
                    ("direct_assigned_reads", [100, 1]),
                    ("taxonomy_lvl", ["U", "R"]),
                    ("taxonomy_id", [0, 1]),
                    ("name", ["unclassified", "root"]),
                ],
            ),
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [99.1, 0.9]),
                    ("clade_assigned_reads", [42, 10_000_000]),
                    ("direct_assigned_reads", [100, 1]),
                    ("taxonomy_lvl", ["U", "R"]),
                    ("taxonomy_id", [0, 1]),
                    ("name", ["unclassified", "root"]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [99.1, 0.9]),
                        ("clade_assigned_reads", [-1, 0]),
                        ("direct_assigned_reads", [100, 1]),
                        ("taxonomy_lvl", ["U", "R"]),
                        ("taxonomy_id", [0, 1]),
                        ("name", ["unclassified", "root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="greater_than_or_equal_to",
            ),
        ),
    ],
)
def test_clade_assigned_reads(profile: pd.DataFrame):
    """Test that the clade_assigned_reads column is checked."""
    Kraken2Profile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [99.1, 0.9]),
                    ("clade_assigned_reads", [100, 1]),
                    ("direct_assigned_reads", [100, 1]),
                    ("taxonomy_lvl", ["U", "R"]),
                    ("taxonomy_id", [0, 1]),
                    ("name", ["unclassified", "root"]),
                ],
            ),
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("percent", [99.1, 0.9]),
                    ("clade_assigned_reads", [100, 1]),
                    ("direct_assigned_reads", [42, 10_000_000]),
                    ("taxonomy_lvl", ["U", "R"]),
                    ("taxonomy_id", [0, 1]),
                    ("name", ["unclassified", "root"]),
                ],
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("percent", [99.1, 0.9]),
                        ("clade_assigned_reads", [100, 1]),
                        ("direct_assigned_reads", [-1, 0]),
                        ("taxonomy_lvl", ["U", "R"]),
                        ("taxonomy_id", [0, 1]),
                        ("name", ["unclassified", "root"]),
                    ],
                ),
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="greater_than_or_equal_to",
            ),
        ),
    ],
)
def test_direct_assigned_reads(profile: pd.DataFrame):
    """Test that the direct_assigned_reads column is checked."""
    Kraken2Profile.validate(profile)
