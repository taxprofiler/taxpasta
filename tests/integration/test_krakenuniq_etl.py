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


"""Test that KrakenUniq profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    KrakenUniqProfileReader,
    KrakenUniqProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "test1.krakenuniq.report.txt",
        pytest.param(
            "test1-invalid.krakenuniq.report.txt",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_read_correctness(
    krakenuniq_data_dir: Path,
    filename: str,
):
    """Test that KrakenUniq profiles are read, validated, and transformed correctly."""
    KrakenUniqProfileStandardisationService.transform(
        KrakenUniqProfileReader.read(krakenuniq_data_dir / filename)
    )
