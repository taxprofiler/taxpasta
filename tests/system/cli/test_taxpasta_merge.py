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
import sys
from pathlib import Path
from typing import Iterable, List

import pytest
from typer.testing import CliRunner

from taxpasta.infrastructure.application import (
    SupportedProfiler,
    TableReaderFileFormat,
    TidyObservationTableFileFormat,
    WideObservationTableFileFormat,
)
from taxpasta.infrastructure.cli import app


def test_merge_profiles_wide(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: List[str],
    observation_matrix_format: WideObservationTableFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a wide format can be created."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{observation_matrix_format.name.lower()}"
    result = runner.invoke(
        app,
        ["merge", "--wide", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()


def test_merge_profiles_long(
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: List[str],
    tidy_observation_table_format: TidyObservationTableFileFormat,
    data_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a long format can be created."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{tidy_observation_table_format.name.lower()}"
    result = runner.invoke(
        app,
        ["merge", "--long", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()


def test_merge_samplesheet_wide(
    runner: CliRunner,
    profiler: SupportedProfiler,
    samplesheet: Path,
    observation_matrix_format: WideObservationTableFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a wide format output can be generated from a sample sheet."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{observation_matrix_format.name.lower()}"
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


def test_merge_samplesheet_long(
    runner: CliRunner,
    profiler: SupportedProfiler,
    samplesheet: Path,
    tidy_observation_table_format: TidyObservationTableFileFormat,
    data_dir: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a long format output can be generated from a sample sheet."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{tidy_observation_table_format.name.lower()}"
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


@pytest.mark.parametrize(
    ("samplesheet_format", "dependencies"),
    [
        (TableReaderFileFormat.XLSX, ("openpyxl",)),
        (TableReaderFileFormat.ODS, ("odf",)),
        (TableReaderFileFormat.arrow, ("arrow",)),
    ],
)
def test_missing_samplesheet_dependencies(
    runner: CliRunner,
    samplesheet_format: TableReaderFileFormat,
    dependencies: Iterable[str],
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Ensure that unsupported sample sheet formats exit with an error."""
    monkeypatch.chdir(tmp_path)
    for dep in dependencies:
        monkeypatch.setitem(sys.modules, dep, None)
    sheet = Path(f"samples.{samplesheet_format.value.lower()}")
    sheet.touch()
    result = runner.invoke(
        app,
        [
            "merge",
            "--profiler",
            SupportedProfiler.kraken2.value,
            "--output",
            "results.tsv",
            "--samplesheet",
            str(sheet),
        ],
    )
    assert result.exit_code == 1
    assert any("pip install" in msg for msg in caplog.messages)


@pytest.mark.parametrize(
    ("wide_table_format", "dependencies"),
    [
        (WideObservationTableFileFormat.XLSX, ("openpyxl",)),
        (WideObservationTableFileFormat.ODS, ("odf",)),
        (WideObservationTableFileFormat.arrow, ("arrow",)),
        (WideObservationTableFileFormat.BIOM, ("biom",)),
    ],
)
def test_missing_wide_table_dependencies(
    runner: CliRunner,
    wide_table_format: WideObservationTableFileFormat,
    dependencies: Iterable[str],
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Ensure that unsupported wide observation table formats exit with an error."""
    monkeypatch.chdir(tmp_path)
    for dep in dependencies:
        monkeypatch.setitem(sys.modules, dep, None)
    sheet = Path("samples.tsv")
    sheet.touch()
    result = runner.invoke(
        app,
        [
            "merge",
            "--profiler",
            SupportedProfiler.kraken2.value,
            "--output",
            f"results.{wide_table_format.value}",
            "--samplesheet",
            str(sheet),
        ],
    )
    assert result.exit_code == 1
    assert any("pip install" in msg for msg in caplog.messages)


@pytest.mark.parametrize(
    ("tidy_table_format", "dependencies"),
    [
        (TidyObservationTableFileFormat.XLSX, ("openpyxl",)),
        (TidyObservationTableFileFormat.ODS, ("odf",)),
        (TidyObservationTableFileFormat.arrow, ("arrow",)),
    ],
)
def test_missing_tidy_table_dependencies(
    runner: CliRunner,
    tidy_table_format: WideObservationTableFileFormat,
    dependencies: Iterable[str],
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Ensure that unsupported tidy observation table formats exit with an error."""
    monkeypatch.chdir(tmp_path)
    for dep in dependencies:
        monkeypatch.setitem(sys.modules, dep, None)
    sheet = Path("samples.tsv")
    sheet.touch()
    result = runner.invoke(
        app,
        [
            "merge",
            "--profiler",
            SupportedProfiler.kraken2.value,
            "--output",
            f"results.{tidy_table_format.value}",
            "--samplesheet",
            str(sheet),
        ],
    )
    assert result.exit_code == 1
    assert any("pip install" in msg for msg in caplog.messages)
