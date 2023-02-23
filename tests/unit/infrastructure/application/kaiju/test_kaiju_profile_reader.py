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


"""Test that the reader can parse valid kaiju profiles."""


from pathlib import Path
from typing import List, Tuple, Union

import pytest

from taxpasta.infrastructure.application import KaijuProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "barcode41_se-barcode41-kaiju.txt",
            [
                (1, 3, "1902245"),
                (4, 2, 292),
                (16, 4, "taxonid:2590016"),
            ],
        ),
        (
            "barcode42_se-barcode42-kaiju.txt",
            [
                (1, 1, 1.693967),
                (2, 2, 91),
                (489, 4, "unclassified"),
            ],
        ),
    ],
)
def test_read_correctness(
    kaiju_data_dir: Path,
    filename: str,
    checks: List[Tuple[int, int, Union[float, int, str]]],
):
    """Test that the reader can parse valid centrifuge profiles."""
    profile = KaijuProfileReader.read(kaiju_data_dir / filename)
    for row, col, value in checks:
        assert profile.iat[row, col] == value
