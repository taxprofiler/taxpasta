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


"""Test that Bracken profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    BrackenProfileReader,
    BrackenProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "2611_se-ERR5766174-db1_S.tsv",
        "2612_pe-ERR5766176-db1_S.tsv",
        "2613_pe-ERR5766181-db1_S.tsv",
        "2612_pe-ERR5766176_B-db1_S.tsv",
        "2612_se-ERR5766180-db1_S.tsv",
        pytest.param(
            "2611_se-ERR5766174-db1_S_invalid.tsv",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
        pytest.param(
            "2612_pe-ERR5766176_B-db1_S_invalid.tsv",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_bracken_etl(
    bracken_data_dir: Path,
    filename: str,
):
    """Test that Bracken profiles are read, validated, and transformed correctly."""
    BrackenProfileStandardisationService.transform(
        BrackenProfileReader.read(bracken_data_dir / filename)
    )
