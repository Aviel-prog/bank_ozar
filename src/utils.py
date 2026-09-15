from datetime import datetime

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
            print("Amount must be greater than zero.")
            return False

        return True

    except (ValueError, TypeError):
        # Triggers if the input contains letters, symbols, or is None
        print("Please enter a valid numeric value.")
        return False


