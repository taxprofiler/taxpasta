# Copyright (c) 2023 Moritz E. Beber
# Copyright (c) 2023 Maxime Borry
# Copyright (c) 2023 James A. Fellows Yates
# Copyright (c) 2023 Sofia Stamouli.
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


"""Test that the schema model validates ganon profiles correctly."""


from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import GanonProfile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", ["1"]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("number_unique", [1]),
                    ("number_shared", [1]),
                    ("number_children", [1]),
                    ("number_cumulative", [1]),
                    ("percent_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["root"]),
                        ("target", ["1"]),
                        ("lineage", ["1"]),
                        ("name", ["root"]),
                        ("number_unique", [1]),
                        ("number_shared", [1]),
                        ("number_children", [1]),
                        ("number_cumulative", [1]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'percent_cumulative' not in dataframe",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("target", ["1"]),
                        ("lineage", ["1"]),
                        ("name", ["root"]),
                        ("number_unique", [1]),
                        ("number_shared", [1]),
                        ("number_children", [1]),
                        ("number_cumulative", [1]),
                        ("percent_cumulative", [100.0]),
                        ("rank", ["root"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'target' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", ["1"]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("number_unique", [1]),
                    ("number_shared", [1]),
                    ("number_children", [1]),
                    ("number_cumulative", [1]),
                    ("percent_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", "1"]),
                        ("lineage", ["-", "1"]),
                        ("name", ["unclassified", "root"]),
                        ("number_unique", [0, 0]),
                        ("number_shared", [0, 0]),
                        ("number_children", [0, 457530]),
                        ("number_cumulative", [0, 4575301]),
                        ("percent_cumulative", [72.38712, 39.61288]),
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
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", "1"]),
                        ("lineage", ["-", "1"]),
                        ("name", ["unclassified", "root"]),
                        ("number_unique", [0, 0]),
                        ("number_shared", [0, 0]),
                        ("number_children", [0, 457530]),
                        ("number_cumulative", [0, 4575301]),
                        ("percent_cumulative", [72.38712, 9.61288]),
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
def test_percent(profile: pd.DataFrame):
    """Test that the percent column (percent_cumulative) is checked."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", ["1"]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("number_unique", [1]),
                    ("number_shared", [1]),
                    ("number_children", [1]),
                    ("number_cumulative", [1]),
                    ("percent_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", 1]),
                        ("lineage", ["-", "1"]),
                        ("name", ["unclassified", "root"]),
                        ("number_unique", [0, -1]),
                        ("number_shared", [0, 0]),
                        ("number_children", [0, 457530]),
                        ("number_cumulative", [0, 4575301]),
                        ("percent_cumulative", [72.38712, 27.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'target' to have type str",
            ),
        ),
    ],
)
def test_target(profile: pd.DataFrame):
    """Test that the target column is checked."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", ["1"]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("number_unique", [1]),
                    ("number_shared", [1]),
                    ("number_children", [1]),
                    ("number_cumulative", [1]),
                    ("percent_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", "1"]),
                        ("lineage", ["-", "1"]),
                        ("name", ["unclassified", "root"]),
                        ("number_unique", [0, -1]),
                        ("number_shared", [0, 0]),
                        ("number_children", [0, 457530]),
                        ("number_cumulative", [0, 4575301]),
                        ("percent_cumulative", [72.38712, 27.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="greater_than_or_equal_to"
            ),
        ),
    ],
)
def test_nr_unique_reads(profile: pd.DataFrame):
    """Test that the number_unique column is checked."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", ["1"]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("number_unique", [1]),
                    ("number_shared", [1]),
                    ("number_children", [1]),
                    ("number_cumulative", [1]),
                    ("percent_cumulative", [100.0]),
                ]
            )
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["unclassified", "root"]),
                    ("target", ["-", "1"]),
                    ("lineage", ["-", "1"]),
                    ("name", ["unclassified", "root"]),
                    ("number_unique", [0, 0]),
                    ("number_shared", [0, 0]),
                    ("number_children", [0, 457530]),
                    ("number_cumulative", [0, 4_575_301]),
                    ("percent_cumulative", [72.38712, 27.61288]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", "1"]),
                        ("lineage", ["-", "1"]),
                        ("name", ["unclassified", "root"]),
                        ("number_unique", [0, 0]),
                        ("number_shared", [0, 0]),
                        ("number_children", [0, 457530]),
                        ("number_cumulative", [0, -1]),
                        ("percent_cumulative", [72.38712, 29.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="greater_than_or_equal_to"
            ),
        ),
    ],
)
def test_nr_cumulative_reads(profile: pd.DataFrame):
    """Test that the number_cumulative column is checked."""
    GanonProfile.validate(profile)
