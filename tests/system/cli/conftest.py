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


"""Provide fixtures to all the CLI end-to-end tests."""


from pathlib import Path
from typing import List

import pandas as pd
import pytest
from typer.testing import CliRunner

from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SupportedProfiler,
    SupportedTabularFileFormat,
)


@pytest.fixture(scope="session")
def runner() -> CliRunner:
    """Return a CLI runner instance for testing."""
    return CliRunner(mix_stderr=False)


@pytest.fixture(scope="session", params=list(SupportedProfiler))
def profiler(request: pytest.FixtureRequest) -> SupportedProfiler:
    """Provide each supported profiler in turn."""
    return request.param


@pytest.fixture(scope="session", params=list(SupportedTabularFileFormat))
def file_format(request: pytest.FixtureRequest) -> SupportedTabularFileFormat:
    """Provide each supported tabular file format in turn."""
    return request.param


@pytest.fixture(scope="session")
def profiles(
    profiler: SupportedProfiler,
    data_dir: Path,
) -> List[str]:
    """Provide valid profiles for each profiler in turn."""
    return [
        str(filename)
        for filename in (data_dir / profiler.name).glob("*")
        if "invalid" not in filename.name
    ]


@pytest.fixture(scope="session")
def samplesheet(
    profiler: SupportedProfiler,
    file_format: SupportedTabularFileFormat,
    data_dir: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Provide a sample sheet for each profiler in turn."""
    sheet = pd.DataFrame(
        data=[
            (filename.stem, str(filename))
            for filename in (data_dir / profiler.name).glob("*")
            if "invalid" not in filename.name
        ],
        columns=["sample", "profile"],
    )
    path = (
        tmp_path_factory.mktemp(profiler.name)
        / f"samplesheet.{file_format.name.lower()}"
    )
    writer = ApplicationServiceRegistry.table_writer(file_format)
    writer.write(sheet, path)
    return path
