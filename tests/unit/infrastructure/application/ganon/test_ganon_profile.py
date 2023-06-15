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
                    ("target", [1]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("nr_unique", [1]),
                    ("nr_shared", [1]),
                    ("nr_children", [1]),
                    ("nr_cumulative", [1]),
                    ("pc_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["root"]),
                        ("target", [1]),
                        ("lineage", ["1"]),
                        ("name", ["root"]),
                        ("nr_unique", [1]),
                        ("nr_shared", [1]),
                        ("nr_children", [1]),
                        ("nr_cumulative", [1]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'pc_cumulative' not in dataframe"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("target", [1]),
                        ("lineage", ["1"]),
                        ("name", ["root"]),
                        ("nr_unique", [1]),
                        ("nr_shared", [1]),
                        ("nr_children", [1]),
                        ("nr_cumulative", [1]),
                        ("pc_cumulative", [100.0]),
                        ("rank", ["root"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'rank' out-of-order"
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
                    ("target", [1]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("nr_unique", [1]),
                    ("nr_shared", [1]),
                    ("nr_children", [1]),
                    ("nr_cumulative", [1]),
                    ("pc_cumulative", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", 1]),
                        ("lineage", ["-", 1]),
                        ("name", ["unclassified", "root"]),
                        ("nr_unique", [0, 0]),
                        ("nr_shared", [0, 0]),
                        ("nr_children", [0, 457530]),
                        ("nr_cumulative", [0, 4575301]),
                        ("pc_cumulative", [72.38712, 39.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="compositionality - percent exceeds 100"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", 1]),
                        ("lineage", ["-", 1]),
                        ("name", ["unclassified", "root"]),
                        ("nr_unique", [0, 0]),
                        ("nr_shared", [0, 0]),
                        ("nr_children", [0, 457530]),
                        ("nr_cumulative", [0, 4575301]),
                        ("pc_cumulative", [72.38712, 9.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="compositionality - percent below 100"
            ),
        ),
    ],
)
def test_percent(profile: pd.DataFrame):
    """Test that the percent column (pc_cumulative) is checked."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", [1]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("nr_unique", [1]),
                    ("nr_shared", [1]),
                    ("nr_children", [1]),
                    ("nr_cumulative", [1]),
                    ("pc_cumulative", [100.0]),
                ]
            )
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["unclassified", "root"]),
                    ("target", ["-", 1]),
                    ("lineage", ["-", 1]),
                    ("name", ["unclassified", "root"]),
                    ("nr_unique", [0, 10_000]),
                    ("nr_shared", [0, 0]),
                    ("nr_children", [0, 457530]),
                    ("nr_cumulative", [0, 4575301]),
                    ("pc_cumulative", [72.38712, 29.61288]),
                ]
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="broken integer format"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", 1]),
                        ("lineage", ["-", 1]),
                        ("name", ["unclassified", "root"]),
                        ("nr_unique", [0, -1]),
                        ("nr_shared", [0, 0]),
                        ("nr_children", [0, 457530]),
                        ("nr_cumulative", [0, 4575301]),
                        ("pc_cumulative", [72.38712, 29.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="count less than 0"
            ),
        ),
    ],
)
def test_nr_unique_reads(profile: pd.DataFrame):
    """Test that the nr_unique column is checked."""
    GanonProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["root"]),
                    ("target", [1]),
                    ("lineage", ["1"]),
                    ("name", ["root"]),
                    ("nr_unique", [1]),
                    ("nr_shared", [1]),
                    ("nr_children", [1]),
                    ("nr_cumulative", [1]),
                    ("pc_cumulative", [100.0]),
                ]
            )
        ),
        pd.DataFrame(
            OrderedDict(
                [
                    ("rank", ["unclassified", "root"]),
                    ("target", ["-", 1]),
                    ("lineage", ["-", 1]),
                    ("name", ["unclassified", "root"]),
                    ("nr_unique", [0, 0]),
                    ("nr_shared", [0, 0]),
                    ("nr_children", [0, 457530]),
                    ("nr_cumulative", [0, 4_575_301]),
                    ("pc_cumulative", [72.38712, 29.61288]),
                ]
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="broken integer format"
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("rank", ["unclassified", "root"]),
                        ("target", ["-", 1]),
                        ("lineage", ["-", 1]),
                        ("name", ["unclassified", "root"]),
                        ("nr_unique", [0, 0]),
                        ("nr_shared", [0, 0]),
                        ("nr_children", [0, 457530]),
                        ("nr_cumulative", [0, -1]),
                        ("pc_cumulative", [72.38712, 29.61288]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="count less than 0"
            ),
        ),
    ],
)
def test_nr_cumulative_reads(profile: pd.DataFrame):
    """Test that the nr_cumulative column is checked."""
    GanonProfile.validate(profile)
