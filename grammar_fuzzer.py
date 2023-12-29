import random

from parameter_generator import ParameterGenerator


class GrammarFuzzer(ParameterGenerator):
    """Generates input parameters for gOATcat that conform to the rules of gOATcat.

    Run goatcat -h to see the rules of the application.
    """

    def __init__(self) -> None:
        """The initialization routine of the GrammarFuzzer."""

        super().__init__()
        self._parameter_count: int = 0
        self._characters_in_path: list[str] = ["y", "a", "h", "2", "j", "6", "9", "l", "m", "z", "p", "e"]
        self._forward_slash: str = "/"
        self._max_path_depth: int = 1
        self._max_directory_name_length: int = 2
        self._max_filename_length: int = 2
        self._filename_extension: str = ".txt"

    def _increment_parameter_count(self) -> int:
        """Increments the value of the parameter count.

        :return: The new value of the parameter count property.
        """

        self._parameter_count += 1
        return self._parameter_count

    def next_parameter(self) -> tuple[int, str]:
        """Randomly generates parameters that syntactically conform to the rules of gOATcat.

        :return: The number of the generated parameter and the next generated parameter.
        """

        while True:
            path_depth: int = random.randint(0, self._max_path_depth)
            filenames: list[str] = list()

            for path_level in range(path_depth):
                directory_name_length: int = random.randint(1, self._max_directory_name_length)
                filenames.append("".join(random.choices(self._characters_in_path, k=directory_name_length)))

            filename_length: int = random.randint(1, self._max_filename_length)
            filenames.append("".join(random.choices(self._characters_in_path, k=filename_length)))

            parameter_count: int = self._increment_parameter_count()
            parameter: str = self._forward_slash + self._forward_slash.join(filenames) + self._filename_extension
            yield parameter_count, parameter
