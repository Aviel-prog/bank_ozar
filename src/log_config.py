"""Logging setup for the banking application."""

import logging

from src.config import LOG_LEVEL, LOG_PATH


def setup_logging() -> None:
    """Sends the application's logs to a file, away from the terminal.

    The menu is a conversation with the person at the keyboard, so stdout
    belongs to them. An audit line landing in the middle of the balance they
    just asked for would be noise to the customer and a lost record to the
    bank, so the two go to different places.
    """
    logging.basicConfig(
        filename=LOG_PATH,
        level=LOG_LEVEL,
        format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
    )
