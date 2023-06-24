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


"""Provide an application service registry."""


from typing import Type

from taxpasta.application.service import (
    ProfileReader,
    ProfileStandardisationService,
    StandardProfileWriter,
    TableReader,
    TidyObservationTableWriter,
    WideObservationTableWriter,
)

from .standard_profile_file_format import StandardProfileFileFormat
from .supported_profiler import SupportedProfiler
from .table_reader_file_format import TableReaderFileFormat
from .tidy_observation_table_file_format import TidyObservationTableFileFormat
from .wide_observation_table_file_format import WideObservationTableFileFormat


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
        elif profiler is SupportedProfiler.diamond:
            from .diamond import DiamondProfileReader

            return DiamondProfileReader
        elif profiler is SupportedProfiler.ganon:
            from .ganon import GanonProfileReader

            return GanonProfileReader
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileReader

            return KaijuProfileReader
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileReader

            return Kraken2ProfileReader
        elif profiler is SupportedProfiler.krakenuniq:
            from .krakenuniq import KrakenUniqProfileReader

            return KrakenUniqProfileReader
        elif profiler is SupportedProfiler.megan6:
            from .megan6 import Megan6ProfileReader

            return Megan6ProfileReader
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileReader

            return MetaphlanProfileReader
        elif profiler is SupportedProfiler.motus:
            from .motus import MotusProfileReader

            return MotusProfileReader

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
        elif profiler is SupportedProfiler.diamond:
            from .diamond import DiamondProfileStandardisationService

            return DiamondProfileStandardisationService
        elif profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileStandardisationService

            return KaijuProfileStandardisationService
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileStandardisationService

            return Kraken2ProfileStandardisationService
        elif profiler is SupportedProfiler.krakenuniq:
            from .krakenuniq import KrakenUniqProfileStandardisationService

            return KrakenUniqProfileStandardisationService
        elif profiler is SupportedProfiler.megan6:
            from .megan6 import Megan6ProfileStandardisationService

            return Megan6ProfileStandardisationService
        elif profiler is SupportedProfiler.motus:
            from .motus import MotusProfileStandardisationService

            return MotusProfileStandardisationService
        elif profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileStandardisationService

            return MetaphlanProfileStandardisationService
        elif profiler is SupportedProfiler.ganon:
            from .ganon import GanonProfileStandardisationService

            return GanonProfileStandardisationService

        else:
            raise ValueError("Unexpected")

    @classmethod
    def standard_profile_writer(
        cls, file_format: StandardProfileFileFormat
    ) -> Type[StandardProfileWriter]:
        """Return a standard profile writer of the correct type."""
        if file_format is StandardProfileFileFormat.TSV:
            from .standard_profile_writer.tsv_standard_profile_writer import (
                TSVStandardProfileWriter,
            )

            return TSVStandardProfileWriter
        elif file_format is StandardProfileFileFormat.CSV:
            from .standard_profile_writer.csv_standard_profile_writer import (
                CSVStandardProfileWriter,
            )

            return CSVStandardProfileWriter
        elif file_format is StandardProfileFileFormat.XLSX:
            from .standard_profile_writer.xlsx_standard_profile_writer import (
                XLSXStandardProfileWriter,
            )

            return XLSXStandardProfileWriter
        elif file_format is StandardProfileFileFormat.ODS:
            from .standard_profile_writer.ods_standard_profile_writer import (
                ODSStandardProfileWriter,
            )

            return ODSStandardProfileWriter
        elif file_format is StandardProfileFileFormat.arrow:
            from .standard_profile_writer.arrow_standard_profile_writer import (
                ArrowStandardProfileWriter,
            )

            return ArrowStandardProfileWriter
        elif file_format is StandardProfileFileFormat.parquet:
            from .standard_profile_writer.parquet_standard_profile_writer import (
                ParquetStandardProfileWriter,
            )

            return ParquetStandardProfileWriter
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported tidy "
                f"observation table writer format."
            )

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
        elif file_format is TableReaderFileFormat.parquet:
            from .table_reader.parquet_table_reader import ParquetTableReader

            return ParquetTableReader
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported table "
                f"reader format."
            )

    @classmethod
    def tidy_observation_table_writer(
        cls, file_format: TidyObservationTableFileFormat
    ) -> Type[TidyObservationTableWriter]:
        """Return a tidy table writer of the correct type."""
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
        elif file_format is TidyObservationTableFileFormat.parquet:
            from .tidy_observation_table_writer.parquet_table_writer import (
                ParquetTidyObservationTableWriter,
            )

            return ParquetTidyObservationTableWriter
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported tidy "
                f"observation table writer format."
            )

    @classmethod
    def wide_observation_table_writer(
        cls, file_format: WideObservationTableFileFormat
    ) -> Type[WideObservationTableWriter]:
        """Return a writer for wide observation tables in the specified format."""
        if file_format is WideObservationTableFileFormat.TSV:
            from .wide_observation_table_writer.tsv_wide_observation_table_writer import (
                TSVWideObservationTableWriter,
            )

            return TSVWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.CSV:
            from .wide_observation_table_writer.csv_wide_observation_table_writer import (
                CSVWideObservationTableWriter,
            )

            return CSVWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.XLSX:
            from .wide_observation_table_writer.xlsx_wide_observation_table_writer import (
                XLSXWideObservationTableWriter,
            )

            return XLSXWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.ODS:
            from .wide_observation_table_writer.ods_wide_observation_table_writer import (
                ODSWideObservationTableWriter,
            )

            return ODSWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.arrow:
            from .wide_observation_table_writer.arrow_wide_observation_table_writer import (
                ArrowWideObservationTableWriter,
            )

            return ArrowWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.parquet:
            from .wide_observation_table_writer.parquet_wide_observation_table_writer import (
                ParquetWideObservationTableWriter,
            )

            return ParquetWideObservationTableWriter
        elif file_format is WideObservationTableFileFormat.BIOM:
            from .wide_observation_table_writer.biom_wide_observation_table_writer import (
                BIOMWideObservationTableWriter,
            )

            return BIOMWideObservationTableWriter
        else:
            ValueError(
                f"The given file format {file_format.name} is not a supported "
                f"observation matrix writer format."
            )
