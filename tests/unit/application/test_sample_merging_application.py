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


"""Test that the multiple samples are merged as expected."""


from typing import Iterable, Tuple

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pandera.typing import DataFrame

from taxpasta.application.sample_merging_application import SampleMergingApplication
from taxpasta.domain import StandardProfile


@pytest.mark.parametrize(
    "samples, expected",
    [
        (
            [
                ("s1", pd.DataFrame({"taxonomy_id": ["1", "2"], "count": [23, 42]})),
                ("s2", pd.DataFrame({"taxonomy_id": ["2", "3"], "count": [33, 55]})),
            ],
            pd.DataFrame(
                {"taxonomy_id": ["1", "2", "3"], "s1": [23, 42, 0], "s2": [0, 33, 55]}
            ),
        )
    ],
)
def test_merge_wide(
    samples: Iterable[Tuple[str, DataFrame[StandardProfile]]], expected: pd.DataFrame
):
    assert_frame_equal(SampleMergingApplication.merge_wide(samples), expected)


@pytest.mark.parametrize(
    "samples, expected",
    [
        (
            [
                ("s1", pd.DataFrame({"taxonomy_id": ["1", "2"], "count": [23, 42]})),
                ("s2", pd.DataFrame({"taxonomy_id": ["2", "3"], "count": [33, 55]})),
            ],
            pd.DataFrame(
                {
                    "taxonomy_id": ["1", "2", "2", "3"],
                    "count": [23, 42, 33, 55],
                    "sample": ["s1", "s1", "s2", "s2"],
                }
            ),
        )
    ],
)
def test_merge_long(
    samples: Iterable[Tuple[str, DataFrame[StandardProfile]]], expected: pd.DataFrame
):
    assert_frame_equal(SampleMergingApplication.merge_long(samples), expected)
