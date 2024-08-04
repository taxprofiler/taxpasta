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


"""Test that the reader can parse valid diamond profiles."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from taxpasta.infrastructure.application import DiamondProfileReader


if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "diamond_valid_1.tsv",
            [
                (1, 1, 511145),
                (2, 2, 1.55e-12),
                (4, 0, "escherichia_coli_962/1"),
            ],
        ),
    ],
)
def test_read_correctness(
    diamond_data_dir: Path,
    filename: str,
    checks: list[tuple[int, int, int | float | str]],
):
    """Test that the reader can parse valid diamond profiles."""
    profile = DiamondProfileReader.read(diamond_data_dir / filename)
    for row, col, value in checks:
        assert profile.iat[row, col] == value
