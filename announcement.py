"""This module contains a function to form an announcement string and then
use the text to speech module to speak it.
"""

import logging
import pyttsx3
from getters import get_covid_stats
from getters import get_notifications
from getters import get_top_three_articles
from getters import get_weather
from getters import access_config_file

(area_name, news_api_key, weather_api_key,
log_filepath) = access_config_file()[:4]

covid_tiers = access_config_file()[5]

logging.basicConfig(filename=log_filepath, encoding='utf-8',
level=logging.DEBUG)

def announcement(news: bool = False, weather: bool = False):
    """Uses text to speech to give an update on news, weather and COVID-19 data.

    Parameters:
        news(bool): If True, a news update will be included in the announcement,
        if False it will not.

        weather(bool): If True, a weather update will be included in the
        announcement, if False it will not.
    Returns:
        None.
    Exceptions:
        An error can occur while using the Flask module in conjunction with the
        pyttsx3 module. One exception to catch this error, log it and then pass.
    Relation to main:
        The user will schedule an alarm for a point in time in the future, and
        will also decide whether they wish for a news update, a weather update
        or both. COVID-19 new deaths and new cases will be included by default.


    The area name will be pulled from the config file and used to retrieve the
    most recent COVID-19 data for the area via get_covid_stats.

    If the user requested news, the current top three news articles will be
    retrieved via get_top_three_articles

    If the user requested weather, a weather report will be retrieved via
    get_weather.

    The data pulled from these three API's will be used to form an announcement
    string with all the neccesary information, which will then be ran by the
    pyttsx3 module to provide an audio announcement.
    """

    engine = pyttsx3.init()

    (date, new_cases_by_publish_date,
    new_deaths_by_death_date) = get_covid_stats(area_name)

    tier_1 = covid_tiers["tier_1"]
    tier_2 = covid_tiers["tier_2"]
    tier_3 = covid_tiers["tier_3"]

    if new_cases_by_publish_date >= tier_1:
        tier = "tier 1"

    if new_cases_by_publish_date >= tier_2:
        tier = "tier 2"

    if new_cases_by_publish_date >= tier_3:
        tier = "tier 3"

    else:
        tier = "tier 0"

    covid_string = f"""As of the following date {date} there has been
    {new_cases_by_publish_date} new cases of corona virus and
    {new_deaths_by_death_date} deaths due to corona virus in your area.
    According to your specified tier boundaries, the current tier for your
    area is {tier}."""

    if news:
        news = True
        top_three_articles = get_top_three_articles(get_notifications(news_api_key))
        news_string = f"""The current top three new stories
        are as folows: {top_three_articles}. """

    if weather:
        weather = True
        (weather_description, temperature_celsius, air_pressure,
        air_humidity) = get_weather(weather_api_key, area_name)
        weather_string = f"""The weather description for your area is
        {weather_description}. The temperature is {temperature_celsius} degrees
        celsius. The air pressure is {air_pressure} millibars and the air
        humidity is {air_humidity}%."""

    if news and weather:
        to_speak = news_string + " " + weather_string + " " + covid_string

    elif news:
        to_speak = news_string + " " + covid_string

    elif weather:
        to_speak = weather_string + " " + covid_string

    else:
        to_speak = covid_string

    to_speak = "Here is your scheduled briefing. " + to_speak

    try:
        engine.endLoop()
    except:
        logging.error("FUNCTION:announcement:PyTTSx3 Endloop error")
    engine.say(to_speak)
    engine.runAndWait()
