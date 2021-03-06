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


"""Provide an abstract base class for reading taxonomic profiles."""


from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class ProfileReader(ABC):
    """Define an abstract base class for reading taxonomic profiles."""

    @classmethod
    @abstractmethod
    def read(cls, profile: Path) -> pd.DataFrame:
        """Read a taxonomic profile from a file."""
