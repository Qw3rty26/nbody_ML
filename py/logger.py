import logging
import sys

class DebugFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)

        if record.levelno == logging.DEBUG:
            return f"\033[95m{message}\033[0m"

        return message


def configure_logging(verbose: bool, debug: bool):

    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        DebugFormatter(
            "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
            "%H:%M:%S"
        )
    )

    logging.basicConfig(
        level=level,
        handlers=[
            handler
        ]
    )
