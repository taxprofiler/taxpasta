# Copyright (c) 2023 Moritz E. Beber
# Copyright (c) 2023 Maxime Borry
# Copyright (c) 2023 James A. Fellows Yates
# Copyright (c) 2023 Sofia Stamouli.
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


"""Test that the schema model validates kmcp profiles correctly."""


from collections import OrderedDict

import pandas as pd
import pytest
from pandera.errors import SchemaError

from taxpasta.infrastructure.application import KmcpProfile


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("ref", ["test_1"]),
                    ("percentage", [100.0]),
                    ("coverage", [1.23]),
                    ("score", [83.97]),
                    ("chunksFrac", [1.0]),
                    ("chunksRelDepth", [1.0]),
                    ("chunksRelDepthStd", [0.0]),
                    ("reads", [114]),
                    ("ureads", [114]),
                    ("hicureads", [25]),
                    ("refsize", [13897]),
                    ("refname", ["test_1"]),
                    ("taxid", [2697049]),
                    ("rank", ["species"]),
                    ("taxname", ["SARS-CoV-2"]),
                    ("taxpath", ["taxdump"]),
                    ("taxpathsn", ["taxdump"]),

                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("ref", ["test_1"]),
                        ("percentage", [100.0]),
                        ("coverage", [1.23]),
                        ("score", [83.97]),
                        ("chunksFrac", [1.0]),
                        ("chunksRelDepth", [1.0]),
                        ("chunksRelDepthStd", [0.0]),
                        ("reads", [114]),
                        ("ureads", [114]),
                        ("hicureads", [25]),
                        ("refsize", [13897]),
                        ("refname", ["test_1"]),
                        ("taxid", [2697049]),
                        ("taxname", ["SARS-CoV-2"]),
                        ("taxpath", ["taxdump"]),
                        ("taxpathsn", ["taxdump"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="column 'rank' not in dataframe",
            ),
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("ref", ["test_1"]),
                        ("coverage", [1.23]),
                        ("percentage", [100.0]),
                        ("score", [83.97]),
                        ("chunksFrac", [1.0]),
                        ("chunksRelDepth", [1.0]),
                        ("chunksRelDepthStd", [0.0]),
                        ("reads", [114]),
                        ("ureads", [114]),
                        ("hicureads", [25]),
                        ("refsize", [13897]),
                        ("refname", ["test_1"]),
                        ("taxid", [2697049]),
                        ("rank", ["species"]),
                        ("taxname", ["SARS-CoV-2"]),
                        ("taxpath", ["taxdump"]),
                        ("taxpathsn", ["taxdump"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="column 'percentage' out-of-order"
            ),
        ),
    ],
)
def test_column_presence(profile: pd.DataFrame):
    """Test that column names and order are validated."""
    KmcpProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("ref", ["test_1", "test_2"]),
                    ("percentage", [100.0, 0.0]),
                    ("coverage", [1.23, 1.23]),
                    ("score", [83.97, 83.97]),
                    ("chunksFrac", [1.0, 1.0]),
                    ("chunksRelDepth", [1.0, 1.0]),
                    ("chunksRelDepthStd", [0.0, 0.0]),
                    ("reads", [114, 114]),
                    ("ureads", [114, 114]),
                    ("hicureads", [25, 25]),
                    ("refsize", [13897, 13897]),
                    ("refname", ["test_1", "test_2"]),
                    ("taxid", [2697049, 2697049]),
                    ("rank", ["species", "species"]),
                    ("taxname", ["SARS-CoV-2", "SARS-CoV-2"]),
                    ("taxpath", ["taxdump", "taxdump"]),
                    ("taxpathsn", ["taxdump", "taxdump"]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("ref", ["test_1", "test_2"]),
                        ("percentage", [72.38712, 39.61288]),
                        ("coverage", [1.23, 1.23]),
                        ("score", [83.97, 83.97]),
                        ("chunksFrac", [1.0, 1.0]),
                        ("chunksRelDepth", [1.0, 1.0]),
                        ("chunksRelDepthStd", [0.0, 0.0]),
                        ("reads", [114, 114]),
                        ("ureads", [114, 114]),
                        ("hicureads", [25, 25]),
                        ("refsize", [13897, 13897]),
                        ("refname", ["test_1", "test_2"]),
                        ("taxid", [2697049, 2697049]),
                        ("rank", ["species", "species"]),
                        ("taxname", ["SARS-CoV-2", "SARS-CoV-2"]),
                        ("taxpath", ["taxdump", "taxdump"]),
                        ("taxpathsn", ["taxdump", "taxdump"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError, message="check_compositionality"
            ),
        ),

    ],
)
def test_percent(profile: pd.DataFrame):
    """Test that the percent column (percent_cumulative) is checked."""
    KmcpProfile.validate(profile)


@pytest.mark.parametrize(
    "profile",
    [
        pd.DataFrame(
            OrderedDict(
                [
                    ("ref", ["test_1"]),
                    ("percentage", [100.0]),
                    ("coverage", [1.23]),
                    ("score", [83.97]),
                    ("chunksFrac", [1.0]),
                    ("chunksRelDepth", [1.0]),
                    ("chunksRelDepthStd", [0.0]),
                    ("reads", [114]),
                    ("ureads", [114]),
                    ("hicureads", [25]),
                    ("refsize", [13897]),
                    ("refname", ["test_1"]),
                    ("taxid", [2697049]),
                    ("rank", ["species"]),
                    ("taxname", ["SARS-CoV-2"]),
                    ("taxpath", ["taxdump"]),
                    ("taxpathsn", ["taxdump"]),
                ]
            )
        ),
        pytest.param(
            pd.DataFrame(
                OrderedDict(
                    [
                        ("ref", ["test_1", "test_2"]),
                        ("percentage", [100.0, "zero"]),
                        ("coverage", [1.23, 1.23]),
                        ("score", [83.97, 83.97]),
                        ("chunksFrac", [1.0, 1.0]),
                        ("chunksRelDepth", [1.0, 1.0]),
                        ("chunksRelDepthStd", [0.0, 0.0]),
                        ("reads", [114, 114]),
                        ("ureads", [114, 114]),
                        ("hicureads", [25, 25]),
                        ("refsize", [13897, 13897]),
                        ("refname", ["test_1", "test_2"]),
                        ("taxid", [2697049, 2697049]),
                        ("rank", ["species", "species"]),
                        ("taxname", ["SARS-CoV-2", "SARS-CoV-2"]),
                        ("taxpath", ["taxdump", "taxdump"]),
                        ("taxpathsn", ["taxdump", "taxdump"]),
                    ]
                )
            ),
            marks=pytest.mark.raises(
                exception=SchemaError,
                message="expected series 'percentage' to have type int",
            ),
        ),
    ],
)
