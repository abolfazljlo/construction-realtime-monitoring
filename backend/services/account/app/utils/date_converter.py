import jdatetime
from datetime import date

def jalali_to_gregorian(jalali_str: str) -> date:
    """
    Converts Jalali date string (YYYY-MM-DD or YYYY/MM/DD) into Gregorian date.
    """
    clean = jalali_str.replace("/", "-")
    parts = clean.split("-")

    if len(parts) != 3:
        raise ValueError("Invalid Jalali date format")

    jy, jm, jd = map(int, parts)

    j = jdatetime.date(jy, jm, jd)
    return j.togregorian()

def gregorian_to_jalali(gregorian_date: date) -> str:
    """
    Converts Gregorian date to Jalali date string (YYYY/MM/DD).
    """
    j_date = jdatetime.date.fromgregorian(date=gregorian_date)
    return f"{j_date.year}/{j_date.month}/{j_date.day}"