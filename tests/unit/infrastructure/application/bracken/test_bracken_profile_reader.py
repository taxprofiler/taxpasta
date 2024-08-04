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


"""Test that the reader can parse valid Bracken profiles."""


from pathlib import Path
from typing import Union

import pytest

from taxpasta.infrastructure.application import BrackenProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "2611_se-ERR5766174-db1_S.tsv",
            [
                (0, 0, "Saccharomyces cerevisiae"),
                (0, 1, 4932),
                (0, 2, "S"),
                (0, 3, 96),
                (0, 4, 0),
                (0, 5, 96),
                (0, 6, 0.80672),
                (1, 0, "Homo sapiens"),
                (1, 1, 9606),
                (1, 2, "S"),
                (1, 3, 23),
                (1, 4, 0),
                (1, 5, 23),
                (1, 6, 0.19328),
            ],
        ),
        (
            "2613_pe-ERR5766181-db1_S.tsv",
            [
                (0, 0, "Homo sapiens"),
                (0, 1, 9606),
                (0, 2, "S"),
                (0, 3, 78),
                (0, 4, 0),
                (0, 5, 78),
                (0, 6, 1.00000),
            ],
        ),
    ],
)
def test_read_correctness(
    bracken_data_dir: Path,
    filename: str,
    checks: list[tuple[int, int, Union[float, int, str]]],
):
    """Test that the reader can parse valid Bracken profiles."""
    profile = BrackenProfileReader.read(bracken_data_dir / filename)
    for row, col, value in checks:
        assert profile.iat[row, col] == value
