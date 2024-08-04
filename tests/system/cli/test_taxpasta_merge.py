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


"""Test the taxpasta merge command."""

import sys
from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from taxpasta.infrastructure.application import (
    ApplicationServiceRegistry,
    SupportedProfiler,
    TableReaderFileFormat,
    TidyObservationTableFileFormat,
    WideObservationTableFileFormat,
)
from taxpasta.infrastructure.cli import app


BAD_ARGUMENT_EXIT_CODE = 2


@pytest.fixture(scope="session", params=list(TableReaderFileFormat))
def kraken2_samplesheet(
    data_dir: Path,
    tmp_path_factory: pytest.TempPathFactory,
    request: pytest.FixtureRequest,
) -> Path:
    """Provide a sample sheet for each profiler in turn."""
    sheet = pd.DataFrame(
        data=[
            (filename.stem, str(filename))
            for filename in (data_dir / SupportedProfiler.kraken2.value).glob("*")
            if "invalid" not in filename.name
        ],
        columns=["sample", "profile"],
    )
    path = (
        tmp_path_factory.mktemp(SupportedProfiler.kraken2.value)
        / f"samplesheet.{request.param.value.lower()}"
    )
    writer = ApplicationServiceRegistry.tidy_observation_table_writer(
        TidyObservationTableFileFormat(request.param.value),
    )
    writer.write(sheet, path)
    return path


def test_merge_profiles_wide(  # noqa: PLR0913
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: list[str],
    wide_observation_table_format: WideObservationTableFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that for each profiler and file format, a wide format can be created."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{wide_observation_table_format.name.lower()}"
    result = runner.invoke(
        app,
        ["merge", "--wide", "--profiler", profiler.name, "--output", output, *profiles],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()


def test_merge_profiles_long(  # noqa: PLR0913
    runner: CliRunner,
    profiler: SupportedProfiler,
    profiles: list[str],
    tidy_observation_table_format: TidyObservationTableFileFormat,
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


def test_merge_samplesheet_wide(  # noqa: PLR0913
    runner: CliRunner,
    profiler: SupportedProfiler,
    tsv_samplesheet: Path,
    wide_observation_table_format: WideObservationTableFileFormat,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a wide format output can be generated from a sample sheet."""
    monkeypatch.chdir(tmp_path)
    output = f"result.{wide_observation_table_format.name.lower()}"
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
            str(tsv_samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()


def test_merge_samplesheet_long(  # noqa: PLR0913
    runner: CliRunner,
    profiler: SupportedProfiler,
    tsv_samplesheet: Path,
    tidy_observation_table_format: TidyObservationTableFileFormat,
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
            str(tsv_samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert Path(output).is_file()


@pytest.mark.parametrize(
    ("samplesheet_format", "dependencies"),
    [
        (TableReaderFileFormat.XLSX, ("openpyxl",)),
        (TableReaderFileFormat.ODS, ("odf",)),
        (TableReaderFileFormat.arrow, ("pyarrow",)),
    ],
)
def test_missing_samplesheet_dependencies(  # noqa: PLR0913
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
    with caplog.at_level("CRITICAL"):
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
        (WideObservationTableFileFormat.arrow, ("pyarrow",)),
        (WideObservationTableFileFormat.BIOM, ("biom",)),
    ],
)
def test_missing_wide_table_dependencies(  # noqa: PLR0913
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
    with caplog.at_level("CRITICAL"):
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
        (TidyObservationTableFileFormat.arrow, ("pyarrow",)),
    ],
)
def test_missing_tidy_table_dependencies(  # noqa: PLR0913
    runner: CliRunner,
    tidy_table_format: TidyObservationTableFileFormat,
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
    with caplog.at_level("CRITICAL"):
        result = runner.invoke(
            app,
            [
                "merge",
                "--long",
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


def test_samplesheet_formats(
    runner: CliRunner,
    kraken2_samplesheet: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a sample sheet can be read in from every supported format."""
    monkeypatch.chdir(tmp_path)
    output = Path("result.tsv")
    result = runner.invoke(
        app,
        [
            "merge",
            "--long",
            "--profiler",
            "kraken2",
            "--output",
            str(output),
            "--samplesheet",
            str(kraken2_samplesheet),
        ],
    )
    assert result.exit_code == 0, result.stderr
    assert output.is_file()


def test_bad_wide_output(
    runner: CliRunner,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a bad wide table output file extension is caught."""
    monkeypatch.chdir(tmp_path)
    output = Path("result.txt")
    output.touch()
    sheet = Path("samples.tsv")
    sheet.touch()
    with caplog.at_level("CRITICAL"):
        result = runner.invoke(
            app,
            [
                "merge",
                "--profiler",
                "kraken2",
                "--output",
                str(output),
                "--samplesheet",
                str(sheet),
            ],
        )
    assert result.exit_code == BAD_ARGUMENT_EXIT_CODE, result.stderr
    assert any("extension" in msg for msg in caplog.messages)


def test_bad_long_output(
    runner: CliRunner,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a bad long table output file extension is caught."""
    monkeypatch.chdir(tmp_path)
    output = Path("result.txt")
    output.touch()
    sheet = Path("samples.tsv")
    sheet.touch()
    with caplog.at_level("CRITICAL"):
        result = runner.invoke(
            app,
            [
                "merge",
                "--long",
                "--profiler",
                "kraken2",
                "--output",
                str(output),
                "--samplesheet",
                str(sheet),
            ],
        )
    assert result.exit_code == BAD_ARGUMENT_EXIT_CODE, result.stderr
    assert any("extension" in msg for msg in caplog.messages)


def test_bad_samplesheet_extension(
    runner: CliRunner,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that a bad sample sheet file extension is caught."""
    monkeypatch.chdir(tmp_path)
    sheet = Path("result.txt")
    sheet.touch()
    with caplog.at_level("CRITICAL"):
        result = runner.invoke(
            app,
            [
                "merge",
                "--long",
                "--profiler",
                "kraken2",
                "--output",
                str(sheet),
                "--samplesheet",
                str(sheet),
            ],
        )
    assert result.exit_code == BAD_ARGUMENT_EXIT_CODE, result.stderr
    assert any("extension" in msg for msg in caplog.messages)
