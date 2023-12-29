import datetime
from typing import Optional, TypeVar

from logger import Logger
from parameter_generator import ParameterGenerator
from runner import Runner
from test_environment import TestEnvironment
from timer import Timer

ParameterGeneratorType: TypeVar = TypeVar(name='ParameterGeneratorType', bound=ParameterGenerator)


class TestEnvironmentGoatcat(TestEnvironment):
    """A test environment that carries out test runs of the gOATcat executable and orchestrates output logging."""

    def __init__(self, path_to_executable: str) -> None:
        """Initializes the gOATcat test environment with members that correspond to the parameter rules of gOATcat.

        :raise FileNotFoundError: Raised if no executable file with the given name exists at the given path.
        """

        super().__init__(path_to_executable)
        self._path_to_executable: str = path_to_executable
        self._logger: Logger = Logger()
        self._runner: Runner = Runner(self._get_logger())
        self._target: str = "FLAG"
        self._non_target: str = "unix style"  # Necessary to prevent stopping the search at argument "-h"

    def _get_path_to_executable(self) -> str:
        """Gets the path to the executable that is to be tested.

        :return: The path to the executable to be tested.
        """

        return self._path_to_executable

    def _get_logger(self) -> Logger:
        """Gets the logger that is responsible for logging and persisting test results.

        :return: The logger responsible for logging and persisting test results.
        """

        return self._logger

    def _get_runner(self) -> Runner:
        """Gets the runner that is responsible for running the executable with parameters.

        :return: The runner responsible for running the executable with parameters.
        """

        return self._runner

    def _get_target(self) -> str:
        """Gets the target string that is searched for in the solution.

        :return: The target string searched for in the solution.
        """

        return self._target

    def _get_non_target(self) -> str:
        """Gets the non-target string that must not be contained in the solution.

        :return: The non-target string that must not be in the solution.
        """

        return self._non_target

    def perform_test_run(self, parameter_generator: ParameterGeneratorType, test_count: Optional[int]) -> None:
        """Initiates a timed test run with the given parameter generator and initiates post-run logger handling.

        :param parameter_generator: The parameter generator to generate parameters for the test.
        :param test_count: The number of tests to carry out in the test run.
        """

        elapsed_time: float = self._run(parameter_generator, test_count)
        parameter_generator_class_name: str = parameter_generator.__class__.__name__
        self._handle_logs(parameter_generator_class_name, elapsed_time)

    def _run(self, parameter_generator: ParameterGeneratorType, test_count: Optional[int]) -> float:
        """Performs a timed test of the gOATcat executable with the given parameter generator.

        :param parameter_generator: The parameter generator to generate parameters for the test.
        :param test_count: The number of tests to carry out in the test run.
        :return: The elapsed time (in seconds) taken to test gOATcat.
        """

        print(f"Test environment: {self.__class__.__name__}\n"
              f"Parameter generator: {parameter_generator.__class__.__name__}\n"
              f"Path to executable: {self._get_path_to_executable()}\n"
              f"Test run started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        timer_name: str = f"{parameter_generator.__class__.__name__}Timer"

        with Timer(name=timer_name) as timer:
            for parameter_count, parameter in parameter_generator.next_parameter():
                output: str = self._get_runner().run_executable(parameter_count, self._get_path_to_executable(),
                                                                [parameter])
                if parameter_count % 10000 == 0:
                    print(f"Parameter {parameter_count}: {parameter}")
                if self._test_run_completed(output) or (test_count and parameter_count == test_count):
                    break

        return timer.timers[timer_name]

    def _test_run_completed(self, output: str) -> bool:
        """Checks if the test run has completed based on the given gOATcat output.

        :param output: The gOATcat output.
        :return: A boolean that states if the current test run has completed.
        """

        return self._get_target() in output and self._get_non_target() not in output

    def _handle_logs(self, parameter_generator_type: str, elapsed_time: float) -> None:
        """Prompts logger to write logs to file and reset."""

        logger: Logger = self._get_logger()
        logger.to_file(parameter_generator_type, elapsed_time)
        logger.reset()
