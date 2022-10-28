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


"""Test that the reader can parse valid MALT-rma2info profiles."""


from pathlib import Path
from typing import List, Tuple, Union

import pytest

from taxpasta.infrastructure.application import MaltProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "malt_rma2info_valid.txt.gz",
            [
                (1, 1, 3.0),
                (2, 0, 10),
                (5, 1, 9.0),
            ],
        ),
    ],
)
def test_read_correctness(
    malt_data_dir: Path,
    filename: str,
    checks: List[Tuple[int, int, Union[int, float, str]]],
):
    """Test that the reader can parse valid malt profiles."""
    profile = MaltProfileReader.read(malt_data_dir / filename)
    for (row, col, value) in checks:
        assert profile.iat[row, col] == value