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


"""Test the taxpasta command line interface."""


from pathlib import Path
from typing import List

import pytest
from typer.testing import CliRunner

import taxpasta
from taxpasta.domain import StandardProfile
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SupportedProfiler,
    SupportedTabularFileFormat,
)
from taxpasta.infrastructure.cli import app


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    """Return a CLI runner instance for testing."""
    return CliRunner(mix_stderr=False)


@pytest.fixture(scope="module", params=list(SupportedProfiler))
def profiler(request) -> SupportedProfiler:
    """Provide each supported profiler in turn."""
    return request.param


@pytest.fixture(scope="module", params=list(SupportedTabularFileFormat))
def file_format(request) -> SupportedTabularFileFormat:
    """Provide each supported tabular file format in turn."""
    return request.param


@pytest.fixture(scope="module")
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


@pytest.mark.parametrize("args", [["-h", "--help"]])
def test_help(runner: CliRunner, args: List[str]):
    """Expect that the help can be requested successfully."""
    result = runner.invoke(app, args)
    assert result.exit_code == 0


def test_version(runner: CliRunner):
    """Expect that the version can be requested successfully."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == taxpasta.__version__


@pytest.mark.parametrize(
    "args",
    [
        ["--log-level", "DEBUG"],
        ["--log-level", "INFO"],
        ["--log-level", "WARNING"],
        ["--log-level", "ERROR"],
        ["--log-level", "CRITICAL"],
        ["-l", "DEBUG"],
        ["-l", "INFO"],
        ["-l", "WARNING"],
        ["-l", "ERROR"],
        ["-l", "CRITICAL"],
    ],
)
def test_log_level(runner: CliRunner, args: List[str]):
    """Expect that the log level can be set successfully."""
    result = runner.invoke(app, args)
    assert result.exit_code == 0


def test_merge_wide(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: List[str],
    file_format: SupportedTabularFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a wide format can be created."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{file_format.name.lower()}"
    result = runner.invoke(
        app,
        ["merge", "--wide", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    reader = ApplicationServiceRegistry.table_reader(file_format)
    df = reader.read(output)
    assert df.columns[0] == StandardProfile.taxonomy_id
    assert len(df.columns) == len(profiles) + 1


def test_merge_long(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: List[str],
    file_format: SupportedTabularFileFormat,
    data_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a long format can be created."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{file_format.name.lower()}"
    result = runner.invoke(
        app,
        ["merge", "--long", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    reader = ApplicationServiceRegistry.table_reader(file_format)
    df = reader.read(output)
    assert len(df.columns) == 3
    assert df.columns.tolist() == [
        StandardProfile.taxonomy_id,
        StandardProfile.count,
        "sample",
    ]
