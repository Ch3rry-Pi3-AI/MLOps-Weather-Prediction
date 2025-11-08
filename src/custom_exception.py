"""
custom_exception.py
-------------------
Defines a custom exception class for unified and descriptive error handling
throughout the MLOps project.

This module standardises how exceptions are raised and reported by including
information such as the file name and line number where the error occurred,
plus a formatted traceback where available.

Usage
-----
Example (within any module):

    from src.custom_exception import CustomException
    import sys

    try:
        result = 10 / 0
    except Exception as e:
        # Either of these is fine:
        raise CustomException("Division error", sys) from e
        # or
        raise CustomException("Division error", e)

Notes
-----
- The exception message includes both the file name and line number when they
  can be determined from the traceback.
- Accepts `sys`, an exception instance, or nothing (falls back to current
  `sys.exc_info()`), so you won't get missing-argument errors.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import sys
import traceback
from typing import Any


# -------------------------------------------------------------------
# Custom Exception Class
# -------------------------------------------------------------------
class CustomException(Exception):
    """
    A custom exception class that enhances error messages with detailed
    context (file name and line number) and a formatted traceback.

    Parameters
    ----------
    error_message : str
        A human-readable description of the error.
    error_detail : Any | None, default=None
        One of:
          • the `sys` module (so we can call `sys.exc_info()`),
          • an Exception instance (to read its `__traceback__`), or
          • None (falls back to current `sys.exc_info()`).

    Attributes
    ----------
    error_message : str
        The formatted error message including file name, line number, and
        traceback (when available).
    """

    def __init__(self, error_message: str, error_detail: Any | None = None):
        super().__init__(error_message)
        self.error_message = self._build_detailed_message(error_message, error_detail)

    # -------------------------------------------------------------------
    # Static Method: Error Message Formatter
    # -------------------------------------------------------------------
    @staticmethod
    def _build_detailed_message(error_message: str, error_detail: Any | None) -> str:
        """
        Construct a detailed error message containing the file name,
        line number, and formatted traceback (when available).
        """
        # Case 1: detail looks like the sys module (has exc_info)
        if error_detail is not None and hasattr(error_detail, "exc_info"):
            _, _, tb = error_detail.exc_info()
            if tb:
                last_tb = tb
                while last_tb.tb_next:
                    last_tb = last_tb.tb_next
                file_name = last_tb.tb_frame.f_code.co_filename
                line_number = last_tb.tb_lineno
                tb_str = "".join(traceback.format_tb(tb))
                return f"Error in {file_name}, line {line_number}: {error_message}\n{tb_str}".rstrip()

        # Case 2: detail is an Exception instance
        if isinstance(error_detail, BaseException):
            tb = error_detail.__traceback__
            last_tb = tb
            while last_tb and last_tb.tb_next:
                last_tb = last_tb.tb_next
            file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
            line_number = last_tb.tb_lineno if last_tb else "?"
            tb_str = "".join(traceback.format_exception(type(error_detail), error_detail, tb))
            return f"Error in {file_name}, line {line_number}: {error_message}\n{tb_str}".rstrip()

        # Case 3: no detail provided; try current sys.exc_info()
        etype, evalue, tb = sys.exc_info()
        if tb:
            last_tb = tb
            while last_tb.tb_next:
                last_tb = last_tb.tb_next
            file_name = last_tb.tb_frame.f_code.co_filename
            line_number = last_tb.tb_lineno
            tb_str = "".join(traceback.format_exception(etype, evalue, tb))
            return f"Error in {file_name}, line {line_number}: {error_message}\n{tb_str}".rstrip()

        # Fallback: just the message
        return error_message

    # -------------------------------------------------------------------
    # String Representation
    # -------------------------------------------------------------------
    def __str__(self) -> str:
        """Return the formatted error message when the exception is printed."""
        return self.error_message