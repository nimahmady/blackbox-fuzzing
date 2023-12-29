from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from logger import Logger
from runner import Runner
from parameter_generator import ParameterGenerator

ParameterGeneratorType: TypeVar = TypeVar(name='ParameterGeneratorType', bound=ParameterGenerator)


class TestEnvironment(ABC):
    """An abstract base class for test environments (for specific executables) to specialize."""

    def __init__(self, path_to_executable: str) -> None:
        self._path_to_executable = path_to_executable
        self._logger = Logger()
        self._runner = Runner(self._get_logger)

    @property
    @abstractmethod
    def _get_path_to_executable(self) -> str:
        """Gets the path to the executable that is to be tested.

        :return: The path to the executable to be tested.
        """

        return self._path_to_executable

    @property
    @abstractmethod
    def _get_logger(self) -> Logger:
        """Gets the logger that is responsible for logging and persisting test results.

        :return: The logger responsible for logging and persisting test results.
        """

        return self._logger

    @property
    @abstractmethod
    def _get_runner(self) -> Runner:
        """Gets the runner that is responsible for running the executable with parameters.

        :return: The runner responsible for running the executable with parameters.
        """

        return self._runner

    @property
    @abstractmethod
    def _get_target(self) -> str:
        """Gets the target string that is searched for in the solution.

        :return: The target string searched for in the solution.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def _get_non_target(self) -> str:
        """Gets the non-target string that must not be contained in the solution.

        :return: The non-target string that must not be in the solution.
        """

        raise NotImplementedError

    @abstractmethod
    def perform_test_run(self, parameter_generator: ParameterGeneratorType, test_count: Optional[int]) -> None:
        """Initiates a timed test run with the given parameter generator and initiates post-run logger handling.

        :param parameter_generator: The parameter generator to generate parameters for the test.
        :param test_count: The number of tests to carry out in the test run.
        """

        raise NotImplementedError

    @abstractmethod
    def _run(self, parameter_generator: ParameterGeneratorType, test_count: Optional[int]) -> float:
        """Performs a timed test of the executable with the given parameter generator.

        :param parameter_generator: The parameter generator to generate parameters for the test.
        :param test_count: The number of tests to carry out in the test run.
        :return: The elapsed time (in seconds) taken to test the executable.
        """

        raise NotImplementedError

    @abstractmethod
    def _test_run_completed(self, output: str) -> bool:
        """Checks if the current test run has completed based on the given output of the executable.

        :param output: The output of the executable.
        :return: A boolean that states if the current test run has completed.
        """

        raise NotImplementedError

    @abstractmethod
    def _handle_logs(self, parameter_generator_type: str, elapsed_time: float) -> None:
        """Prompts logger to write logs to file and reset."""

        raise NotImplementedError
