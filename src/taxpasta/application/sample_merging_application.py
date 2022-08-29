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


"""Provide a sample merging application that summarizes two or more samples."""


from typing import Iterable, Tuple

import pandas as pd
from pandera.typing import DataFrame

from taxpasta.domain import StandardProfile


class SampleMergingApplication:
    """Define a sample merging application that summarizes one or more samples."""

    @classmethod
    def merge_wide(
        cls, samples: Iterable[Tuple[str, DataFrame[StandardProfile]]]
    ) -> DataFrame:
        """
        Merge two or more sample profiles into a wide-format table.

        Args:
            samples: Pairs of sample name and standard profile.

        Returns:
            A single table containing one row per taxon, one column for the taxonomy
            identifier, and one column per sample with abundance counts.

        """
        # `set_index` creates a copy of the original profile which is convenient so that
        # we do not modify existing profiles but, of course, doubles the memory used.
        counts = [
            profile.set_index(
                keys=StandardProfile.taxonomy_id, verify_integrity=True
            ).rename(columns={StandardProfile.count: name})
            for name, profile in samples
        ]
        return (
            counts[0].join(counts[1:], how="outer").fillna(0).astype(int).reset_index()
        )

    @classmethod
    def merge_long(
        cls, samples: Iterable[Tuple[str, DataFrame[StandardProfile]]]
    ) -> DataFrame:
        """
        Merge two or more sample profiles into a summary table.

        Args:
            samples: Pairs of sample name and standard profile.

        Returns:
            A single table containing three columns: taxonomy identifier, abundance
            count, and sample identifier.

        """
        # `assign` creates a copy of the original profile which is convenient so that
        # we do not modify existing profiles but, of course, doubles the memory used.
        return pd.concat(
            [profile.assign(sample=name) for name, profile in samples],
            ignore_index=True,
        )
