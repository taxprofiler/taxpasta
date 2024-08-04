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


"""Test that the reader can parse valid KMCP profiles."""


from pathlib import Path
from typing import Union

import pytest

from taxpasta.infrastructure.application import KMCPProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "2612_pe_ERR5766176_db1.kmcp_profile.profile",
            [
                (0, 0, "test_1"),
                (0, 1, 100.00000),
                (0, 2, 1.238685),
            ],
        ),
    ],
)
def test_read_correctness(
    kmcp_data_dir: Path,
    filename: str,
    checks: list[tuple[int, int, Union[float, int, str]]],
):
    """Test that the reader can parse valid KMCP profiles."""
    profile = KMCPProfileReader.read(kmcp_data_dir / filename)
    for row, col, value in checks:
        assert profile.iat[row, col] == value
