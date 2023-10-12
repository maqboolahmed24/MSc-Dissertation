#suppress TensorFlow warnings
import contextlib
import gym
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
import logging
logging.getLogger('tensorflow').setLevel(logging.FATAL)

#suppress Python warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

#suppress other print outputs (like from C/C++ code)
import sys
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr.close()
        sys.stderr = self._original_stderr

#automatically initiate hidden prints upon importing
with HiddenPrints():
    pass


@contextlib.contextmanager
def suppress_torcs_output():
    original_stdout = os.dup(1)
    original_stderr = os.dup(2)
    os.close(1)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    try:
        yield None
    finally:
        os.dup2(original_stdout, 1)
        os.dup2(original_stderr, 2)
