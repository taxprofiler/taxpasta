# Copyright (c) 2023 Moritz E. Beber
# Copyright (c) 2023 Maxime Borry
# Copyright (c) 2023 James A. Fellows Yates
# Copyright (c) 2023 Sofia Stamouli.
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


"""Test that taxpasta returns a semantic versioning string."""


from typer.testing import CliRunner

import taxpasta
from taxpasta.infrastructure.cli import app


def test_dunder_version_is_defined():
    """Expect that the version is defined."""
    assert taxpasta.__version__ != "undefined"


def test_cli_version(runner: CliRunner):
    """Expect that the CLI returns the same version as the package."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.stderr
    assert result.stdout.strip() == taxpasta.__version__
