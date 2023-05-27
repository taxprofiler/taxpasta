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


"""Test that the schema model validates MEGAN6 rma2info profiles correctly."""


from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import Megan6Profile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("taxonomy_id", [1]),
                    ("count", [100.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", [1]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'count' not in",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("count", [100.0]),
                        ("taxonomy_id", [1]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'count' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    Megan6Profile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("taxonomy_id", [20, 21]),
                    ("count", [21.0, 9.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", ["20", 21]),
                        ("count", [21.0, 9.0]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'taxonomy_id' to have type",
            ),
        ),
    ],
)
def test_taxonomy_id(profile: pd.DataFrame):
    """Test that the taxonomy_id column is checked."""
    Megan6Profile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("taxonomy_id", [20, 21]),
                    ("count", [21.0, 9.0]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("taxonomy_id", [20, 21]),
                        ("count", [21.0, "9.0"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'count' to have type",
            ),
        ),
    ],
)
def test_count(profile: pd.DataFrame):
    """Test that the count column is checked."""
    Megan6Profile.validate(profile)
