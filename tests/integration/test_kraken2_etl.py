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


"""Test that kraken2 profiles are read, validated, and transformed correctly."""


from pathlib import Path

import pytest
from pandera.errors import SchemaErrors

from taxpasta.application.error import StandardisationError
from taxpasta.infrastructure.application import (
    Kraken2ProfileReader,
    Kraken2ProfileStandardisationService,
)


@pytest.fixture(
    scope="module",
    params=[
        ("bracken", "2612_pe-ERR5766176_B-db1_S.tsv"),
        # The tabular Centrifuge output is identical to the Kraken2 one.
        # ("centrifuge", "AD_pe-db1.centrifuge.txt"),  # noqa: E800
        ("diamond", "diamond_valid_1.tsv"),
        ("ganon", "2612_pe_ERR5766176_db1.ganon.tre"),
        ("kaiju", "barcode41_se-barcode41-kaiju.txt"),
        ("kmcp", "2612_pe_ERR5766176_db1.kmcp_profile.profile"),
        # ("kraken2", "2612_pe-ERR5766176-db1.kraken2.report.txt"),  # noqa: E800
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
@pytest.mark.filterwarnings("error::UserWarning")
def test_kraken2_etl(
    kraken2_data_dir: Path,
    filename: str,
):
    """Test that kraken2 profiles are read, validated, and transformed correctly."""
    Kraken2ProfileStandardisationService.transform(
        Kraken2ProfileReader.read(kraken2_data_dir / filename)
    )


def test_failure_on_other_profiles(other_profile: Path):
    """Expect that profiles from other profilers fail validation."""
    with pytest.raises((ValueError, SchemaErrors, StandardisationError)):
        Kraken2ProfileStandardisationService.transform(
            Kraken2ProfileReader.read(other_profile)
        )
