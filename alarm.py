"""This module contains the vast majority of functions that are related
to the alarm functionality of the user interface.
"""

import datetime
import logging
from getters import access_config_file

log_filepath = access_config_file()[3]

logging.basicConfig(filename=log_filepath, encoding='utf-8',
level=logging.DEBUG)




def is_alarm_in_future(date_and_time: str) -> bool:
    """Checks whether a date and time is in the future and return a boolean.

    Parameters:
        date_and_time(str): A date and time. Must be in format 0000-00-00T00:00
        where all 0s can be converted to integers.

    Returns:
        If the date and time is in the future, True will be returned
        If the date and time is in the past, False will be returned.
        If a ValueError occurs, False will also be returned.

    Exceptions:
        Datetime cannot convert years greater that 9999. Hence if the
        year >= 10000, the value error will be caught and logged. False will
        be returned.

    Relation to main:
        When the users shcedules an alarm, if the date and time they input is in
        the past, this function will will catch it and returns False. This will
        prevent the alarm from being scheduled and return the HTML template.

        If a date and time is not entered with the appropriate format the
        function will most likely fail. In the context of the main module,
        a correctly formatted date and time should always be entered.
    """

    date_and_time = date_and_time.split("T")
    date = date_and_time[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    time = date_and_time[1].split(":")
    hours = int(time[0])
    minutes = int(time[1])

    try:
        alarm_datetime = datetime.datetime(year, month, day, hours, minutes)
    except ValueError:
        logging.warning("""FUNCTION FAILURE:is_alarm_in_future:User entered
        out of range date.""")
        return False

    return alarm_datetime > datetime.datetime.now()




def get_delay(date_and_time: str) -> float:
    """Convert a date and time into epoch time and subtract current epoch time.

    Parameters:
        date_and_time(str): A date and time. Must be in format 0000-00-00T00:00
        where all 0s can be converted to integers.
    Returns:
        Calculates a delay in seconds (float) by subtracting the current epoch
        time from the future, converted epoch time.
    Exceptions:
        No stated exceptions.
    Relation to main:
        When the user inputs a date and time the date and time will be used to
        calculate how many seconds will pass until this point is reached. This
        float will be inputted into the shceduler to tell it to wait for the
        stated number of seconds, then to trigger an announcement.

        If a date and time is not entered with the appropriate format the
        function will most likely fail. In the context of the main module,
        a correctly formatted date and time should always be entered.
    """

    date_and_time = date_and_time.split("T")
    date = date_and_time[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    time = date_and_time[1].split(":")
    hours = int(time[0])
    minutes = int(time[1])

    alarm_epoch_time = datetime.datetime(year, month, day, hours, minutes).timestamp()
    current_epoch_time = datetime.datetime.now().timestamp()

    delay = alarm_epoch_time - current_epoch_time

    return delay




def get_alarm_title(date_and_time: str) -> str:
    """Convert a date and time into a presentable title for an alarm.

    Parameters:
        date_and_time(str): A date and time. Must be in format 0000-00-00T00:00
        where all 0s can be converted to integers.
    Returns:
        Returns the date and time with the format - Date: {date}   Time: {time}.
    Exceptions:
        No stated exceptions.
    Relation to main:
        The string returned from this function will be the alarm title that is
        injected into the HTML template for the user to read.
    """

    date_and_time = date_and_time.split("T")
    date = date_and_time[0].split("-")
    time = date_and_time[1]
    year = date[0]
    month = date[1]
    day = date[2]
    date = day + "/" + month + "/" + year

    title_string = f"Date: {date}   Time: {time}"

    return title_string




def alarm_already_set(alarms: list[dict], alarm_date_and_time: str) -> bool:
    """Check whether an alarm has already been set and return a boolean.

    Parameters:
        A list of alarms that have been set by the user.
    Returns:
        Each alarm is a dictionary with a key "url_request". The function
        compares the value of each alarms "url_request" with the date and time
        of the alarm that the user wants to set. If an alarm is in "alarms"
        and has a "url_request" value equal to the alarm_date_and_time input,
        then the alarm has already been set and it will return True.

        Else, the function will return false as the alarm has not been set.
    Exceptions:
        No stated exceptions.
    Relation to main:
        The function works a sort of error prevention. If the user sets an
        alarm and then refreshes the page manually, a second alarm will be
        scheduled with all the same details and the exact same time, which can
        cause some errors. There is no utility to setting two alarms for the
        same time with the same details, so best just to avoid it.
    """

    for alarm in alarms:
        if alarm["url_request"] == alarm_date_and_time:
            logging.info("FUNCTION:alarm_already_set:Alarm already set")
            return True

    logging.info("FUNCTION:alarm_already_set:Alarm not already set")
    return False
