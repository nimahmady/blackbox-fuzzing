"""Test environment for parameter-based testing of gOATcat.

This script initializes and orchestrates the components required for testing an executable with different test
approaches. The test approaches provided by default are brute force and grammar fuzzing.

    * main: the main function of the script

- Authors: Nima Ahmady-Moghaddam, Eric Eichholtz, Peer Maute, Daniel Osterholz (Team 01)
- Course: Testen von Sicherheit und Zuverlaessigkeit (TES)
- Supervisor: Prof. Dr. Bettina Buth (University of Applied Sciences Hamburg)
- Semester: Winter semester 2023
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from parameter_generator import ParameterGenerator
# noinspection PyUnresolvedReferences
from brute_forcer import BruteForcer  # Import is needed for dynamic instantiation (see verify_arguments())
# noinspection PyUnresolvedReferences
from grammar_fuzzer import GrammarFuzzer  # Import is needed for dynamic instantiation (see verify_arguments())
from test_environment import TestEnvironment
# noinspection PyUnresolvedReferences
from test_environment_goatcat import TestEnvironmentGoatcat  # Import is needed for dynamic instantiation


def parse_arguments() -> Namespace:
    """Defines and parses arguments passed to the application.

    :return: a namespace object containing the parsed arguments.
    """

    argument_parser: ArgumentParser = ArgumentParser(
        description="An application for blackbox-fuzzing executable programs.")

    argument_parser.add_argument("-pe", "--path_to_executable", type=str, required=True,
                                 dest="pe", help="The absolute or relative path to the executable to be tested")
    argument_parser.add_argument("-pg", "--parameter_generator", type=str, required=True,
                                 choices=[subclass.__name__ for subclass in ParameterGenerator.__subclasses__()],
                                 dest="pg", help="The class name of the parameter generator to be used in the test run")
    argument_parser.add_argument("-te", "--test_environment", type=str, required=True, dest="te",
                                 choices=[subclass.__name__ for subclass in TestEnvironment.__subclasses__()],
                                 help="The class name of the test environment to perform the test run")
    argument_parser.add_argument("-tc", "--test_count", type=int, required=False, dest="tc",
                                 help="(Optional) The number of tests to carry out in the test run (can be used to "
                                      "produce short test runs for debugging purposes)")

    return argument_parser.parse_args()


def verify_arguments(arguments: Namespace) -> tuple[ParameterGenerator, TestEnvironment]:
    """Verifies arguments passed to the application and instantiates requested parameter generator and test environment.

    :return: An instance of the parameter generator and an instance of the test environment to be used in the test run.
    :raise FileNotFoundError: Raised if no executable file with the given name exists at the given path.
    :raise ValueError: Raised if an invalid parameter generator name or test environment name was passed.
    """

    pg: str = arguments.pg  # This argument represents the name of the requested parameter generator
    pe: str = arguments.pe  # This argument represents the path to the requested executable
    te: str = arguments.te  # This argument represents the name of the requested test environment

    if not Path(pe).is_file():
        raise FileNotFoundError(f"File not found at path: {pe}")

    # Iterate over immediate subclasses of ParameterGenerator and create instance of class whose name matches given name
    for subclass in ParameterGenerator.__subclasses__():
        if subclass.__name__ == pg:
            parameter_generator: ParameterGenerator = subclass()
            break
    else:  # Unreachable because ArgumentParser checks validity of passed parameter generator name with choices-flag
        raise ValueError(f"An invalid parameter generator name was passed: {pg}")

    # Iterate over immediate subclasses of TestEnvironment and create instance of class whose name matches given name
    for subclass in TestEnvironment.__subclasses__():
        if subclass.__name__ == te:
            test_environment: TestEnvironment = subclass(pe)
            break
    else:  # Unreachable because ArgumentParser checks validity of passed test environment name with choices-flag
        raise ValueError(f"An invalid test environment name was passed: {te}")

    return parameter_generator, test_environment


def main() -> None:
    """Prompts parsing and verification of arguments, and initiates a test run with a requested test environment and
    parameter generator."""

    arguments: Namespace = parse_arguments()
    parameter_generator, test_environment = verify_arguments(arguments)
    test_environment.perform_test_run(parameter_generator, arguments.tc)


if __name__ == '__main__':
    main()
