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


"""Test the sample merging application."""

from pathlib import Path

import pandas as pd
import pytest

from taxpasta.application import SampleHandlingApplication
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SupportedProfiler,
)


def test_zero_warning(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
):
    """Expect that a warning is emitted about additional zeroes."""
    monkeypatch.chdir(tmp_path)
    profile_1 = Path("profile_1.tsv")
    with profile_1.open(mode="a") as handle:
        handle.writelines(["#\n"] * 4)
        pd.DataFrame(
            [
                ("k__Bacteria", "2", 100.0, None),
                ("k__Bacteria|p__Actinobacteria", "2|201174", 100.0, None),
            ],
        ).to_csv(handle, sep="\t", index=False, header=False)
    profile_2 = Path("profile_2.tsv")
    with profile_2.open(mode="a") as handle:
        handle.writelines(["#\n"] * 4)
        pd.DataFrame(
            [
                ("k__Bacteria", "2", 100.0, None),
                ("k__Bacteria|p__Firmicutes", "2|1239", 100.0, None),
            ],
        ).to_csv(handle, sep="\t", index=False, header=False)
    app = SampleHandlingApplication(
        profile_reader=ApplicationServiceRegistry.profile_reader(
            SupportedProfiler.metaphlan,
        ),
        profile_standardiser=ApplicationServiceRegistry.profile_standardisation_service(
            SupportedProfiler.metaphlan,
        ),
    )
    samples = [
        app.etl_sample("profile_1", profile_1),
        app.etl_sample("profile_2", profile_2),
    ]
    with caplog.at_level("WARNING"):
        app.merge_samples(
            samples,
            wide_format=True,
        )
    assert any("zeroes were introduced" in msg for msg in caplog.messages)
