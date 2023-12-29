import itertools
import string

from parameter_generator import ParameterGenerator


class BruteForcer(ParameterGenerator):
    """Generates input parameters naively for gOATcat."""

    def __init__(self) -> None:
        """The initialization routine of the BruteForcer."""

        super().__init__()
        self._parameter_count: int = 0
        self._characters: str = " " + string.punctuation + string.digits + string.ascii_letters

    def _increment_parameter_count(self) -> int:
        """Increments the value of the parameter count.

        :return: The new value of the parameter count property.
        """

        self._parameter_count += 1
        return self._parameter_count

    def next_parameter(self) -> tuple[int, str]:
        """Systematically generates increasingly long strings with printable ASCII characters (0, 1, ..., 00, 01, ...).
        Source: https://stackoverflow.com/questions/68668662/infinity-generation-of-ascii-combinations

        :return: The number of the generated parameter and the next generated parameter.
        """

        for length in itertools.count(1):
            for letters in itertools.permutations(self._characters, length):
                parameter_count: int = self._increment_parameter_count()
                parameter: str = ''.join(letters)
                yield parameter_count, parameter
