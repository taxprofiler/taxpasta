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


"""Provide general decorators."""


import warnings
from functools import wraps
from typing import Any, Callable

from pandas.errors import ParserWarning


def raise_parser_warnings(func: Callable) -> Callable:
    """Decorate a function in order to raise parser warnings as value errors."""

    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        with warnings.catch_warnings():
            warnings.filterwarnings(action="error", category=ParserWarning)
            try:
                result = func(*args, **kwargs)
            except ParserWarning as exc:
                raise ValueError(
                    "There were unexpected issues with the data. Please double-check "
                    "the specific combination of your chosen metagenomic profiler and "
                    "input profile."
                ) from exc
        return result

    return wrapped
