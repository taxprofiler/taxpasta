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


from .bracken import (
    BrackenProfile,
    BrackenProfileReader,
    BrackenProfileStandardisationService,
)
from .centrifuge import (
    CentrifugeProfile,
    CentrifugeProfileReader,
    CentrifugeProfileStandardisationService,
)
from .diamond import (
    DiamondProfile,
    DiamondProfileReader,
    DiamondProfileStandardisationService,
)
from .kaiju import (
    KaijuProfile,
    KaijuProfileReader,
    KaijuProfileStandardisationService,
)
from .kraken2 import (
    Kraken2Profile,
    Kraken2ProfileReader,
    Kraken2ProfileStandardisationService,
)
from .malt import (
    MaltProfile,
    MaltProfileReader,
    MaltProfileStandardisationService,
)
from .metaphlan import (
    MetaphlanProfile,
    MetaphlanProfileReader,
    MetaphlanProfileStandardisationService,
)
from .application_service_registry import ApplicationServiceRegistry
from .sample_sheet import SampleSheet
from .sample_merging_application import SampleMergingApplication
from .supported_profiler import SupportedProfiler
from .supported_tabular_file_format import SupportedTabularFileFormat
