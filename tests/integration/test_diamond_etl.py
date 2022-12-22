# Copyright (c) 2022, Moritz E. Beber, Maxime Borry, Sofia Stamouli.
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


"""Test that diamond profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandas.errors import ParserError

from taxpasta.infrastructure.application import (
    DiamondProfileReader,
    DiamondProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "diamond_valid_1.tsv",
        "diamond_valid_2.tsv",
        pytest.param(
            "diamond_invalid_1.tsv",
            marks=pytest.mark.raises(exception=ParserError),
        ),
        pytest.param(
            "diamond_invalid_2.tsv",
            marks=pytest.mark.raises(exception=ParserError),
        ),
    ],
)
def test_read_correctness(
    diamond_data_dir: Path,
    filename: str,
):
    """Test that diamond profiles are read, validated, and transformed correctly."""
    DiamondProfileStandardisationService.transform(
        DiamondProfileReader.read(diamond_data_dir / filename)
    )
