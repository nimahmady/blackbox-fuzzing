import time
from subprocess import CompletedProcess


class Logger:
    """Logs and persists output information of an executable."""

    def __init__(self) -> None:
        self._log: list[str] = list()

    def append(self, parameter_count: int, process: CompletedProcess) -> None:
        """Creates a new log entry from the given process data and appends it to the internal log list.

        :param parameter_count: The number of the passed parameter.
        :param process: The process that ran the executable.
        """

        log_entry: str = (f"{parameter_count}. "
                          f"Input: {process.args[1]}, "
                          f"Exit code: {process.returncode}, "
                          f"Output: {process.stdout.strip()}")
        self._log.append(log_entry)

    def to_file(self, parameter_generator_type: str, elapsed_time: float) -> None:
        """Writes the entries of the internal log list to a LOG file line by line."""

        timestamp_for_filename = time.strftime("%Y%m%d-%H%M%S")
        with open(f"logs/{timestamp_for_filename}-{parameter_generator_type}-gOATcat.log", "w") as log_file:
            log_file.write(f"Elapsed time (in seconds): {round(elapsed_time, 6)}\n\n")
            log_file.write("Raw data:\n")
            log_file.write("\n".join(self._log))

    def reset(self) -> None:
        """Clears the internal log list for a subsequent test run."""

        self._log.clear()
