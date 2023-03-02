# flake8: noqa
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


"""Provide an abstract base class for consensus building applications."""


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from pandera.typing import DataFrame

from taxpasta.domain.model import StandardProfile


class ConsensusApplication(ABC):
    """Define an abstract base class for consensus building applications."""

    @classmethod
    @abstractmethod
    def run(
        cls, profiles: Iterable[DataFrame[StandardProfile]], taxonomy: Path
    ) -> DataFrame:
        """
        Build a consensus from two or more taxonomic profiles.

        Args:
            profiles: Standardized profiles.
            taxonomy: Provide a shared taxonomy.

        """
        # FIXME: Rough idea on application.
        # builder = ConsensusBuilder()
        # for profile in profiles:
        #     builder.add_profile(profile)
        # return builder.build()
