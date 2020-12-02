"""
This module contains the unit tests for all functions included in this package.
The tests may be ran by running my the module in the command line. If an
assertion error is thrown, it will allow the user to locate the broken function
and debug it as neccessary.
"""

import datetime
from alarm import (is_alarm_in_future, get_delay,
get_alarm_title, alarm_already_set)
from getters import (get_covid_stats, get_notifications,
get_top_three_articles, get_weather, access_config_file)
from handlers import (cancel_notification, dismiss_cancelled_notifications,
check_alarm_url_request, config_file_checker)
from loggers import log_alarm


(news_api_key, weather_api_key, log_filepath) = access_config_file()[1:4]

#Alarm tests

def test_is_alarm_in_future():
    """Test various scenarios and return values for is_alarm_in_future."""

    future_date_and_time = "2050-01-01T12:00"
    past_date_and_time = "2010-01-01T12:00"
    date_out_of_range = "10000-01-01-T12:00"
    assert is_alarm_in_future(future_date_and_time) is True
    assert is_alarm_in_future(past_date_and_time) is False
    assert is_alarm_in_future(date_out_of_range) is False

def test_get_delay():
    """Test various scenarios and return values for get_delay."""

    current_time_string = str(datetime.datetime.now())[:16].replace(" ", "T")
    delay = get_delay(current_time_string)
    assert delay <= 0
    assert delay >= -60
def test_get_alarm_title():
    """Test various scenarios and return values for get_alarm_title."""

    date_and_time = "2025-12-02T02:14"
    assert get_alarm_title(date_and_time) == "Date: 02/12/2025   Time: 02:14"

def test_alarm_already_set():
    """Test various scenarios and return values for test_alarm_already_set."""

    alarms = [
    {"title": "Date: 02/12/2025   Time: 02:14",
    "content": "Test alarm",
    "url_request": "2025-12-02T02:14",
    "alarm_identifier": "Test alarm"}
    ]

    set_alarm = "2025-12-02T02:14"
    unset_alarm = "2021-12-25T00:00"

    assert alarm_already_set(alarms, set_alarm) is True
    assert alarm_already_set(alarms, unset_alarm) is False

#Getters tests

def test_get_covid_stats():
    """Test various scenarios and return values for get_covid_stats."""

    area_name = ""
    assert get_covid_stats(area_name) is None
    area_name = "Mordor"
    assert get_covid_stats(area_name) is None
    area_name = "Exeter"
    assert get_covid_stats(area_name) is not None

def test_get_weather():
    """Test various scenarios and return values for get_weather."""

    area_name = ""
    assert get_weather(weather_api_key, area_name) is None
    area_name = "Mordor"
    assert get_weather(weather_api_key, area_name) is None
    area_name = "Exeter"
    assert get_weather(weather_api_key, area_name) is not None


def test_get_notifications():
    """Test various scenarios and return values for get_notifications."""

    assert len(get_notifications(news_api_key)) > 0

def test_get_top_three_articles():
    """Test various scenarios and return values for get_top_three_articles."""

    articles = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Google is a website", "url": "www.google.com"}
    ]
    assert len(get_top_three_articles(articles)) == 3
    articles = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Google is a website", "url": "www.google.com"}
    ]
    assert len(get_top_three_articles(articles)) == 2
    articles = []
    assert get_top_three_articles(articles) is None

#Handlers tests

def test_cancel_notification():
    """Test various scenarios and return values for cancel_notification."""
    notifications = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Exeter has a website", "url": "www.exeter.ac.uk"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]
    cancelled_notifications = []

    assert cancel_notification(notifications, cancelled_notifications,
    "Exeter has a website") == {"title": "Exeter has a website",
    "url": "www.exeter.ac.uk"}

    notifications = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Exeter has a website", "url": "www.exeter.ac.uk"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]
    cancelled_notifications = [{"title": "Exeter has a website",
    "url": "www.exeter.ac.uk"}]
    assert cancel_notification(notifications, cancelled_notifications,
    "Exeter has a website") is None

def test_dismiss_cancelled_notifications():
    """Test various scenarios and return values for
    dismiss_cancelled_notifications.
    """

    notifications = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Exeter has a website", "url": "www.exeter.ac.uk"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]
    cancelled_notifications = []

    assert dismiss_cancelled_notifications(notifications,
    cancelled_notifications) == [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Exeter has a website", "url": "www.exeter.ac.uk"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]

    notifications = [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Exeter has a website", "url": "www.exeter.ac.uk"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]
    cancelled_notifications = [{"title": "Exeter has a website",
    "url": "www.exeter.ac.uk"}]

    assert dismiss_cancelled_notifications(notifications,
    cancelled_notifications) == [
    {"title": "Google is a website", "url": "www.google.com"},
    {"title": "Facebook is a website", "url": "www.facebook.com"}
    ]

def test_check_url_request():
    """Test various scenarios and return values for check_alarm_url_request."""

    url_request = "2020-12-25T00:00"
    assert check_alarm_url_request(url_request) is True
    url_request = "2020-12-25T00:000"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020_12-25T00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-12_25T00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-12-25B00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "20Y0-12-25T00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-Y2-25T00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-12-2QT00:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-12-25T0C:00"
    assert check_alarm_url_request(url_request) is False
    url_request = "2020-12-25T00:0T"
    assert check_alarm_url_request(url_request) is False

def test_config_file_checker():
    """Test various scenarios and return values for config_file_checker."""
    area_name = "Exeter"
    covid_tiers = {
      "tier_1": 10,
      "tier_2": 20,
      "tier_3": 30
    }
    refresh_rate = -1
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    refresh_rate = 0
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    refresh_rate = "1"
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    refresh_rate = 1
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is True
    covid_tiers = {
      "tier_1": 10,
      "tier_2": -1,
      "tier_3": 30
    }
    refresh_rate = 1
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    covid_tiers = {
      "tier_1": "10",
      "tier_2": 20,
      "tier_3": 30
    }
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    covid_tiers = {
      "tier_1": 40,
      "tier_2": 20,
      "tier_3": 30
    }
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    covid_tiers = {
      "tier_1": 25,
      "tier_2": 20,
      "tier_3": 30
    }
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    covid_tiers = {
      "tier_1": 10,
      "tier_2": 40,
      "tier_3": 30
    }
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    covid_tiers = {
      "tier_1": 10,
      "tier_2": 20,
      "tier_3": 30
    }
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is True
    area_name = 5
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is False
    area_name = "Exeter"
    assert config_file_checker(refresh_rate, covid_tiers, area_name) is True

#Loggers test

def test_log_alarm():
    """Test various scenarios and return values for log_alarm."""

    current_date_and_time = str(datetime.datetime.now())[:16].replace(" ", "T")

    alarm_1_in_log = False
    label_1 = "Test log_alarm:news and weather"
    log_string_1 = ("Set alarm:news&weather&" + label_1 + "&"
    + current_date_and_time)
    log_alarm(current_date_and_time, label_1, news=True, weather=True)

    alarm_2_in_log = False
    label_2 = "Test log alarm:news"
    log_string_2 = "Set alarm:news&" + label_2 + "&" + current_date_and_time
    log_alarm(current_date_and_time, label_2, news=True)

    alarm_3_in_log = False
    label_3 = "Test log alarm:weather"
    log_string_3 = "Set alarm:weather&" + label_3 + "&" + current_date_and_time
    log_alarm(current_date_and_time, label_3, weather=True)

    alarm_4_in_log = False
    label_4 = "Test log_alarm"
    log_string_4 = "Set alarm:" + label_4 + "&" + current_date_and_time
    log_alarm(current_date_and_time, label_4)

    with open(log_filepath) as logfile:
        for line in logfile.readlines():
            line = line.strip("\n")
            if line[10:] == log_string_1:
                alarm_1_in_log = True
            elif line[10:] == log_string_2:
                alarm_2_in_log = True
            elif line[10:] == log_string_3:
                alarm_3_in_log = True
            elif line[10:] == log_string_4:
                alarm_4_in_log = True

    assert alarm_1_in_log is True
    assert alarm_2_in_log is True
    assert alarm_3_in_log is True
    assert alarm_4_in_log is True


test_is_alarm_in_future()
test_get_delay()
test_get_alarm_title()
test_alarm_already_set()
test_get_covid_stats()
test_get_weather()
test_get_notifications()
test_get_top_three_articles()
test_cancel_notification()
test_dismiss_cancelled_notifications()
test_check_url_request()
test_config_file_checker()
test_log_alarm()
print("All tests passed successfully.")
