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


"""Test that kraken2 profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    Kraken2ProfileReader,
    Kraken2ProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "2611_se-ERR5766174-db1.kraken2.report.txt",
        "2611_se-ERR5766174-db2.kraken2.report.txt.gz",
        "2612_pe-ERR5766176-db1.kraken2.report.txt",
        "2612_pe-ERR5766176-db2.kraken2.report.txt.gz",
        pytest.param(
            "2611_se-ERR5766174-db1-invalid.kraken2.report.txt",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
        pytest.param(
            "2612_pe-ERR5766176-db1-invalid.kraken2.report.txt",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_read_correctness(
    kraken2_data_dir: Path,
    filename: str,
):
    """Test that kraken2 profiles are read, validated, and transformed correctly."""
    Kraken2ProfileStandardisationService.transform(
        Kraken2ProfileReader.read(kraken2_data_dir / filename)
    )
