# Supporting New Taxonomic Profilers

A good way to contribute to the taxpasta project is to add support for a new
taxonomic profiler. This mostly boils down to creating three new Python files
(modules) and filling them with life, as well as testing them appropriately.

The taxpasta package is designed to follow a [hexagonal
architectural](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
style. That means, the directory structure may be somewhat unfamiliar to you.
This architectural style is reflected by the Python package organization which has three
sub-packages: [`taxpasta.domain`][taxpasta.domain], [`taxpasta.application`][taxpasta.application], and [`taxpasta.infrastructure`][taxpasta.infrastructure].
Fortunately, you don't really need to care about that (unless you want to :wink:), as long
as you follow this guide. For supporting a new taxonomic profiler, three new Python
modules need to be placed in a package of their own named for the profiler, for example,
`src/taxpasta/infrastructure/application/kraken2/` and their tests mostly in
`tests/unit/infrastructure/application/kraken2/`.

What do those three new modules need to do? Basically, taxpasta needs to be able
to read a taxonomic profile, validate its correctness as much as possible, and
finally transform it to what we call the
[`StandardProfile`][taxpasta.domain.model.StandardProfile]. All
further processing and logic is based on the [`StandardProfile`][taxpasta.domain.model.StandardProfile] so you don't need
to change anything else!

```mermaid
graph LR
  A[Taxonomic Profile] -->|read| B[pandas.DataFrame];
  B -->|validate| C{ };
  C -->|transform| D[StandardProfile];
  C --> E[pandera.errors.SchemaErrors];
```

## Development Process

We recommend that you start by thinking about how the taxonomic profile from the file,
that means, the output of the tool that you want to support, should be represented within
Python. According to the above diagram, you will start in the middle at the validation step.

If you're feeling very professional, you can also first create your test cases. This is a
principle called [test-driven development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development) which is a great way to check your assumptions
about your code, helps you spot mistakes in your code early, and generally helps designing
your code to be more testable (although we arguably already did that for you).

### 1. Schema Model

We are assuming that all profile data is tabular and therefore
[pandas](https://pandas.pydata.org/) is our choice for handling this data.
Should this assumption somehow not hold, please contact us on [Slack](https://nfcore.slack.com/archives/C031QH57DSS) or create a
[GitHub Discussion](https://github.com/taxprofiler/taxpasta/discussions/new) topic.
In order to perform validation of tabular data, we use [pandera schema
models](https://pandera.readthedocs.io/en/stable/schema_models.html). Therefore, 
please place a
new Python module into `src/taxpasta/infrastructure/application/<profiler name>` that will contain the
schema model expressing the shape and form of your data. The name of the class that you
create should follow Python conventions (be in [Pascal case](https://en.wikipedia.org/wiki/Camel_case)) and should be composed of
the tool name, for example, `Kraken2Profile` for the kraken2 tool. Your new module (Python file)
should be named like your class, except be all lower case and with underscores `_`
separating words, e.g., `kraken2_profile.py` ([snake case](https://en.wikipedia.org/wiki/Snake_case)).

When creating your schema model, you need to think about what columns should be there,
what data types they represent, and what kind of constraints should be placed on them
for validation. Below follows an example for kraken2. Please read up on [pandera schema
models](https://pandera.readthedocs.io/en/stable/schema_models.html) to understand
all the details. Briefly: we expect particularly named columns, in the order defined
in the class, with specific data types, and we expect the numeric data types to be
within certain intervals.

```python title="src/taxpasta/infrastructure/application/kraken2/kraken2_profile.py"
from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Series


class Kraken2Profile(pa.SchemaModel):
    """Define the expected kraken2 profile format."""

    percent: Series[float] = pa.Field(ge=0.0, le=100.0)
    clade_assigned_reads: Series[int] = pa.Field(ge=0)
    direct_assigned_reads: Series[int] = pa.Field(ge=0)
    num_minimizers: Optional[Series[int]] = pa.Field(ge=0)
    distinct_minimizers: Optional[Series[int]] = pa.Field(ge=0)
    taxonomy_lvl: Series[pd.CategoricalDtype] = pa.Field()
    taxonomy_id: Series[pd.CategoricalDtype] = pa.Field()
    name: Series[str] = pa.Field()

    class Config:
        """Configure the schema model."""

        coerce = True
        ordered = True
        strict = True
```

In order to test this schema, you need to place a test module in the equivalent directory 
`tests/unit/infrastructure/application/<profiler name>/`. The name of the file should be the same as your module above
but prefixed with `test_`, for example, `test_kraken2_profile.py`. In there, you need to import
your code module and perform a number of tests on it. In general, pandera is a well tested Python
package itself so we can assume that it works as advertised. These tests are there to confirm
that the data structure that you have in mind for the profile and your schema model match up. Also,
in case you need to modify the schema, these tests will ensure that your previous assumptions
still hold. You can look at existing test cases for inspiration.

### 2. Reader

You could then continue either with the reading or transformation part of the schema presented above.
We will begin with the reader so that you can get some real data into Python.

For reading a taxonomic profile from a new tool, you need to inherit a new class
from the abstract [`ProfileReader`][taxpasta.application.service.ProfileReader]. This
new class and module should follow the naming scheme mentioned above,
as an example `Kraken2ProfileReader` to support `kraken2` in `kraken2_profile_reader.py`.  Since you need to import
your base class from a different package branch, you should use an absolute
import.

```python title="src/taxpasta/infrastructure/application/kraken2/kraken2_profile_reader.py"
from taxpasta.application import ProfileReader


class Kraken2ProfileReader(ProfileReader):
```

What exactly the reader needs to do is very tool dependent. You probably want to use one
of the many `pandas.read_*` functions with specific arguments tailored to reading your
particular file format. Whatever you do, you need to ensure that the output returned by
calling the `read` class method follows the schema that you have defined before. Again,
you can look at existing code for inspiration.

Don't forget to test that your reader creates expected output by adding a few test cases
into a module that you place in `tests/unit/infrastructure/application/<profiler name>/`. To test your
reader you probably want to add some appropriate files into `tests/data/<profiler name>`, too, and
make them accessible with a pytest fixture function which you place into `tests/conftest.py`.
Take a look at the kraken2 fixture:

```python title="tests/conftest.py"
@pytest.fixture(scope="module")
def kraken2_data_dir(data_dir: Path) -> Path:
    """Provide the path to the kraken2 data directory."""
    return data_dir / "kraken2"
```

### 3. Validation & Transformation

 The
validation is automatically performed by decorating with [`pandera.check_types`](https://pandera.readthedocs.io/en/stable/schema_models.html) and annotating the
`transform` class method of the standardisation service, for example,

```python title="src/taxpasta/infrastructure/application/kraken2/kraken2_profile_standardisation_service.py"
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application import ProfileStandardisationService
from taxpasta.domain import StandardProfile

from .kraken2_profile import Kraken2Profile


class Kraken2ProfileStandardisationService(ProfileStandardisationService):
    @classmethod
    @pa.check_types(lazy=True)  # (1)
    def transform(
        cls, profile: DataFrame[Kraken2Profile]
    ) -> DataFrame[StandardProfile]:
```

1. The argument `lazy=True` ensures that all schema errors are reported and not just the
    first one.

Finally, we need to transform the specific taxonomic profile into our standard
profile. Similarly to the profile reader, there exists an abstract
[`ProfileStandardisationService`][taxpasta.application.service.ProfileStandardisationService]
that you need to inherit from. The new module should be placed into
`src/taxpasta/infrastructure/application/<profiler name>/` and the naming should follow the
conventions, as an example, `Kraken2ProfileStandardisationService` class in a
`kraken2_profile_standardisation_service.py` module.

```python title="src/taxpasta/infrastructure/application/kraken2/kraken2_profile_standardisation_service.py"
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application import ProfileStandardisationService
from taxpasta.domain import StandardProfile

from .kraken2_profile import Kraken2Profile


class Kraken2ProfileStandardisationService(ProfileStandardisationService):
    @classmethod
    @pa.check_types(lazy=True)
    def transform(
        cls, profile: DataFrame[Kraken2Profile]
    ) -> DataFrame[StandardProfile]:
```

The `pa.check_types` decorator validates the class method's input and output
using the type annotations and the defined schema models.

The `transform` class method itself needs to modify the given `pandas.DataFrame` such that
the returned result looks like the [`StandardProfile`][taxpasta.domain.model.StandardProfile].

In order to ensure that the whole three-step process from the diagram: read, validate, transform
produces expected results, we will now create a new kind of test; an integration test that
uses all the classes that we have created. Thus, we need a new test module in `tests/integration/`,
you can name it `test_<tool>_etl.py`, e.g., `test_kraken2_etl.py`.

This test has few lines of code but thanks to the `pa.check_types` decorator performs
all the work that we need. Again, for kraken2 this looks like:

```python title="tests/integration/test_kraken2_etl.py"
from pathlib import Path

from taxpasta.infrastructure.application import (
    Kraken2ProfileReader,
    Kraken2ProfileStandardisationService,
)


def test_kraken2_etl(
    kraken2_data_dir: Path,
    filename: str,
):
    """Test that kraken2 profiles are read, validated, and transformed correctly."""
    Kraken2ProfileStandardisationService.transform(
        Kraken2ProfileReader.read(kraken2_data_dir / filename)
    )
```

It is a good idea to include some known invalid files such that you can be sure that
your schema catches input errors.

### 4. Imports

To be able to import your classes from `taxpasta.infrastructure.application` as shown in the test above,
you need to create the right imports. First, import the classes in your profiler-specific package.
For kraken2, this looks like:


```python title="src/taxpasta/infrastructure/application/kraken2/__init__.py"
from .kraken2_profile import Kraken2Profile
from .kraken2_profile_reader import Kraken2ProfileReader
from .kraken2_profile_standardisation_service import (
    Kraken2ProfileStandardisationService,
)
```

Then, import the classes again in the main application package.

```python title="src/taxpasta/infrastructure/application/__init__.py"
from .kraken2 import (
    Kraken2Profile,
    Kraken2ProfileReader,
    Kraken2ProfileStandardisationService,
)
```

### 5. Enable Support

Finally, to make your profiler fully available to taxpasta, you have to add your profiler name
to the [`SupportedProfiler`][taxpasta.infrastructure.application.SupportedProfiler] enumeration.

```python title="src/taxpasta/infrastructure/application/supported_profiler.py" hl_lines="9"
from enum import Enum, unique


@unique
class SupportedProfiler(str, Enum):
    """Define supported taxonomic profilers."""

    kraken2 = "kraken2"
    <profiler name> = "<profiler name>"
```

Once that entry is made. Add your reader and standardisation service to the
[`ApplicationServiceRegistry`][taxpasta.infrastructure.application.ApplicationServiceRegistry].
First, add a condition to the `profile_reader` class method as shown here for kraken2.

```python title="src/taxpasta/infrastructure/application/application_service_registry.py" hl_lines="11-14"
class ApplicationServiceRegistry:
    """Define an application service registry."""

    @classmethod
    def profile_reader(cls, profiler: SupportedProfiler) -> Type[ProfileReader]:
        """Return a profile reader of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileReader

            return BrackenProfileReader
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileReader

            return Kraken2ProfileReader
        else:
            raise ValueError("Unexpected")
```

Second, add a condition to the `profile_standardisation_service` class method in a similar manner.

```python title="src/taxpasta/infrastructure/application/application_service_registry.py" hl_lines="12-15"
class ApplicationServiceRegistry:
    """Define an application service registry."""

    def profile_standardisation_service(
        cls, profiler: SupportedProfiler
    ) -> Type[ProfileStandardisationService]:
        """Return a profile standardisation service of the correct type."""
        if profiler is SupportedProfiler.bracken:
            from .bracken import BrackenProfileStandardisationService

            return BrackenProfileStandardisationService
        elif profiler is SupportedProfiler.kraken2:
            from .kraken2 import Kraken2ProfileStandardisationService

            return Kraken2ProfileStandardisationService
        else:
            raise ValueError("Unexpected")
```

Congratulations! :tada: You are now ready to use your added profiler in the taxpasta commands.

## Overview

Overall, taking kraken2 as an example once more, your classes should have the same relationships as shown in the diagram below (open the image in a new tab for a better view).

![](taxpasta_profiler_support_overview.svg)
