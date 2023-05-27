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


"""Test that MEGAN6 rma2info profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandas.errors import ParserError
from pandera.errors import SchemaErrors

from taxpasta.application.error import StandardisationError
from taxpasta.infrastructure.application import (
    Megan6ProfileReader,
    Megan6ProfileStandardisationService,
)


@pytest.fixture(
    scope="module",
    params=[
        ("bracken", "2612_pe-ERR5766176_B-db1_S.tsv"),
        ("centrifuge", "AD_pe-db1.centrifuge.txt"),
        ("diamond", "diamond_valid_1.tsv"),
        ("kaiju", "barcode41_se-barcode41-kaiju.txt"),
        ("kraken2", "2612_pe-ERR5766176-db1.kraken2.report.txt"),
        ("krakenuniq", "test1.krakenuniq.report.txt"),
        # ("megan6", "malt_rma2info_valid.txt.gz"),  # noqa: E800
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
    megan6_data_dir: Path,
    filename: str,
):
    """Test that megan6 profiles are read, validated, and transformed correctly."""
    Megan6ProfileStandardisationService.transform(
        Megan6ProfileReader.read(megan6_data_dir / filename)
    )


def test_failure_on_other_profiles(other_profile: Path):
    """Expect that profiles from other profilers fail validation."""
    with pytest.raises((ValueError, SchemaErrors, StandardisationError)):
        Megan6ProfileStandardisationService.transform(
            Megan6ProfileReader.read(other_profile)
        )
