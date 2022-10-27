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


"""Provide an TSV writer."""


import pandas as pd

from taxpasta.application import BufferOrFilepath, TableWriter


class TSVTableWriter(TableWriter):
    """Define the TSV writer."""

    @classmethod
    def write(cls, table: pd.DataFrame, target: BufferOrFilepath, **kwargs) -> None:
        """Write the given table to the given buffer or file."""
        table.to_csv(target, sep="\t", index=False, **kwargs)
