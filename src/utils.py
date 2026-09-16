import logging
from datetime import datetime

from src.config import SUBSCRIPTION_DATE_FORMAT

logger = logging.getLogger(__name__)

def is_valid_date(date_str: str, date_format: str = SUBSCRIPTION_DATE_FORMAT) -> bool:
    """Whether the string is a real date written in the expected format.

    The format defaults to the one subscriptions are stored in, so callers do
    not each repeat the pattern and drift apart from the database.
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except (ValueError, TypeError):
        # Triggers if the format is wrong, the date does not exist, or it is None
        return False


def is_valid_number(number) -> bool:
    """Validates that the input is a positive numerical amount greater than zero."""
    try:
        # Convert to float to support both whole numbers and decimals
        value = float(number)

        if value <= 0:
            logger.warning("rejected amount %r: not greater than zero", number)
            return False

        return True

    except (ValueError, TypeError):
        # Triggers if the input contains letters, symbols, or is None
        logger.warning("rejected amount %r: not a number", number)
        return False


