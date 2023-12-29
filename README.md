# Black-box Fuzzing an Executable

This project contains an application that performs black-box fuzzing of an executable. The following fully automated functionality is provided:

1. A brute-force approach and a grammar-fuzzing approach to generating string parameters
2. Testing or fuzzing an executable by executing it with generated parameters as arguments
3. Logging of execution results and persisting of log data
4. Measurment of test duration

The executable `gOATcat` serves as the default test object. Its binary files for Linux, MacOS, and Windows are located in the directory `build/`.

## Project Information

- **Authors:** Nima Ahmady-Moghaddam, Eric Eichholtz, Peer Maute, Daniel Osterholz (Team 01)
- **Course:** Testen von Sicherheit und Zuverlaessigkeit (TES)
- **Supervisor:** Prof. Dr. Bettina Buth (University of Applied Sciences Hamburg)
- **Semester:** Winter semester 2023

## Using the Project

This section outlines the setup and execution of the application and the types of results produced during test runs.

### Project requirements

- Python v3.10 or greater

### Project setup

To set up the project in an IDE, follow these steps:

1. Open the root directory of the project in an IDE.
2. Select or configure a Python interpreter for the project that meets the requirements listed in [Project Requirements](#project-requirements).

A file `requirements.txt` is not included because all application dependencies are either internal (i.e., local files) or part of the Python Standard Library.

### Starting a test run

To start a test run from the terminal, do either of the following:

- In a terminal opened in the root directory of the project, run the following command (the `|` stands for "xor"):
  - MacOS/Linux: `python3 main.py -pe path/to/executable -pg BruteForcer|GrammarFuzzer -te TestEnvironmentGoatcat`
  - Windows: `python main.py -pe path/to/executable -pg BruteForcer|GrammarFuzzer -te TestEnvironmentGoatcat`
- In an IDE with the project opened, set up a configuration that takes a valid value for each of the parameters `-pe`, `-pg`, and `-te`.

The following parameters can be used to configure test runs:

- `-pe` (required): The absolute or relative path to the executable to be tested
- `-pg` (required): The class name of the parameter generator to be used in the test run
- `-te` (required): The class name of the test environment to be used in the test run
- `-tc` (optional): The number of tests to carry out in the test run (can be used to produce short test runs for debugging purposes).
- (`-h`: Displays the help test of the application)

> **Note:** The application enables the implementation and use of additional parameter generators and test environments. See [Developing the Project](#developing-the-project) for more details.

### Viewing test outputs

The application automatically logs the duration of and raw data produced during each test run. Raw data include input parameters, exit codes, and outputs of the executable. Log files are generated *after* each test run and are stored in the directory `logs/`. (Two example log files that were produced during a test run with the `GrammarFuzzer` are provided in this project.)

## Developing the Project

This section provides an overview of the structure of the project and suggestions on how the project might be developed further.

### Project Overview

A class diagram of the application with selected members of each class is shown below. Per default, the multiplicity of each class is 1 and is therefore omitted from the diagram.

![Simplified class diagram of the project](./img/class_diag.png)

- `TestEnvironment`: An abstract base class for test environments to specialize.
- `TestEnvironmentGoatcat`: Initializes and orchestrates the components required for testing the `gOATcat` executable and logging test results.
- `ParameterGenerator`: An abstract base class for parameter generators to specialize.
- `BruteForcer`: A parameter generator that systematically generates increasingly long strings with printable ASCII characters (`0, 1, 2, ..., 00, 01, 02, ...`). This approach makes no assumptions about the input requirements of `gOATcat`, other than that it accepts printable ASCII characters. (For a list of printable ASCII characters, see [this](https://en.wikipedia.org/wiki/ASCII#cite_note-60) Wikipedia note.)
- `GrammarFuzzer`: A parameter generator that randomly generates parameters that syntactically satisfy the rules of `gOATcat`. (Run `goatcat -h` in a terminal to see the rules of `gOATcat`.)
- `Runner`: Runs a given executable with a given list of parameters as arguments.
- `Logger`: Logs and persists output information of the `gOATcat` executable.
- `Timer`: Measures and reports execution time of test runs.

### Writing a new test environment

The application includes a default test environment `TestEnvironmentGoatcat` designed to test the `gOATcat` executable (see [Project Overview](#project-overview)). To write a new test environment, follow these steps:

1. In a new file (say `my_new_file`), define a new class (say `MyNewClass`) that inherits from `TestEnvironment`.
2. In `MyNewClass`, implements the required members of `TestEnvironment`. For reference, see the implementation of `TestEnvironmentGoatcat`.
3. In the file `main.py`, add an import statement for the new class:

```python
# noinspection PyUnresolvedReferences
from my_new_file import MyNewClass
```

> **Note:** The comment-style annotation `# noinspection PyUnresolvedReferences` is added to prevent the IDE PyCharm from marking the import as unused. The import is not used explicitly in `main.py`; but it is necessary to bring `MyNewClass` into the file scope and enable dynamic instantiation based on the arguments passed to the application at runtime. (See the method `verify_arguments()` in `main.py` for more details.)

### Writing a new parameter generator

The application includes two default parameter generators `BruteForcer` and `GrammarFuzzer` designed to test the `gOATcat` executable (see [Project Overview](#project-overview)). To write a new parameter generator, follow these steps:

1. In a new file (say `my_new_file`), define a new class (say `MyNewClass`) that inherits from `ParameterGenerator`.
2. In `MyNewClass`, implement the required members of `ParameterGenerator`. For reference, see the implementation of `BruteForcer` or `GrammarFuzzer`.

    > **Note:** It is recommended that the method `_next_parameter()` return a generator object (using the Python keyword `yield` instead of `return`) to enable the theoretical generation of infinitely many parameters.

3. In the file `main.py`, add an import statement for the new class:

```python
# noinspection PyUnresolvedReferences
from my_new_file import MyNewClass
```

> **Note:** See the note in [Writing a new test environment](#writing-a-new-test-environment) for more information on the comment-style annotation `# noinspection PyUnresolvedReferences`.

### Adding a new test object

The default test object included in the project is the `gOATcat` executable. To add a new test object to the project for the application to run tests on, follow these steps:

1. Add an executable to the project, preferably under the directory `build/`.
2. When starting a test run, pass the path to the executable to the parameter `-pe`. See [Starting a test run](#starting-a-test-run) for more details on test run parameterization.
