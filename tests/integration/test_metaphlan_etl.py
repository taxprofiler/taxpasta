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


"""Test that metaphlan profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandas.errors import ParserError
from pandera.errors import SchemaErrors

from taxpasta.infrastructure.application import (
    MetaphlanProfileReader,
    MetaphlanProfileStandardisationService,
)


@pytest.mark.parametrize(
    "filename",
    [
        "mpa_valid_simple.tsv",
        "mpa_valid_complex.tsv",
        pytest.param(
            "mpa_invalid_tabs.tsv",
            marks=pytest.mark.raises(exception=ParserError),
        ),
        pytest.param(
            "mpa_invalid_abundance_sum.tsv",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
    ],
)
def test_read_correctness(
    metaphlan_data_dir: Path,
    filename: str,
):
    """Test that kraken2 profiles are read, validated, and transformed correctly."""
    MetaphlanProfileStandardisationService.transform(
        MetaphlanProfileReader.read(metaphlan_data_dir / filename)
    )
