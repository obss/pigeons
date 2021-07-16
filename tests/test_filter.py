import logging

from pigeons.filter import TeamsFilter


def test_filter_without_capture_flags():
    log_record_dict = {"msg": "Test log at INFO level.", "levelno": logging.INFO}
    test_log_record = logging.makeLogRecord(log_record_dict)
    tf = TeamsFilter(level=logging.INFO)
    filtered = tf.filter(test_log_record)

    assert filtered


def test_filter_with_capture_flags():
    capture_flag = "$test_flag "
    log_record_dict_true = {"msg": capture_flag + "Test log at INFO level.", "levelno": logging.INFO}
    log_record_dict_false = {"msg": "Test log at INFO level.", "levelno": logging.INFO}
    test_log_record_true = logging.makeLogRecord(log_record_dict_true)
    test_log_record_false = logging.makeLogRecord(log_record_dict_false)
    tf = TeamsFilter(level=logging.INFO, capture_flags=[capture_flag])
    filtered_true = tf.filter(test_log_record_true)
    filtered_false = tf.filter(test_log_record_false)

    assert filtered_true and not filtered_false


def test_filter_with_higher_levels():
    capture_flag = "$test_flag "
    log_record_dict_true = {"msg": capture_flag + "Test log at INFO level.", "levelno": logging.ERROR}
    log_record_dict_false = {"msg": "Test log at INFO level.", "levelno": logging.ERROR}
    test_log_record_true = logging.makeLogRecord(log_record_dict_true)
    test_log_record_false = logging.makeLogRecord(log_record_dict_false)
    tf = TeamsFilter(level=logging.INFO, capture_flags=[capture_flag])

    # Both should pass regardless of flags.
    filtered_true = tf.filter(test_log_record_true)
    filtered_false = tf.filter(test_log_record_false)

    assert filtered_true and filtered_false


def test_filter_with_lower_levels():
    capture_flag = "$test_flag "
    log_record_dict_true = {"msg": capture_flag + "Test log at DEBUG level.", "levelno": logging.DEBUG}
    log_record_dict_false = {"msg": "Test log at DEBUG level.", "levelno": logging.DEBUG}
    test_log_record_true = logging.makeLogRecord(log_record_dict_true)
    test_log_record_false = logging.makeLogRecord(log_record_dict_false)
    tf = TeamsFilter(level=logging.INFO, capture_flags=[capture_flag])

    # Both should fail regardless of flags.
    filtered_true = tf.filter(test_log_record_true)
    filtered_false = tf.filter(test_log_record_false)

    assert not filtered_true and not filtered_false
