import json
import logging
import pytest

from requests.exceptions import SSLError

from pigeon import init_logger


channels = "channels.json"
channel_key = "TEST"

DEFAULT_FLAG = "$my_flag "


def test_init_logger_with_json_file():
    logger = init_logger(
            endpoint=channels,
            endpoint_key=channel_key,
            log_to_teams=True,
            tf_capture_flags=[DEFAULT_FLAG],
            tf_regex=False
    )

    assert isinstance(logger, logging.Logger)


def test_init_logger_with_url():
    logger = init_logger(
            endpoint=channels,
            endpoint_key=channel_key,  # should be ignored
            log_to_teams=True,
            tf_capture_flags=[DEFAULT_FLAG],
            tf_regex=False
    )

    assert isinstance(logger, logging.Logger)


def test_init_logger_with_dict():
    with open(channels, 'r') as jf:
        channels_dict = json.load(jf)

    logger = init_logger(
            endpoint=channels_dict,
            endpoint_key=channel_key,
            log_to_teams=True,
            tf_capture_flags=[DEFAULT_FLAG],
            tf_regex=False
    )

    assert isinstance(logger, logging.Logger)


def test_init_logger_with_malformed_url():
    endpoint = "http://google"

    with pytest.raises(AssertionError):
        init_logger(
                endpoint=endpoint,
                log_to_teams=True,
                tf_capture_flags=[DEFAULT_FLAG],
                tf_regex=False
        )


def test_init_logger_non_exist_url():
    endpoint = "https://qweasdqwe.com/api/v2"

    with pytest.raises(SSLError):
        init_logger(
                endpoint=endpoint,
                log_to_teams=True,
                tf_capture_flags=[DEFAULT_FLAG],
                tf_regex=False
        )
