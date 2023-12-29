from abc import ABC, abstractmethod


class ParameterGenerator(ABC):
    """Abstract base class for parameter generators to specialize."""

    def __init__(self) -> None:
        """The initialization routine of the parameter generator."""

        self._parameter_count = 0

    @property
    @abstractmethod
    def _increment_parameter_count(self) -> int:
        """Increments the value of the parameter count."""

        self._parameter_count += 1
        return self._parameter_count

    @abstractmethod
    def next_parameter(self) -> tuple[int, str]:
        """Generates the next parameter using some logic.

        :return: The number of the generated parameter and the next generated parameter.
        """

        raise NotImplementedError
