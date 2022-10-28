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


"""Test the taxpasta merge command."""


from pathlib import Path
from typing import List

import pytest
from biom.table import Table
from biom.util import biom_open
from typer.testing import CliRunner

from taxpasta.domain import StandardProfile
from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SampleSheet,
    SupportedProfiler,
    SupportedTabularFileFormat,
)
from taxpasta.infrastructure.cli import app


def test_merge_profiles_wide(
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


def test_merge_profiles_biom(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: List[str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a wide format can be created."""
    monkeypatch.chdir(tmp_path)
    output = "result.biom"
    result = runner.invoke(
        app,
        ["merge", "--biom", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    with biom_open(output) as handle:
        container = Table.from_hdf5(handle)
    assert len(container.ids()) == len(profiles)


def test_merge_profiles_long(
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


def test_merge_samplesheet_wide(
    runner: CliRunner,
    profiler: SupportedProfiler,
    samplesheet: Path,
    file_format: SupportedTabularFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a wide format output can be generated from a sample sheet."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{file_format.name.lower()}"
    result = runner.invoke(
        app,
        [
            "merge",
            "--wide",
            "--profiler",
            profiler.name,
            "--output",
            output,
            "--samplesheet",
            str(samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    reader = ApplicationServiceRegistry.table_reader(file_format)
    df = reader.read(output)
    sheet = reader.read(samplesheet)
    samples = sheet[SampleSheet.sample]
    assert df.columns[0] == StandardProfile.taxonomy_id
    assert len(df.columns) == len(samples) + 1
    assert set(df.columns[1:]) == set(samples)


def test_merge_samplesheet_biom(
    runner: CliRunner,
    profiler: SupportedProfiler,
    samplesheet: Path,
    file_format: SupportedTabularFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a wide format can be created."""
    monkeypatch.chdir(tmp_path)
    output = "result.biom"
    result = runner.invoke(
        app,
        [
            "merge",
            "--biom",
            "--profiler",
            profiler.name,
            "--output",
            output,
            "--samplesheet",
            str(samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    reader = ApplicationServiceRegistry.table_reader(file_format)
    sheet = reader.read(samplesheet)
    samples = sheet[SampleSheet.sample]
    with biom_open(output) as handle:
        container = Table.from_hdf5(handle)
    assert len(container.ids()) == len(samples)
    assert set(container.ids()) == set(samples)


def test_merge_samplesheet_long(
    runner: CliRunner,
    profiler: SupportedProfiler,
    samplesheet: Path,
    file_format: SupportedTabularFileFormat,
    data_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a long format output can be generated from a sample sheet."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{file_format.name.lower()}"
    result = runner.invoke(
        app,
        [
            "merge",
            "--long",
            "--profiler",
            profiler.name,
            "--output",
            output,
            "--samplesheet",
            str(samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()
    reader = ApplicationServiceRegistry.table_reader(file_format)
    df = reader.read(output)
    sheet = reader.read(samplesheet)
    samples = sheet[SampleSheet.sample]
    assert len(df.columns) == 3
    assert df.columns.tolist() == [
        StandardProfile.taxonomy_id,
        StandardProfile.count,
        "sample",
    ]
    assert set(df["sample"].unique()) == set(samples)
