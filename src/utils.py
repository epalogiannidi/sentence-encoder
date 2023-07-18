import time
import yaml
from datetime import timedelta


class Timer:
    """Context manager to count elapsed time

    Example:
    --------
    .. highlight:: python
    .. code-block:: python

        with Timer() as t:
            y = f(x)
        print(f'Invocation of f took {t.elapsed}s!')
    """

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *args):
        self._end = time.time()
        self._elapsed = self._end - self._start
        self.elapsed = str(timedelta(seconds=self._elapsed))


class SetUpConfig:
    def __init__(self):
        self.config_path = "configs/encoder.yml"

        with open(self.config_path, "r") as cf:
            self.config_values = yaml.safe_load(cf)
