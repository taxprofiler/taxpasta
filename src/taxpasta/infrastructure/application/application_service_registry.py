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
    def profile_reader(cls, profiler: SupportedProfiler) -> type[ProfileReader]:  # noqa: C901, PLR0911
        """Return a profile reader of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileReader

            return BrackenProfileReader

        if profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileReader

            return CentrifugeProfileReader

        if profiler is SupportedProfiler.diamond:
            from .diamond import DiamondProfileReader

            return DiamondProfileReader

        if profiler is SupportedProfiler.ganon:
            from .ganon import GanonProfileReader

            return GanonProfileReader

        if profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileReader

            return KaijuProfileReader

        if profiler is SupportedProfiler.kmcp:
            from .kmcp import KMCPProfileReader

            return KMCPProfileReader

        if profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileReader

            return Kraken2ProfileReader

        if profiler is SupportedProfiler.krakenuniq:
            from .krakenuniq import KrakenUniqProfileReader

            return KrakenUniqProfileReader

        if profiler is SupportedProfiler.megan6:
            from .megan6 import Megan6ProfileReader

            return Megan6ProfileReader

        if profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileReader

            return MetaphlanProfileReader

        if profiler is SupportedProfiler.motus:
            from .motus import MotusProfileReader

            return MotusProfileReader

        msg = f"Unexpected profiler: {profiler}"
        raise ValueError(msg)

    @classmethod
    def profile_standardisation_service(  # noqa: C901, PLR0911
        cls,
        profiler: SupportedProfiler,
    ) -> type[ProfileStandardisationService]:
        """Return a profile standardisation service of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileStandardisationService

            return BrackenProfileStandardisationService

        if profiler is SupportedProfiler.centrifuge:
            from .centrifuge import CentrifugeProfileStandardisationService

            return CentrifugeProfileStandardisationService

        if profiler is SupportedProfiler.diamond:
            from .diamond import DiamondProfileStandardisationService

            return DiamondProfileStandardisationService

        if profiler is SupportedProfiler.kaiju:
            from .kaiju import KaijuProfileStandardisationService

            return KaijuProfileStandardisationService

        if profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileStandardisationService

            return Kraken2ProfileStandardisationService

        if profiler is SupportedProfiler.krakenuniq:
            from .krakenuniq import KrakenUniqProfileStandardisationService

            return KrakenUniqProfileStandardisationService

        if profiler is SupportedProfiler.megan6:
            from .megan6 import Megan6ProfileStandardisationService

            return Megan6ProfileStandardisationService

        if profiler is SupportedProfiler.motus:
            from .motus import MotusProfileStandardisationService

            return MotusProfileStandardisationService

        if profiler is SupportedProfiler.metaphlan:
            from .metaphlan import MetaphlanProfileStandardisationService

            return MetaphlanProfileStandardisationService

        if profiler is SupportedProfiler.ganon:
            from .ganon import GanonProfileStandardisationService

            return GanonProfileStandardisationService

        if profiler is SupportedProfiler.kmcp:
            from .kmcp import KMCPProfileStandardisationService

            return KMCPProfileStandardisationService

        msg = f"Unexpected profiler: {profiler}"
        raise ValueError(msg)

    @classmethod
    def standard_profile_writer(
        cls,
        file_format: StandardProfileFileFormat,
    ) -> type[StandardProfileWriter]:
        """Return a standard profile writer of the correct type."""
        if file_format is StandardProfileFileFormat.TSV:
            from .standard_profile_writer.tsv_standard_profile_writer import (
                TSVStandardProfileWriter,
            )

            return TSVStandardProfileWriter

        if file_format is StandardProfileFileFormat.CSV:
            from .standard_profile_writer.csv_standard_profile_writer import (
                CSVStandardProfileWriter,
            )

            return CSVStandardProfileWriter

        if file_format is StandardProfileFileFormat.XLSX:
            from .standard_profile_writer.xlsx_standard_profile_writer import (
                XLSXStandardProfileWriter,
            )

            return XLSXStandardProfileWriter

        if file_format is StandardProfileFileFormat.ODS:
            from .standard_profile_writer.ods_standard_profile_writer import (
                ODSStandardProfileWriter,
            )

            return ODSStandardProfileWriter

        if file_format is StandardProfileFileFormat.arrow:
            from .standard_profile_writer.arrow_standard_profile_writer import (
                ArrowStandardProfileWriter,
            )

            return ArrowStandardProfileWriter

        if file_format is StandardProfileFileFormat.parquet:
            from .standard_profile_writer.parquet_standard_profile_writer import (
                ParquetStandardProfileWriter,
            )

            return ParquetStandardProfileWriter

        msg = (
            f"The given file format {file_format.name} is not a supported tidy "
            f"observation table writer format."
        )
        raise ValueError(msg)

    @classmethod
    def table_reader(cls, file_format: TableReaderFileFormat) -> type[TableReader]:
        """Return a table reader of the correct type."""
        if file_format is TableReaderFileFormat.TSV:
            from .table_reader.tsv_table_reader import TSVTableReader

            return TSVTableReader

        if file_format is TableReaderFileFormat.CSV:
            from .table_reader.csv_table_reader import CSVTableReader

            return CSVTableReader

        if file_format is TableReaderFileFormat.XLSX:
            from .table_reader.xlsx_table_reader import XLSXTableReader

            return XLSXTableReader

        if file_format is TableReaderFileFormat.ODS:
            from .table_reader.ods_table_reader import ODSTableReader

            return ODSTableReader

        if file_format is TableReaderFileFormat.arrow:
            from .table_reader.arrow_table_reader import ArrowTableReader

            return ArrowTableReader

        if file_format is TableReaderFileFormat.parquet:
            from .table_reader.parquet_table_reader import ParquetTableReader

            return ParquetTableReader

        msg = (
            f"The given file format {file_format.name} is not a supported table "
            f"reader format.",
        )
        raise ValueError(msg)

    @classmethod
    def tidy_observation_table_writer(
        cls,
        file_format: TidyObservationTableFileFormat,
    ) -> type[TidyObservationTableWriter]:
        """Return a tidy table writer of the correct type."""
        if file_format is TidyObservationTableFileFormat.TSV:
            from .tidy_observation_table_writer.tsv_table_writer import (
                TSVTidyObservationTableWriter,
            )

            return TSVTidyObservationTableWriter

        if file_format is TidyObservationTableFileFormat.CSV:
            from .tidy_observation_table_writer.csv_table_writer import (
                CSVTidyObservationTableWriter,
            )

            return CSVTidyObservationTableWriter

        if file_format is TidyObservationTableFileFormat.XLSX:
            from .tidy_observation_table_writer.xlsx_table_writer import (
                XLSXTidyObservationTableWriter,
            )

            return XLSXTidyObservationTableWriter

        if file_format is TidyObservationTableFileFormat.ODS:
            from .tidy_observation_table_writer.ods_table_writer import (
                ODSTidyObservationTableWriter,
            )

            return ODSTidyObservationTableWriter

        if file_format is TidyObservationTableFileFormat.arrow:
            from .tidy_observation_table_writer.arrow_table_writer import (
                ArrowTidyObservationTableWriter,
            )

            return ArrowTidyObservationTableWriter

        if file_format is TidyObservationTableFileFormat.parquet:
            from .tidy_observation_table_writer.parquet_table_writer import (
                ParquetTidyObservationTableWriter,
            )

            return ParquetTidyObservationTableWriter

        msg = (
            f"The given file format {file_format.name} is not a supported tidy "
            f"observation table writer format."
        )
        raise ValueError(msg)

    @classmethod
    def wide_observation_table_writer(  # noqa: PLR0911
        cls,
        file_format: WideObservationTableFileFormat,
    ) -> type[WideObservationTableWriter]:
        """Return a writer for wide observation tables in the specified format."""
        if file_format is WideObservationTableFileFormat.TSV:
            from .wide_observation_table_writer.tsv_wide_observation_table_writer import (  # noqa: E501
                TSVWideObservationTableWriter,
            )

            return TSVWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.CSV:
            from .wide_observation_table_writer.csv_wide_observation_table_writer import (  # noqa: E501
                CSVWideObservationTableWriter,
            )

            return CSVWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.XLSX:
            from .wide_observation_table_writer.xlsx_wide_observation_table_writer import (  # noqa: E501
                XLSXWideObservationTableWriter,
            )

            return XLSXWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.ODS:
            from .wide_observation_table_writer.ods_wide_observation_table_writer import (  # noqa: E501
                ODSWideObservationTableWriter,
            )

            return ODSWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.arrow:
            from .wide_observation_table_writer.arrow_wide_observation_table_writer import (  # noqa: E501
                ArrowWideObservationTableWriter,
            )

            return ArrowWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.parquet:
            from .wide_observation_table_writer.parquet_wide_observation_table_writer import (  # noqa: E501
                ParquetWideObservationTableWriter,
            )

            return ParquetWideObservationTableWriter

        if file_format is WideObservationTableFileFormat.BIOM:
            from .wide_observation_table_writer.biom_wide_observation_table_writer import (  # noqa: E501
                BIOMWideObservationTableWriter,
            )

            return BIOMWideObservationTableWriter

        msg = (
            f"The given file format {file_format.name} is not a supported "
            f"observation matrix writer format."
        )
        raise ValueError(msg)
