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


"""Test that MALT-rma2info profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandas.errors import ParserError

from taxpasta.infrastructure.application import (
    MaltProfileReader,
    MaltProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "malt_rma2info_valid.txt.gz",
        pytest.param(
            "malt_rma2info_invalid_1.txt.gz",
            marks=pytest.mark.raises(exception=ParserError),
        ),
        "ERX5474930_ERR5766174_1.txt.gz",
        "ERX5474932_ERR5766176_1.txt.gz",
        "ERX5474932_ERR5766176_2.txt.gz",
        "ERX5474932_ERR5766176_B_1.txt.gz",
        "ERX5474932_ERR5766176_B_2.txt.gz",
        "ERX5474936_ERR5766180_1.txt.gz",
        "ERX5474937_ERR5766181_1.txt.gz",
        "ERX5474937_ERR5766181_2.txt.gz",
    ],
)
def test_read_correctness(
    malt_data_dir: Path,
    filename: str,
):
    """Test that malt profiles are read, validated, and transformed correctly."""
    MaltProfileStandardisationService.transform(
        MaltProfileReader.read(malt_data_dir / filename)
    )
