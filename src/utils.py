import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def is_valid_date(date_str: str) -> bool:
    try:
        # Tries to parse the string matching the DD-MM-YYYY format exactly
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        # Triggers if the format is wrong or the date does not exist
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


