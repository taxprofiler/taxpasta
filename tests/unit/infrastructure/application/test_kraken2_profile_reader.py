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


"""Test that the reader can parse valid kraken2 profiles."""


from pathlib import Path

import pytest

from taxpasta.infrastructure.application import Kraken2ProfileReader


PROFILES = [
    obj
    for obj in (
        Path(__file__).parent.parent.parent.parent / "data" / "kraken2"
    ).iterdir()
    if obj.is_file()
]


@pytest.fixture(scope="module", params=PROFILES)
def kraken2_profile(request) -> Path:
    return request.param


def test_read(kraken2_profile):
    Kraken2ProfileReader.read(kraken2_profile)
