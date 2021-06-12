"""Collection of tests around log handling."""
import logging
import unittest
from logger import configure_logger
from version import NAME


def create_log_records():
    """Test function, create log entries in expected stage of test."""
    mooringSimulator_logger = logging.getLogger('NAME')
    foo_logger = logging.getLogger(f"{NAME}.foo")
    foobar_logger = logging.getLogger(f"{NAME}.foo.bar")

    mooringSimulator_logger.info(f"Welcome to {NAME}")
    mooringSimulator_logger.debug('Generating project from unittest-plugin')
    foo_logger.info('Loading user config from home dir')
    foobar_logger.debug("I don't know.")
    foobar_logger.debug('I wanted to save the world.')
    foo_logger.error('Aw, snap! Something went wrong')
    mooringSimulator_logger.debug('Successfully generated project')


#@unittest.fixture
def info_messages():
    """Fixture. List of test info messages."""
    return [
        'INFO: Welcome to mooringSimulator',
        'INFO: Loading user config from home dir',
        'ERROR: Aw, snap! Something went wrong',
    ]


#@unittest.fixture
def debug_messages():
    """Fixture. List of test debug messages."""
    return [
        "INFO mooringSimulator: Welcome to mooringSimulator",
        "DEBUG mooringSimulator: Generating project from unittest-plugin",
        "INFO mooringSimulator.foo: Loading user config from home dir",
        "DEBUG mooringSimulator.foo.bar: I don't know.",
        "DEBUG mooringSimulator.foo.bar: I wanted to save the world.",
        "ERROR mooringSimulator.foo: Aw, snap! Something went wrong",
        "DEBUG mooringSimulator: Successfully generated project",
    ]


#@unittest.fixture
def info_logger():
    """Fixture. Call mooringSimulator logger setup with `info` debug level."""
    return configure_logger(stream_level='INFO')


#@unittest.fixture
def debug_logger():
    """Fixture. Call mooringSimulator logger setup with `debug` debug level."""
    return configure_logger(stream_level='DEBUG')


#@unittest.fixture
def debug_file(tmp_path):
    """Fixture. Generate debug file location for tests."""
    return tmp_path.joinpath('unittest-plugin.log')


#@unittest.fixture
def info_logger_with_file(debug_file):
    """Fixture. Call mooringSimulator logger setup with `info` debug level + `file`."""
    return configure_logger(stream_level='INFO', debug_file=str(debug_file))


def test_info_stdout_logging(caplog, info_logger, info_messages):
    """Test that stdout logs use info format and level."""
    [stream_handler] = info_logger.handlers
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.INFO

    create_log_records()

    stream_messages = [
        stream_handler.format(r)
        for r in caplog.records
        if r.levelno >= stream_handler.level
    ]

    assert stream_messages == info_messages


def test_debug_stdout_logging(caplog, debug_logger, debug_messages):
    """Test that stdout logs use debug format and level."""
    [stream_handler] = debug_logger.handlers
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.DEBUG

    create_log_records()

    stream_messages = [
        stream_handler.format(r)
        for r in caplog.records
        if r.levelno >= stream_handler.level
    ]

    assert stream_messages == debug_messages


def test_debug_file_logging(caplog, info_logger_with_file, debug_file, debug_messages):
    """Test that logging to stdout uses a different format and level than \
    the the file handler."""
    [file_handler, stream_handler] = info_logger_with_file.handlers
    assert isinstance(file_handler, logging.FileHandler)
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.INFO
    assert file_handler.level == logging.DEBUG

    create_log_records()

    assert debug_file.exists()

    # Last line in the log file is an empty line
    with debug_file.open() as f:
        assert f.read().split('\n') == debug_messages + ['']
