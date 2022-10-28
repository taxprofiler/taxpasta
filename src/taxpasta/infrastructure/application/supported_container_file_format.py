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


"""Provide a service for supported container file formats."""


from __future__ import annotations

from enum import Enum, unique
from pathlib import Path


@unique
class SupportedContainerFileFormat(str, Enum):
    """Define the supported container file formats."""

    BIOM = "BIOM"

    @classmethod
    def guess_format(cls, filename: Path) -> SupportedContainerFileFormat:
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
                f"Unrecognized file type extension {''.join(filename.suffixes)}."
            )
        elif len(common) > 1:
            raise ValueError(
                f"Ambiguous file type extension {''.join(filename.suffixes)}."
            )
        else:
            return supported_formats[common.pop()]

    @classmethod
    def check_dependencies(cls, file_format: SupportedContainerFileFormat) -> None:
        """
        Test that relevant dependencies are installed.

        Args:
            file_format: The file format for which to check dependencies.

        Raises:
            RuntimeError: If the required dependency could not be imported.

        """
        if file_format is cls.BIOM:
            try:
                import biom  # noqa: F401
            except ImportError as error:
                raise RuntimeError(
                    f"The desired file format '{file_format}' is currently not "
                    f"available. Please install 'taxpasta[biom]' to support it."
                ) from error
