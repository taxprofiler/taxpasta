# flake8: noqa
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


"""Provide an application service registry."""


from typing import Type

from taxpasta.application.service import (
    ObservationMatrixWriter,
    ProfileReader,
    ProfileStandardisationService,
    TableReader,
    TidyObservationTableWriter,
)

from .observation_matrix_file_format import ObservationMatrixFileFormat
from .supported_profiler import SupportedProfiler
from .table_reader_file_format import TableReaderFileFormat
from .tidy_observation_table_file_format import TidyObservationTableFileFormat


class ApplicationServiceRegistry:
    """Define an application service registry."""

    @classmethod
    def profile_reader(cls, profiler: SupportedProfiler) -> Type[ProfileReader]:
        """Return a profile reader of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileReader

            return BrackenProfileReader
        elif profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileReader

            return CentrifugeProfileReader
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileReader

            return KaijuProfileReader
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileReader

            return Kraken2ProfileReader
        elif profiler is SupportedProfiler.malt:
            from .malt import MaltProfileReader

            return MaltProfileReader
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileReader

            return MetaphlanProfileReader
        else:
            raise ValueError("Unexpected")

    @classmethod
    def profile_standardisation_service(
        cls, profiler: SupportedProfiler
    ) -> Type[ProfileStandardisationService]:
        """Return a profile standardisation service of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileStandardisationService

            return BrackenProfileStandardisationService
        elif profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileStandardisationService

            return CentrifugeProfileStandardisationService
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileStandardisationService

            return KaijuProfileStandardisationService
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileStandardisationService

            return Kraken2ProfileStandardisationService
        elif profiler is SupportedProfiler.malt:
            from .malt import MaltProfileStandardisationService

            return MaltProfileStandardisationService
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileStandardisationService

            return MetaphlanProfileStandardisationService
        else:
            raise ValueError("Unexpected")

    @classmethod
    def table_reader(cls, file_format: TableReaderFileFormat) -> Type[TableReader]:
        """Return a table reader of the correct type."""
        if file_format is TableReaderFileFormat.TSV:
            from .table_reader.tsv_table_reader import TSVTableReader

            return TSVTableReader
        elif file_format is TableReaderFileFormat.CSV:
            from .table_reader.csv_table_reader import CSVTableReader

            return CSVTableReader
        elif file_format is TableReaderFileFormat.XLSX:
            from .table_reader.xlsx_table_reader import XLSXTableReader

            return XLSXTableReader
        elif file_format is TableReaderFileFormat.ODS:
            from .table_reader.ods_table_reader import ODSTableReader

            return ODSTableReader
        elif file_format is TableReaderFileFormat.arrow:
            from .table_reader.arrow_table_reader import ArrowTableReader

            return ArrowTableReader
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported table "
                f"reader format."
            )

    @classmethod
    def tidy_observation_table_writer(
        cls, file_format: TidyObservationTableFileFormat
    ) -> Type[TidyObservationTableWriter]:
        """Return a table writer of the correct type."""
        if file_format is TidyObservationTableFileFormat.TSV:
            from .tidy_observation_table_writer.tsv_table_writer import (
                TSVTidyObservationTableWriter,
            )

            return TSVTidyObservationTableWriter
        elif file_format is TidyObservationTableFileFormat.CSV:
            from .tidy_observation_table_writer.csv_table_writer import (
                CSVTidyObservationTableWriter,
            )

            return CSVTidyObservationTableWriter
        elif file_format is TidyObservationTableFileFormat.XLSX:
            from .tidy_observation_table_writer.xlsx_table_writer import (
                XLSXTidyObservationTableWriter,
            )

            return XLSXTidyObservationTableWriter
        elif file_format is TidyObservationTableFileFormat.ODS:
            from .tidy_observation_table_writer.ods_table_writer import (
                ODSTidyObservationTableWriter,
            )

            return ODSTidyObservationTableWriter
        elif file_format is TidyObservationTableFileFormat.arrow:
            from .tidy_observation_table_writer.arrow_table_writer import (
                ArrowTidyObservationTableWriter,
            )

            return ArrowTidyObservationTableWriter
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported tidy "
                f"observation table writer format."
            )

    @classmethod
    def observation_matrix_writer(
        cls, file_format: ObservationMatrixFileFormat
    ) -> Type[ObservationMatrixWriter]:
        """Return a container writer of the correct type."""
        if file_format is ObservationMatrixFileFormat.TSV:
            from .observation_matrix_writer.tsv_observation_matrix_writer import (
                TSVObservationMatrixWriter,
            )

            return TSVObservationMatrixWriter
        elif file_format is ObservationMatrixFileFormat.CSV:
            from .observation_matrix_writer.csv_observation_matrix_writer import (
                CSVObservationMatrixWriter,
            )

            return CSVObservationMatrixWriter
        elif file_format is ObservationMatrixFileFormat.XLSX:
            from .observation_matrix_writer.xlsx_observation_matrix_writer import (
                XLSXObservationMatrixWriter,
            )

            return XLSXObservationMatrixWriter
        elif file_format is ObservationMatrixFileFormat.ODS:
            from .observation_matrix_writer.ods_observation_matrix_writer import (
                ODSObservationMatrixWriter,
            )

            return ODSObservationMatrixWriter
        elif file_format is ObservationMatrixFileFormat.arrow:
            from .observation_matrix_writer.arrow_observation_matrix_writer import (
                ArrowObservationMatrixWriter,
            )

            return ArrowObservationMatrixWriter
        elif file_format is ObservationMatrixFileFormat.BIOM:
            from .observation_matrix_writer.biom_container_writer import (
                BIOMObservationMatrixWriter,
            )

            return BIOMObservationMatrixWriter
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported "
                f"observation matrix writer format."
            )
