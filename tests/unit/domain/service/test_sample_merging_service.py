# Copyright (c) 2022 Moritz E. Beber
# Copyright (c) 2022 Maxime Borry
# Copyright (c) 2022 James Fellows Yates
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


"""Test that the multiple samples are merged as expected."""


from typing import Iterable

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from taxpasta.domain.model import Sample, StandardProfile
from taxpasta.domain.service import SampleMergingService


@pytest.mark.parametrize(
    ("samples", "expected"),
    [
        (
            [
                Sample(
                    name="s1",
                    profile=pd.DataFrame(
                        {
                            StandardProfile.taxonomy_id: pd.Series(
                                ["1", "2"], dtype="category"
                            ),
                            StandardProfile.count: [23, 42],
                        }
                    ),
                ),
                Sample(
                    name="s2",
                    profile=pd.DataFrame(
                        {
                            StandardProfile.taxonomy_id: pd.Series(
                                ["2", "3"], dtype="category"
                            ),
                            StandardProfile.count: [33, 55],
                        }
                    ),
                ),
            ],
            pd.DataFrame(
                {
                    "taxonomy_id": pd.Series(["1", "2", "3"], dtype="category"),
                    "s1": [23, 42, 0],
                    "s2": [0, 33, 55],
                }
            ),
        )
    ],
)
def test_merge_wide(samples: Iterable[Sample], expected: pd.DataFrame):
    """Expect that samples are merged in wide format."""
    # On Windows the `astype` conversion may change the dtype from int64 to int32.
    # For compatibility, we disable the exact dtype match here.
    assert_frame_equal(
        SampleMergingService.merge_wide(samples), expected, check_dtype=False
    )


@pytest.mark.parametrize(
    ("samples", "expected"),
    [
        (
            [
                Sample(
                    name="s1",
                    profile=pd.DataFrame(
                        {
                            StandardProfile.taxonomy_id: pd.Series(
                                ["1", "2"], dtype="category"
                            ),
                            StandardProfile.count: [23, 42],
                        }
                    ),
                ),
                Sample(
                    name="s2",
                    profile=pd.DataFrame(
                        {
                            StandardProfile.taxonomy_id: pd.Series(
                                ["2", "3"], dtype="category"
                            ),
                            StandardProfile.count: [33, 55],
                        }
                    ),
                ),
            ],
            pd.DataFrame(
                {
                    "taxonomy_id": pd.Series(["1", "2", "2", "3"], dtype="category"),
                    "count": [23, 42, 33, 55],
                    "sample": pd.Series(["s1", "s1", "s2", "s2"], dtype="category"),
                }
            ),
        )
    ],
)
def test_merge_long(samples: Iterable[Sample], expected: pd.DataFrame):
    """Expect that samples are merged in long format."""
    assert_frame_equal(SampleMergingService.merge_long(samples), expected)
