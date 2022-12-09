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


"""Test that mOTUs profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    MotusProfileReader,
    MotusProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "2612_se-ERR5766180-db_mOTU.out",
        pytest.param(
            "2612_se-ERR5766180-invalid_db_mOTU.out",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_read_correctness(
    motus_data_dir: Path,
    filename: str,
):
    """Test that mOTUs profiles are read, validated, and transformed correctly."""
    MotusProfileStandardisationService.transform(
        MotusProfileReader.read(motus_data_dir / filename)
    )
