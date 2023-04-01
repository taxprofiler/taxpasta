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


"""Provide a description of samples and profile locations."""


from pathlib import Path
from typing import cast

import pandera as pa
from pandera.typing import DataFrame, Series


class SampleSheet(pa.DataFrameModel):
    """Define a description of samples and profile locations."""

    sample: Series[str] = pa.Field()
    profile: Series[str] = pa.Field()  # type: ignore

    @pa.dataframe_check
    @classmethod
    def check_number_samples(cls, table: DataFrame) -> bool:
        """Check that there are at least two samples."""
        return (table[cls.sample].notnull() & table[cls.profile].notnull()).sum() > 1

    @pa.check("profile", name="profile_presence")
    @classmethod
    def check_profile_presence(
        cls, profile: Series[str]  # type: ignore
    ) -> Series[bool]:
        """Check that every profile is present at the specified location."""
        return cast(Series[bool], profile.map(lambda path: Path(path).is_file()))

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
        strict = True
