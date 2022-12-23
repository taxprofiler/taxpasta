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


"""Provide a mixin for checking Python package dependencies."""


from __future__ import annotations

from enum import Enum
from pathlib import Path


class DependencyCheckMixin(Enum):
    """Define a mixin for checking Python package dependencies."""

    @classmethod
    def guess_format(cls, filename: Path) -> DependencyCheckMixin:
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
        supported_formats = {option.value.upper(): option for option in cls}
        common = suffixes.intersection(supported_formats)
        if not common:
            raise ValueError(
                f"Unrecognized file type extension '{''.join(filename.suffixes)}'."
            )
        elif len(common) > 1:
            raise ValueError(
                f"Ambiguous file type extension '{''.join(filename.suffixes)}'."
            )
        else:
            return supported_formats[common.pop()]

    @classmethod
    def check_dependencies(cls, file_format: DependencyCheckMixin) -> None:
        """
        Test that relevant dependencies are installed.

        Args:
            file_format: The file format for which to check dependencies.

        Raises:
            RuntimeError: If the required dependency could not be imported.

        """
        try:
            assert isinstance(file_format.value, str)  # nosec assert_used
            supported_format = getattr(cls, file_format.value)
        except AttributeError:
            raise RuntimeError(
                f"The file format to be checked '{file_format.value}' is not supported "
                f"by this class {cls.__name__}."
            )
        # Call the file format's corresponding check, if it exists.
        getattr(cls, f"_check_{supported_format.value.lower()}", lambda: None)()

    @classmethod
    def _check_ods(cls) -> None:
        """Check for dependencies for the ODS file format."""
        try:
            import odf  # noqa: F401
        except ImportError as error:
            raise RuntimeError(
                "The desired file format 'ODS' is currently not "
                "available. Please `pip install 'taxpasta[ods]'` to support it."
            ) from error

    @classmethod
    def _check_xlsx(cls) -> None:
        """Check for dependencies for the XLSX file format."""
        try:
            import openpyxl  # noqa: F401
        except ImportError as error:
            raise RuntimeError(
                "The desired file format 'XLSX' is currently not "
                "available. Please `pip install 'taxpasta[xlsx]'` to support it."
            ) from error

    @classmethod
    def _check_arrow(cls) -> None:
        """Check for dependencies for the arrow file format."""
        try:
            import pyarrow  # noqa: F401
        except ImportError as error:
            raise RuntimeError(
                "The desired file format 'arrow' is currently not "
                "available. Please `pip install 'taxpasta[arrow]'` to support it."
            ) from error

    @classmethod
    def _check_biom(cls) -> None:
        """Check for dependencies for the BIOM file format."""
        try:
            import biom  # noqa: F401
        except ImportError as error:
            raise RuntimeError(
                "The desired file format 'BIOM' is currently not "
                "available. Please `pip install 'taxpasta[biom]'` to support it."
            ) from error
