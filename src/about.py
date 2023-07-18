""" Contains the project details,
    e.g., *title*, *version*, *summary* etc.
"""

__MAJOR__ = 1
__MINOR__ = 0
__PATCH__ = 0

__title__ = "Sentence Encoder"
__version__ = ".".join([str(__MAJOR__), str(__MINOR__), str(__PATCH__)])
__summary__ = "Encodes a sentence or a batch of sentences into a vector."
__author__ = "Elisavet Palogiannidi"
__copyright__ = f"Copyright (C) 2023 {__author__}"
__email__ = "epalogiannidi@gmail.com"


if __name__ == "__main__":
    print(__version__)
