# Copyright (c) 2022, Moritz E. Beber, Maxime Borry, Sofia Stamouli.
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


"""Test the main taxpasta command line interface."""


import sys
from typing import List

import pytest
from typer.testing import CliRunner

import taxpasta
from taxpasta.infrastructure.cli import app


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
def test_log_level_with_rich(runner: CliRunner, args: List[str]):
    """Expect that the log level can be set successfully."""
    result = runner.invoke(app, args)
    assert result.exit_code == 0


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
def test_log_level_without_rich(
    runner: CliRunner, args: List[str], monkeypatch: pytest.MonkeyPatch
):
    """Expect that the log level can be set successfully."""
    monkeypatch.setitem(sys.modules, "rich", None)
    result = runner.invoke(app, args)
    assert result.exit_code == 0
