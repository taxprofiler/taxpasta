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


"""Provide a builder service for creating a consensus between many profiles."""


from abc import ABC, abstractmethod

import pandas as pd


class ConsensusBuilder(ABC):
    """Define a builder service for creating a consensus between many profiles."""

    @abstractmethod
    def add_profile(self, profile: pd.DataFrame) -> None:
        """Add a profile to the consensus builder."""

    @abstractmethod
    def build(self) -> pd.DataFrame:
        """Build the consensus between all added profiles."""
