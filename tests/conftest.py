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


"""Provide fixtures to all pytest modules."""


from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="session")
def runner() -> CliRunner:
    """Return a CLI runner instance for testing."""
    return CliRunner(mix_stderr=False)


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Provide the path to the global data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def kraken2_data_dir(data_dir: Path) -> Path:
    """Provide the path to the kraken2 data directory."""
    return data_dir / "kraken2"


@pytest.fixture(scope="session")
def bracken_data_dir(data_dir: Path) -> Path:
    """Provide the path to the Bracken data directory."""
    return data_dir / "bracken"


@pytest.fixture(scope="session")
def metaphlan_data_dir(data_dir: Path) -> Path:
    """Provide the path to the metaphlan data directory."""
    return data_dir / "metaphlan"


@pytest.fixture(scope="session")
def centrifuge_data_dir(data_dir: Path) -> Path:
    """Provide the path to the centrifuge data directory."""
    return data_dir / "centrifuge"


@pytest.fixture(scope="session")
def kaiju_data_dir(data_dir: Path) -> Path:
    """Provide the path to the kaiju data directory."""
    return data_dir / "kaiju"


@pytest.fixture(scope="session")
def diamond_data_dir(data_dir: Path) -> Path:
    """Provide the path to the diamond data directory."""
    return data_dir / "diamond"


@pytest.fixture(scope="session")
def megan6_data_dir(data_dir: Path) -> Path:
    """Provide the path to the MEGAN6 rma2info data directory."""
    return data_dir / "megan6"


@pytest.fixture(scope="session")
def krakenuniq_data_dir(data_dir: Path) -> Path:
    """Provide the path to the KrakenUniq data directory."""
    return data_dir / "krakenuniq"


@pytest.fixture(scope="session")
def motus_data_dir(data_dir: Path) -> Path:
    """Provide the path to the mOTUs data directory."""
    return data_dir / "motus"


@pytest.fixture(scope="session")
def ganon_data_dir(data_dir: Path) -> Path:
    """Provide the path to the ganon data directory."""
    return data_dir / "ganon"
