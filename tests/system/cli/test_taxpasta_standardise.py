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


"""Test the taxpasta standardise command."""


from pathlib import Path

import pytest
from typer.testing import CliRunner

from taxpasta.infrastructure.application import (
    StandardProfileFileFormat,
    SupportedProfiler,
)
from taxpasta.infrastructure.cli import app


def test_standardise(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profile: Path,
    standard_profile_format: StandardProfileFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a profile can be standardised."""
    monkeypatch.chdir(tmp_path)
    output = Path(f"result.{standard_profile_format.name.lower()}")
    result = runner.invoke(
        app,
        [
            "standardise",
            "--profiler",
            profiler.name,
            "--output",
            str(output),
            str(profile),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert output.is_file()
