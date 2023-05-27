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


"""Test that diamond profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.application.error import StandardisationError
from taxpasta.infrastructure.application import (
    DiamondProfileReader,
    DiamondProfileStandardisationService,
)


@pytest.fixture(
    scope="module",
    params=[
        ("bracken", "2612_pe-ERR5766176_B-db1_S.tsv"),
        ("centrifuge", "AD_pe-db1.centrifuge.txt"),
        # ("diamond", "diamond_valid_1.tsv"),  # noqa: E800
        ("kaiju", "barcode41_se-barcode41-kaiju.txt"),
        ("kraken2", "2612_pe-ERR5766176-db1.kraken2.report.txt"),
        ("krakenuniq", "test1.krakenuniq.report.txt"),
        ("megan6", "malt_rma2info_valid.txt.gz"),
        ("metaphlan", "mpa_valid_complex.tsv"),
        ("motus", "2612_pe-ERR5766176-db_mOTU.out"),
    ],
)
def other_profile(data_dir: Path, request: pytest.FixtureRequest) -> Path:
    """Return parametrized paths to other profilers' profiles."""
    profiler, filename = request.param
    return data_dir / profiler / filename


@pytest.mark.parametrize(
    "filename",
    [
        "diamond_valid_1.tsv",
        "diamond_valid_2.tsv",
        pytest.param(
            "diamond_invalid_1.tsv",
            marks=pytest.mark.raises(exception=SchemaErrors),
        ),
        pytest.param(
            "diamond_invalid_2.tsv",
            marks=pytest.mark.raises(exception=SchemaErrors),
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


def test_failure_on_other_profiles(other_profile: Path):
    """Expect that profiles from other profilers fail validation."""
    with pytest.raises((ValueError, SchemaErrors, StandardisationError)):
        DiamondProfileStandardisationService.transform(
            DiamondProfileReader.read(other_profile)
        )
