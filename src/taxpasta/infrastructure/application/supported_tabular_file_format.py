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


"""Provide a service for supported tabular file formats."""


from __future__ import annotations

from enum import Enum, unique
from pathlib import Path

import pandas as pd


@unique
class SupportedTabularFileFormat(str, Enum):
    """Define the supported tabular file formats."""

    TSV = "TSV"
    CSV = "CSV"
    ODS = "ODS"
    XLSX = "XLSX"
    arrow = "arrow"

    @classmethod
    def guess_format(cls, filename: Path) -> SupportedTabularFileFormat:
        """
        Guess the desired format from a file's extensions.

        Args:
            filename: The filename itself or a complete path.

        Returns:
            The supported format if it can be guessed.

        Raises:
            ValueError: If the filename has no supported format or the file extensions
                are ambiguous.

        """
        # Set of all suffixes without the dot.
        suffixes = {suffix[1:].upper() for suffix in filename.suffixes}
        # Mapping of supported output formats.
        supported_formats = {option.name.upper(): option for option in cls}
        common = suffixes.intersection(supported_formats)
        if not common:
            raise ValueError(
                f"Unrecognized output file type extension {''.join(filename.suffixes)}."
            )
        elif len(common) > 1:
            raise ValueError(
                f"Ambiguous output file type extension {''.join(filename.suffixes)}."
            )
        else:
            return supported_formats[common.pop()]

    @classmethod
    def check_dependencies(cls, file_format: SupportedTabularFileFormat) -> None:
        """
        Test that relevant dependencies are installed.

        Args:
            file_format: The file format for which to check dependencies.

        Raises:
            ImportError: If the required dependency could not be imported.

        """
        if file_format is cls.ODS:
            try:
                import odf  # noqa: F401
            except ImportError as error:
                raise ImportError(
                    f"The desired file format '{file_format}' is currently not "
                    f"available. Please install the package 'odfpy' to support it."
                ) from error
        elif file_format is cls.XLSX:
            try:
                import openpyxl  # noqa: F401
            except ImportError as error:
                raise ImportError(
                    f"The desired file format '{file_format}' is currently not "
                    f"available. Please install the package 'openpyxl' to support it."
                ) from error
        elif file_format is cls.arrow:
            try:
                import pyarrow  # noqa: F401
            except ImportError as error:
                raise ImportError(
                    f"The desired file format '{file_format}' is currently not "
                    f"available. Please install the package 'pyarrow' to support it."
                ) from error

    @classmethod
    def write_table(
        cls,
        table: pd.DataFrame,
        filename: Path,
        file_format: SupportedTabularFileFormat,
        **kwargs,
    ) -> None:
        """
        Write a table to a file in the desired format.

        Args:
            table: The table to be written.
            filename: The path where the file should be written.
            file_format: The desired output file format.
            kwargs: Any keyword arguments are passed to the underlying writing method
                allowing for additional customization.

        """
        if file_format is cls.TSV:
            table.to_csv(filename, sep="\t", index=False, **kwargs)
        elif file_format is cls.CSV:
            table.to_csv(filename, index=False, **kwargs)
        elif file_format is cls.XLSX:
            table.to_excel(filename, index=False, engine="openpyxl", **kwargs)
        elif file_format is cls.ODS:
            table.to_excel(filename, index=False, engine="odf", **kwargs)
        elif file_format is cls.arrow:
            table.to_feather(filename, **kwargs)
