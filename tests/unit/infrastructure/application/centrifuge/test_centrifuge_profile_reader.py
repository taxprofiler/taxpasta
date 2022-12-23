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


"""Test that the reader can parse valid centrifuge profiles."""


from pathlib import Path
from typing import List, Tuple, Union

import pytest

from taxpasta.infrastructure.application import CentrifugeProfileReader


@pytest.mark.parametrize(
    ("filename", "checks"),
    [
        (
            "AD_pe-db1.centrifuge.txt",
            [
                (0, 5, "unclassified"),
                (1, 5, "root"),
                (4, 1, 23),
                (4, 0, 23.23),
                (15, 0, 1.01),
                (15, 1, 1),
                (15, 2, 1),
                (15, 5, "Torque teno virus 13"),
                (43, 0, 1.01),
                (43, 1, 1),
                (43, 2, 1),
                (43, 5, "Lactobacillus prophage Lj771"),
            ],
        ),
        (
            "barcode52_se-db1.centrifuge.txt",
            [
                (0, 0, 0.00),
                (0, 1, 0),
                (0, 2, 0),
                (0, 5, "unclassified"),
                (1, 0, 100),
                (1, 1, 203),
                (1, 2, 0),
                (1, 5, "root"),
                (15, 0, 0.49),
                (15, 1, 1),
                (15, 2, 1),
                (15, 5, "Staphylococcus virus 71"),
                (43, 0, 0.49),
                (43, 1, 1),
                (43, 2, 1),
                (43, 5, "Staphylococcus phage phiNM3"),
            ],
        ),
    ],
)
def test_read_correctness(
    centrifuge_data_dir: Path,
    filename: str,
    checks: List[Tuple[int, int, Union[float, int, str]]],
):
    """Test that the reader can parse valid centrifuge profiles."""
    profile = CentrifugeProfileReader.read(centrifuge_data_dir / filename)
    for (row, col, value) in checks:
        assert profile.iat[row, col] == value
