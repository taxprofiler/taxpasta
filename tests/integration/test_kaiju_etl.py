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


"""Test that kaiju profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    KaijuProfileReader,
    KaijuProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "barcode41_se-barcode41-kaiju.txt",
        "barcode42_se-barcode42-kaiju.txt",
        pytest.param(
            "barcode41_se-barcode41-invalid.kaiju.txt",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_kaiju_etl(
    kaiju_data_dir: Path,
    filename: str,
):
    """Test that kaiju profiles are read, validated, and transformed correctly."""
    KaijuProfileStandardisationService.transform(
        KaijuProfileReader.read(kaiju_data_dir / filename)
    )
