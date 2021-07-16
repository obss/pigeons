# pigeons

![](assets/logo.png)

Pigeons is an easy and practical alert tool which enables sending logs to MSTeams. 
It also supports dynamic filtering of log records with an option to use 
regex to capture records of any logger.

## Installation

### Installing through pip

    pip install pigeons

### Build from source
    
    git clone https://github.com/obss/pigeons
    cd pigeons
    python setup.py install

## Usage
Pigeons is easy to use with just two line of codes.
    
    import sys

    from pigeon import init_logger, pigeon_excepthook

    sys.excepthook = pigeon_excepthook
    logger = init_logger(
        ...
    )


### With Start Flags
Pigeons will look for specified flags in the beginning of the log for 
the specified log level. If the log message starts with the flag, then
it will be sent to specified endpoint.

    import logging

    from pigeon import init_logger

    endpoint = "https://custom_domain.com/api/..."
    my_flag = "!my_flag "
    logger = init_logger(
            endpoint=endpoint,
            level=logging.INFO, # Default
            log_to_teams=True,
            tf_capture_flags=[my_flag],
            tf_regex=False
    )

### With Regex
Pigeons will look for specified regex in the log for the specified log level. 
If the log message matches the regex, then it will be sent to specified endpoint.

    import logging

    from pigeon import init_logger

    endpoint = "https://custom_domain.com/api/..."
    my_regex = "^[a-zA-Z0-9]+$"
    logger = init_logger(
            endpoint=endpoint,
            level=logging.INFO, # Default
            log_to_teams=True,
            tf_capture_flags=[my_regex],
            tf_regex=True
    )

### Uncaught Exceptions

Pigeons has a custom excepthook for handling uncaught exceptions.
To handle uncaught exceptions just override `sys.excepthook` as follows

    importy sys
    from pigeon import pigeon_excepthook

    sys.excepthook = pigeon_excepthook

### Examples

    # Lower levels will be ignored.
    logger.debug("This log will be ignored.")
    
    # At level=level (logging.INFO)
    logger.info("This log is ignored".)
    logger.info(my_flag + "This log is captured and sent to Teams.")
    
    # Higher levels will always be captured regardless presence of flag.    
    logger.warning("This is sent.")
    logger.error("This is also sent.")
    logger.critical("Another captured message.")
    logger.fatal("And another one.")

## Contributing

PRs are always welcomed.

### Installation

    git clone https://github.com/obss/pigeons.git
    cd pigeons
    python setup.py develop
    pip install -r requirements-dev.txt

### Tests

To tests simply run.

    pytest tests/

Pigeons uses black to assure code style standard.

    black . --config pyproject.toml


## License

Licensed under the [MIT](LICENSE) License.