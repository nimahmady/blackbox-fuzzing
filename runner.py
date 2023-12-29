import subprocess
from subprocess import CompletedProcess

from logger import Logger


class Runner:
    """Parameterizes and runs an executable."""

    def __init__(self, logger: Logger) -> None:
        self._logger: Logger = logger

    def run_executable(self, parameter_count: int, path_to_executable: str, arguments: list[str]) -> str:
        """Runs an executable file with provided arguments.

        :param parameter_count: The number of the passed parameter.
        :param path_to_executable: The relative path to the executable to be tested.
        :param arguments: A list of strings to be passed to the executable as positioned arguments in the given order.
        Example: [arg1, arg2]
        :return: The return value of the executable written to standard output (stdout).
        """

        process: CompletedProcess = subprocess.run([path_to_executable] + arguments, capture_output=True, text=True)
        self._logger.append(parameter_count, process)
        return process.stdout
