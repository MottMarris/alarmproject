"""This module contains three functions that interact with global variables
that are injected into the HTML template. There is also a function that handles
url requests. The final function is the user_interface function, which
directly or indirectly uses almost every other previously defined function
in order to coordinate the logic for the user interface and allow user to
perform all the intended functionality.
"""

import sched
import time
import logging
import json
import pyttsx3
from flask import Flask
from flask import render_template
from flask import request
from alarm import is_alarm_in_future
from alarm import get_delay
from alarm import get_alarm_title
from alarm import alarm_already_set
from getters import get_notifications
from getters import test_apis
from getters import access_config_file
from handlers import cancel_notification
from handlers import dismiss_cancelled_notifications
from handlers import check_alarm_url_request
from handlers import config_file_checker
from announcement import announcement
from loggers import log_alarm

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
tts = pyttsx3.init()

(area_name, news_api_key, weather_api_key, log_filepath, refresh_rate,
covid_tiers) = access_config_file()

with open("config.json", "r") as config_file:
    config_file = json.load(config_file)
    title = config_file["title"]
    image = config_file["image"]

logging.basicConfig(filename=log_filepath, encoding='utf-8',
level=logging.DEBUG)

alarms = []
notifications = get_notifications(news_api_key)
cancelled_notifications = []
PAGE_REFRESHES = 0




def set_alarm(alarm_date_and_time: str, label: str, news: bool = False,
weather: bool = False):
    """Schedules an annoucement for the date and time specified.

    Parameters:
        date_and_time(str): A date and time. Must be in format 0000-00-00T00:00
        where all 0s can be converted to integers.

        label(str): The piece of text that will be used to label the alarm.

        news(bool): Determines whether the alarm will include a news briefing.

        weather(bool): Determines whether the alarm will include a weather
        briefing.
    Returns:
        None
    Exceptions:
        No stated exceptions.
    Use in main:
        The function uses the is_alarm_in_future function to check whether the
        date and time entered is in the future. If it is, the function will
        continue, if not it will return None. The function will then use the
        get_delay to calculate the time the shceduler should wait until it
        triggers the annoucement. An event is then entered to the shceduler
        with the delay, the annoucement function identifier and the boolean
        values for news and weather as inputs. An alarm title is produced via
        the get_alarm_title function. The atributes of the alarm are then as
        follows: the alarm title, the label, the original url request and the
        identifier that is return from the scheduler fucntion enter(). These
        are then used to form a dictionary with all the alarms attributes,
        which is then appended to the list of active alarms. None is returned.
    """

    if not is_alarm_in_future(alarm_date_and_time):
        return None

    delay = get_delay(alarm_date_and_time)

    alarm_identifier = s.enter(delay, 1, announcement,
    kwargs={"news": news, "weather": weather})

    alarm_title = get_alarm_title(alarm_date_and_time)
    new_alarm = {"title": alarm_title, "content": label,
    "url_request": alarm_date_and_time, "identifier": alarm_identifier}
    alarms.append(new_alarm)

    return None




def user_cancel_alarm(alarm_to_cancel: str):
    """Removes an alarm from the list of alarms and from the shceduler.

    Parameters:
        alarm_to_cancel(str): A date and time in format 0000-00-00T00:00
        where all 0s can be converted to integers.
    Returns:
        None
    Exceptions:
        Due to page refreshes, sometimes the function may attempt to remove an
        alarm from the alarm list that isn't in there, causing a ValueError.
        This is caught and logged.

        Also due to page refreshes, the function may sometimes attempt to
        cancel a shceduler function that has already been cancelled, causing a
        TypeError. This is also caught and logged.
    Use in main:
        When the user clicks the cancel button on an alarm in the user
        interface, the request will be passed into the function. The alarms
        in alarms will then be looped through, comparing their "title" value
        to the value of alarm_to_cancel. When the correspoding alarm is found,
        it will be removed from the list of alarms. The alarms "identifier"
        value is then used to remove the alarm from the shceduler. The
        cancellation is logged and is used be the restore_state function
        to ensure cancelled alarms are not restored upon restart.
    """

    for alarm in alarms:
        if alarm["title"] == alarm_to_cancel:
            try:
                alarms.remove(alarm)
                s.cancel(alarm["identifier"])
                logging.info("Alarm cancel:" + alarm["url_request"])
                logging.info("FUNCTION:user_cancel_alarm:cancelled alarm="
                + alarm_to_cancel)
            except ValueError:
                logging.warning("FUNCTION:user_cancel_alarm:"
                + alarm_to_cancel + "already removed")
            except TypeError:
                logging.warning("FUNCTION:user_cancel_alarm"
                + alarm_to_cancel + "already cancelled")




def restore_state():
    """Restores not yet triggered after an application restart.

    Parameters:
        None
    Returns:
        None
    Exceptions:
        No stated exceptions.
    Use in main:
        The function will loop through the lines in the log file to find alarms
        that have been shceduled and alarms that have been cancelled, appending
        them to their respective lists. The information contained within the
        alarms log file line is used to determine the date and time it was
        shceduled for, the label of the alarm and whether the user wanted a
        news/weather briefing. The alarms in cancelled alarms are not restored,
        and the alarms that have already been expired will be filtered out by
        the is_alarm_in_future function contained within the set_alarm
        function.
    """

    with open(log_filepath) as logfile:
        restore_alarms = []
        cancelled_alarms = []
        for line in logfile.readlines():
            line = line.strip("\n")
            if line[:4] == "INFO" and line[10:19] == "Set alarm":
                alarm_info = line[20:]
                restore_alarms.append(alarm_info)
            if line[:4] == "INFO" and line[10:22] == "Alarm cancel":
                alarm_info = line[-16:]
                cancelled_alarms.append(alarm_info)

    for alarm in restore_alarms:
        info = alarm.split("&")
        if info[-1] not in cancelled_alarms:
            if "news" in info and "weather" in info:
                set_alarm(info[3], info[2], news=True, weather=True)
            elif "news" in info:
                set_alarm(info[2], info[1], news=True)
            elif "weather" in info:
                set_alarm(info[2], info[1], weather=True)
            else:
                set_alarm(info[1], info[0], weather=True)

    logging.info("FUNCTION:restore_state:Past state succesfully restored")




def get_args() -> tuple[str]:
    """Exracts arguments from url requests to be passed into user_interface.

    If the user edits the alarm date and time in the url, it will return it
    as an empty string. If the label contains the & symbol, it will also
    return the alarm date and time as en empty string to prevent a software
    failure.
    """

    alarm_date_and_time = request.args.get("alarm")
    include_news = request.args.get("news")
    include_weather = request.args.get("weather")
    label = request.args.get("two")
    notification_to_cancel = request.args.get("notif")
    alarm_to_cancel = request.args.get("alarm_item")

    if not check_alarm_url_request(alarm_date_and_time):
        alarm_date_and_time = ""

    if label:
        if "&" in label:
            alarm_date_and_time = ""

    return (alarm_date_and_time, include_news, include_weather, label,
    notification_to_cancel, alarm_to_cancel)




@app.route("/index")
def user_interface():
    """Coordinates the logic for the user interface.

    Parameters:
        None
    Returns:
        Returnsrender_template function with an assigned template that displays
        a picture, a title, the shceduled alarms and the news notifications.
    Exceptions:
        No stated exceptions.
    Use in main:
        To begin with s.run is called in order to start any announcements that
        were scheduled to go off at this time. Next, the get_args function
        is called in order to retrieve all the neccesary url requests. Then
        the functions checks to see if it should refresh the notifications. If
        it should, it will call the get_notifications function to get the most
        recent notifications. The number of times the page has been refreshed
        will be incremented by 1. If notification to cancel is not an empty
        string, cancel notifications will be called and the cancelled
        notification will be appended to to the list of cancelled
        notifications. The dismiss_cancelled_notifications function will then
        be called to remove the cancelled notifications from the notifications
        data structure. If alarm_to_cancel is not an empty string, the
        user_cancel_alarm will be called to cancel the alarm. If
        alarm_date_and_time is not an empty string and the alarm_already_set
        function returns that the alarm is not already set, the alarm will be
        logged via log_alarm. Then, depending on whether include_weather and
        include_news are both empty strings, both not empty strings, or only
        one of them is an empty string, different combinations of set alarm
        will be called to set the alarm. The user interface will then once
        again be returned to the user.
    """

    global notifications
    global PAGE_REFRESHES

    s.run(blocking=False)

    (alarm_date_and_time, include_news, include_weather, label,
    notification_to_cancel, alarm_to_cancel) = get_args()
    if PAGE_REFRESHES % refresh_rate == 0:
        notifications = get_notifications(news_api_key)

    PAGE_REFRESHES += 1

    if notification_to_cancel:
        cancelled_notification = cancel_notification(notifications,
        cancelled_notifications, notification_to_cancel)
        cancelled_notifications.append(cancelled_notification)

    notifications = dismiss_cancelled_notifications(notifications,
    cancelled_notifications)

    if alarm_to_cancel:
        user_cancel_alarm(alarm_to_cancel)

    if alarm_date_and_time and not alarm_already_set(alarms,
    alarm_date_and_time):

        log_alarm(alarm_date_and_time, label, include_news, include_weather)

        if include_news and include_weather:
            set_alarm(alarm_date_and_time, label, news=True, weather=True)
        elif include_news:
            set_alarm(alarm_date_and_time, label, news=True)
        elif include_weather:
            set_alarm(alarm_date_and_time, label, weather=True)
        else:
            set_alarm(alarm_date_and_time, label)

    return render_template("index.html", image=image, title=title,
    notifications=notifications, alarms=alarms)




if __name__ == "__main__":
    if (test_apis(area_name, news_api_key, weather_api_key)
    and config_file_checker(refresh_rate, covid_tiers, area_name)):
        restore_state()
        app.run()
    else:
        logging.warning("API FAILURE:Check logs")
        logging.warning("CONFIG_FILE:Ensure config file is configured right.")
