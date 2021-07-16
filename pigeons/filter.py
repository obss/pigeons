import logging
import re
from typing import List


class TeamsFilter(logging.Filter):
    def __init__(
        self, name: str = "", level: int = logging.INFO, capture_flags: List[str] = None, regex: bool = False
    ):
        """
        Initialize a filter for logging to Teams.

        Initialize with the name of the logger which, together with its
        children, will have its events allowed through the filter above
        the level specified.

        Parameters
        ----------
        name : str, default=''
                Name of the filter.
        level : int, default=logging.INFO
                Logging level to filter log records.
        capture_flags : List[str], default=None
                Flags to capture and send for the specified log level. Higher level
                log records are passed without being filtered.
        regex : bool, default=False
                If capture_flags are regex strings, then pass regex=True to filter log records
                with regex search. If false, only checks if log messages begins with the
                capture flag or not.

        Returns
        -------
        filter : logging.Filter
                A Filter object which can be attached to loggers or handlers.
        """
        super().__init__(name=name)
        self.level = level
        self.capture_flags = capture_flags
        self.regex = regex

    def filter(self, record: logging.LogRecord) -> bool:
        flags = self.capture_flags
        msg_match = []

        if flags is not None and record.levelno == self.level:
            for flag in flags:
                if self.regex:
                    match = re.search(flag, record.msg)
                else:
                    match = record.msg.startswith(flag)
                msg_match.append(match)
            if any(msg_match):
                return True
        elif record.levelno < self.level:
            return False
        else:  # levels above INFO
            return True

        return False
