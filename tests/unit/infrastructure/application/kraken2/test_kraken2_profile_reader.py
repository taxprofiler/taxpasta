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


"""Test that the reader can parse valid kraken2 profiles."""


from pathlib import Path
from typing import List, Tuple, Union

import pytest

from taxpasta.infrastructure.application import Kraken2ProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "2611_se-ERR5766174-db1.kraken2.report.txt",
            [
                (0, 0, 99.98),
                (0, 1, 787758),
                (0, 2, 787758),
                (0, 5, "unclassified"),
                (1, 0, 0.02),
                (1, 1, 119),
                (1, 2, 0),
                (1, 5, "root"),
                (15, 0, 0.01),
                (15, 1, 96),
                (15, 2, 96),
                (15, 5, "Saccharomyces cerevisiae S288C"),
                (43, 0, 0.00),
                (43, 1, 23),
                (43, 2, 23),
                (43, 5, "Homo sapiens"),
            ],
        ),
        (
            "2611_se-ERR5766174-db2.kraken2.report.txt.gz",
            [
                (0, 0, 99.98),
                (0, 1, 787758),
                (0, 2, 787758),
                (0, 5, "unclassified"),
                (1, 0, 0.02),
                (1, 1, 119),
                (1, 2, 0),
                (1, 5, "root"),
                (15, 0, 0.01),
                (15, 1, 96),
                (15, 2, 96),
                (15, 5, "Saccharomyces cerevisiae S288C"),
                (43, 0, 0.00),
                (43, 1, 23),
                (43, 2, 23),
                (43, 5, "Homo sapiens"),
            ],
        ),
        (
            "2612_pe-ERR5766176-db1.kraken2.report.txt",
            [
                (0, 0, 99.97),
                (0, 1, 627680),
                (0, 2, 627680),
                (0, 5, "unclassified"),
                (1, 0, 0.03),
                (1, 1, 168),
                (1, 2, 0),
                (1, 5, "root"),
                (32, 0, 0.02),
                (32, 1, 152),
                (32, 2, 152),
                (32, 5, "Homo sapiens"),
                (43, 0, 0.00),
                (43, 1, 16),
                (43, 2, 16),
                (43, 5, "Saccharomyces cerevisiae S288C"),
            ],
        ),
        (
            "2612_pe-ERR5766176-db2.kraken2.report.txt.gz",
            [
                (0, 0, 99.97),
                (0, 1, 627680),
                (0, 2, 627680),
                (0, 5, "unclassified"),
                (1, 0, 0.03),
                (1, 1, 168),
                (1, 2, 0),
                (1, 5, "root"),
                (32, 0, 0.02),
                (32, 1, 152),
                (32, 2, 152),
                (32, 5, "Homo sapiens"),
                (43, 0, 0.00),
                (43, 1, 16),
                (43, 2, 16),
                (43, 5, "Saccharomyces cerevisiae S288C"),
            ],
        ),
    ],
)
def test_read_correctness(
    kraken2_data_dir: Path,
    filename: str,
    checks: List[Tuple[int, int, Union[float, int, str]]],
):
    """Test that the reader can parse valid kraken2 profiles."""
    profile = Kraken2ProfileReader.read(kraken2_data_dir / filename)
    for row, col, value in checks:
        assert profile.iat[row, col] == value
