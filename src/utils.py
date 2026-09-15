from datetime import datetime

def is_valid_date(date_str: str) -> bool:
    try:
        # Tries to parse the string matching the DD-MM-YYYY format exactly
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        # Triggers if the format is wrong or the date does not exist
        return False

