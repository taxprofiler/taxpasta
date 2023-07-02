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


"""Provide a reader for metaphlan profiles."""


from io import TextIOWrapper
from pathlib import Path
from typing import BinaryIO, TextIO

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.application.service import BufferOrFilepath, ProfileReader
from taxpasta.infrastructure.helpers import raise_parser_warnings

from .metaphlan_profile import MetaphlanProfile


class MetaphlanProfileReader(ProfileReader):
    """Define a reader for Metaphlan profiles."""

    @classmethod
    @raise_parser_warnings
    def read(cls, profile: BufferOrFilepath) -> DataFrame[MetaphlanProfile]:
        """Read a metaphlan taxonomic profile from a file."""
        num_header_lines = cls._detect_number_header_line(profile)
        result = pd.read_table(
            filepath_or_buffer=profile,
            sep="\t",
            skiprows=num_header_lines,
            header=None,
            index_col=False,
            names=[
                MetaphlanProfile.clade_name,
                MetaphlanProfile.ncbi_tax_id,
                MetaphlanProfile.relative_abundance,
                MetaphlanProfile.additional_species,
            ],
            dtype={MetaphlanProfile.ncbi_tax_id: str},
        )
        cls._check_num_columns(result, MetaphlanProfile)
        return result

    @classmethod
    def _detect_number_header_line(cls, profile: BufferOrFilepath) -> int:
        """
        Detect the number of comment lines in the header of a MetaPhlAn profile.

        The number of lines varies at least between versions 3 & 4.

        """
        if isinstance(profile, BinaryIO):
            # We assume default file encoding here (UTF-8 in most environments).
            result = cls._detect_first_content_line(buffer=TextIOWrapper(profile))
            profile.seek(0)
            return result
        elif isinstance(profile, TextIO):
            result = cls._detect_first_content_line(buffer=profile)
            profile.seek(0)
            return result
        else:
            with Path(profile).open(mode="r") as handle:
                return cls._detect_first_content_line(buffer=handle)

    @classmethod
    def _detect_first_content_line(
        cls, buffer: TextIO, comment_marker: str = "#", max_lines: int = 10
    ) -> int:
        """Detect the first non-comment line in the given text buffer."""
        for num, line in enumerate(buffer):
            if not line.startswith(comment_marker):
                return num
            if num >= max_lines:
                raise ValueError(
                    "Unexpectedly large number of comment lines in MetaPhlAn "
                    "profile (>10)."
                )
        else:
            raise ValueError("Could not detect any content lines in MetaPhlAn profile.")
