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


"""Provide a sample merging service that summarizes two or more samples."""


from typing import Iterable

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from ..model import Sample, StandardProfile, TidyObservationTable, WideObservationTable


class SampleMergingService:
    """Define a sample merging service that summarizes one or more samples."""

    @classmethod
    @pa.check_types(lazy=True)
    def merge_wide(cls, samples: Iterable[Sample]) -> DataFrame[WideObservationTable]:
        """
        Merge two or more sample profiles into a wide-format observation matrix.

        Args:
            samples: Two or more samples.

        Returns:
            A single table containing one row per taxon, one column for the taxonomy
            identifier, and one column per sample with abundance counts.

        """
        # `set_index` creates a copy of the original profile which is convenient so that
        # we do not modify existing profiles but, of course, doubles the memory used.
        counts = [
            sample.profile.set_index(
                keys=StandardProfile.taxonomy_id, verify_integrity=True
            ).rename(columns={StandardProfile.count: sample.name})
            for sample in samples
        ]
        # Please note that `set_index` restores the underlying dtype of the categorical
        # column `taxonomy_id`. Thus, when we `reset_index` the column is of dtype
        # object but, due to schema coercion, this is automatically converted into a
        # categorical dtype again when pandera checks the return type.
        return (
            counts[0]
            .join(counts[1:], how="outer")
            .fillna(0)
            # We explicitly convert to int64 because of a Windows type problem.
            # See https://github.com/unionai-oss/pandera/issues/726
            .astype(np.int64)
            .reset_index()
        )

    @classmethod
    @pa.check_types(lazy=True)
    def merge_long(cls, samples: Iterable[Sample]) -> DataFrame[TidyObservationTable]:
        """
        Merge two or more sample profiles into a tidy observation table.

        Args:
            samples: Two or more samples.

        Returns:
            A single table containing three columns: taxonomy identifier, abundance
            count, and sample identifier.

        """
        # `assign` creates a copy of the original profile which is convenient so that
        # we do not modify existing profiles but, of course, doubles the memory used.
        # Please note that `concat` restores the underlying dtype of the categorical
        # column `taxonomy_id`. Thus, the column is of dtype
        # object but, due to schema coercion, this is automatically converted into a
        # categorical dtype again when pandera checks the return type. The same holds
        # for the `sample` column.
        result = pd.concat(
            [sample.profile.assign(sample=sample.name) for sample in samples],
            ignore_index=True,
            copy=False,
        )
        # We explicitly convert to int64 because of a Windows type problem.
        # See https://github.com/unionai-oss/pandera/issues/726
        result[TidyObservationTable.count] = result[TidyObservationTable.count].astype(
            np.int64
        )
        return result
