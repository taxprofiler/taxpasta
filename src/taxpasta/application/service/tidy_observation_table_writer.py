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


"""Provide an abstract base class for writing tidy observation tables."""


from abc import ABC, abstractmethod

from pandera.typing import DataFrame

from taxpasta.domain.model import TidyObservationTable

from ._types import BufferOrFilepath


class TidyObservationTableWriter(ABC):
    """Define an abstract base class for writing tidy observation tables."""

    @classmethod
    @abstractmethod
    def write(
        cls, table: DataFrame[TidyObservationTable], target: BufferOrFilepath, **kwargs
    ) -> None:
        """Write a tidy observation table to the given buffer or file."""
