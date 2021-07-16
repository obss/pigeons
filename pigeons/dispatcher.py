import json
import logging
import os
import sys
import traceback
from typing import Union, Dict, List

import requests
from teams_logger import TeamsHandler, Office365CardFormatter
import validators

from pigeons.filter import TeamsFilter


def _check_url(endpoint):
    assert validators.url(endpoint)

    response = requests.head(url=endpoint)
    assert response.status_code == 200, "Endpoint is not available."


def init_logger(
    endpoint: Union[str, Dict[str, str]],
    endpoint_key: str = None,
    name: str = None,
    level: int = logging.INFO,
    log_to_teams: bool = True,
    tf_capture_flags: List[str] = None,
    tf_regex: bool = False,
):
    """
    Initialize a filter for logging to Teams.

    Initialize with the name of the logger which, together with its
    children, will have its events allowed through the filter above
    the level specified.

    Parameters
    ----------
    endpoint : str, default=''
            Name of the filter.
    endpoint_key: str, default=None
            Ignored if endpoint is URL, otherwise indicates key for dict.
    name: str
            Logger name.
    level: int, default=logging.INFO
            Log level.
    log_to_teams: bool, default=True
            Whether to send logs to MSTeams or not.
    tf_capture_flags: List[str], default=None
            Flags to capture in log records for specified level.
    tf_regex: bool, default=False
            Whether capture flags are regex or not.

    Returns
    -------
    filter : logging.Logger
            Logger object.
    """
    if isinstance(endpoint, str):
        if os.path.exists(endpoint):
            endpoint = get_endpoint_from_file(filepath=endpoint, key=endpoint_key)
    if isinstance(endpoint, dict):
        endpoint = endpoint.get(endpoint_key)

    _check_url(endpoint)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if log_to_teams:
        th = TeamsHandler(url=endpoint, level=logging.INFO)
        logger.addHandler(th)
        cf = Office365CardFormatter(facts=["name", "levelname", "lineno"])
        th.setFormatter(cf)
        tf = TeamsFilter(capture_flags=tf_capture_flags, regex=tf_regex)
        logger.addFilter(tf)

    return logger


def get_endpoint_from_file(filepath, key):
    with open(filepath, "r") as jf:
        endpoints = json.load(jf)

    return endpoints.get(key)


def pigeon_excepthook(exc_type, exc_value, exc_traceback):
    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    err = ["An uncaught exception occurred:", f"Value: {repr(exc_value)}"]

    if exc_traceback:
        format_exception = "".join(traceback.format_tb(exc_traceback))
        format_exception = f"<pre>{format_exception}</pre>"
        err.append(format_exception)

    fmt_err = "   \n".join(err)
    logging.exception(fmt_err)
    raise exc_type(exc_value)
