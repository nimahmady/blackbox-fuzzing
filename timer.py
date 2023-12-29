import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Dict, Optional, Any


class TimerError(Exception):
    """A custom exception used to report errors in Timer class."""


@dataclass
class Timer(ContextDecorator):
    """Reports execution time of code. Can be used as a class, context manager, or decorator.

    Source: https://realpython.com/python-timer/#the-python-timer-code
    """

    timers: ClassVar[Dict[str, float]] = dict()
    name: Optional[str] = None
    text: str = "Elapsed time: {:0.6f} seconds"
    logger: Optional[Callable[[str], None]] = print
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialization: adds Timer (if named) to dictionary of timers."""

        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self) -> None:
        """Starts a new timer."""

        if self._start_time is not None:
            raise TimerError(f"Timer is already running. Use {self.stop.__name__} to stop it.")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stops the timer and report the elapsed time.

        :return: The elapsed time in seconds.
        """

        if self._start_time is None:
            raise TimerError(f"Timer is not yet running. Use {self.start.__name__} to start it.")

        # Calculate elapsed time and clear start time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

    def __enter__(self) -> "Timer":
        """Starts a new timer as a context manager.

        :return: A reference to the started Timer object.
        """

        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stops the context manager timer."""

        self.stop()
