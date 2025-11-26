import phonenumbers

def normalize_mobile(mobile: str) -> str:
    """
    Normalizes Iranian phone numbers.
    Input examples:
        "09191234567"
        "9191234567"
        "+989191234567"
    Output:
        "9191234567"
    """

    # Remove all non-digit chars
    digits = ''.join(filter(str.isdigit, mobile))
    
    # Now parse using phonenumbers
    try:
        parsed = phonenumbers.parse(digits, "IR")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError("Invalid mobile number format")

    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Invalid Iranian mobile number")

    # Return NATIONAL number like "9191234567"
    return str(parsed.national_number)
