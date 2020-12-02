"""This module contains function that are related to acquiring different
pieces of data to be used in other modules, and a function to test their own
functonality.
"""

import logging
import json
import requests
from flask import Markup
from uk_covid19 import Cov19API

def access_config_file() -> tuple[str, str, str, str]:
    """Retrieves all stored information from the config file and returns it."""

    with open("config.json", "r") as config_file:
        config_file = json.load(config_file)
        area_name = config_file["area_name"]
        api_keys = config_file["api_keys"]
        news_api_key = api_keys["news_api_key"]
        weather_api_key = api_keys["weather_api_key"]
        filepaths = config_file["file_paths"]
        logfilepath = filepaths["log_file"]
        refresh_rate = config_file["refresh_rate"]
        covid_tiers = config_file["covid_tiers"]

    return (area_name, news_api_key, weather_api_key, logfilepath,
    refresh_rate, covid_tiers)




log_filepath = access_config_file()[3]

logging.basicConfig(filename=log_filepath, encoding='utf-8', level=logging.DEBUG)




def get_covid_stats(area_name: str) -> tuple[str, int, int]:
    """Calls the Cov19API for the selected area and returns relevant data.

    Parameters:
        area_name(str): Specified in the config file. The Cov19API will
        retrieve COVID-19 data for this area.
    Returns:
        The date of the information.
        The number of new COVID-19 cases for the area.
        The number of new COVID-19 deaths for the area.
        If either of the previous two values are 'None', they will be changed
        to str(0) and returned.
    Exceptions:
        If an empty string is passed as an argument for area name, the function
        will log the error and return None.

        If the "length" value in the data dictionary is 0, either an invalid
        area name has been passed or the API has failed. The error will be
        logged and return None.
    Relation to __main__:
        Not directly used in __main__ but used by the annoucement module to
        retrieve all the neccesary information to give a text to speech
        annoucement.
    """
    if not area_name:
        logging.warning("API FAILURE:COVID API:Empty string.")
        return None

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate"
    }

    api = Cov19API(filters=["areaName=" + area_name.title()], structure=cases_and_deaths)
    data = api.get_json()

    if data["length"] == 0:
        logging.warning("API FAILURE:COVID API:Invalid area name or broken API")
        return None

    current_data = data["data"][0]

    date = current_data["date"]
    new_cases_by_publish_date = current_data["newCasesByPublishDate"]
    new_deaths_by_death_date = current_data["newDeathsByDeathDate"]

    if new_deaths_by_death_date is None:
        new_deaths_by_death_date = "0"
    if new_cases_by_publish_date is None:
        new_cases_by_publish_date = "0"

    return date, new_cases_by_publish_date, new_deaths_by_death_date




def get_weather(weather_api_key: str,
area_name: str) ->tuple[str, str, str, str]:
    """Calls the weather API for the area and returns the relevant data.

    Parameters:
        weather_api_key(str): API key that can be pulled from the config file
        and used to call the openweathermap API.
        area_name(str): Also pulled from the config file. Weather data will be
        collected for this area.
    Returns:
        A description of the weather, the current temperate in celsius,
        the air pressure in millibars and the % air humidity.
    Exceptions:
        If the "404" value in the dictionary is 404, then most likely an
        invalid area name has been added. The area will be logged and None
        will be returned.

        If the function encounters a key error due to an empty dictionary, this
        is most likely due to an empty string being used as an area name, an
        invalid API key being used or the API being down. The error will be
        logged and None will be returned.
    Relation to __main__:
        Not directly used in __main__ but used by the annoucement module to
        retrieve all the neccesary information to give a text to speech
        annoucement.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = (base_url + "appid=" + weather_api_key + "&q="
    + area_name.title())
    response = requests.get(complete_url)
    weather_dict = response.json()

    if weather_dict["cod"] == "404":
        logging.warning("API FAILURE:WEATHER API:Invalid area name")
        return None

    try:
        weather_description = weather_dict["weather"][0]["description"]
        temperature_kelvin = weather_dict["main"]["temp"]
        temperature_celsius = str(int(int(temperature_kelvin) - 273.15))
        air_pressure = str(weather_dict["main"]["pressure"])
        air_humidity = str(weather_dict["main"]["humidity"])
    except KeyError:
        logging.warning("""API FAILURE:WEATHER API:Maybe empty string, invalid
        API key or broken API.""")
        return None

    return weather_description, temperature_celsius, air_pressure, air_humidity




def get_notifications(news_api_key: str) -> list[dict]:
    """Call the news API and returns a list of current top news stories.

    Parameters:
        news_api_key(str): API that can be pulled from the config file and
        used to call the newsapi API.
    Returns:
        A list of dictionaries, each one corresponding to a top news article
        with a title and a url link to the article.
    Exceptions:
        No stated exceptions with the function. It will be tested by the
        test_getters function defined below.
    Relation to __main__:
        Called in the user_interface module to retrieve the top news stories,
        with the list then being passed into the template and the elements
        within each dictionary being displayed to the user.
    """

    base_url = "https://newsapi.org/v2/top-headlines?"
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + news_api_key
    response = requests.get(complete_url)
    news_dict = response.json()
    articles = news_dict["articles"]

    article_with_url = []

    for article in articles:
        html_start = "<a href="
        html_middle = ">"
        html_end = "</a>"
        article_dict = {}
        article_dict["title"] = article["title"]
        url = article["url"]
        url_with_html = Markup(html_start + url + html_middle + url + html_end)
        article_dict["content"] = url_with_html

        article_with_url.append(article_dict)

    logging.info("""FUNCTION:get_notifications:Notifications retrieved
    succesfully""")

    return article_with_url




def get_top_three_articles(articles: list[dict]) -> list[str]:
    """Takes a list of articles and returns the top three, if possible.

    Parameters:
        articles(list[dict]): A list of articles, each article as a dictionary.
    Returns:
        Parses the list and retrieves the value of "title" for the top three
        articles.

        If there is three or more articles in the list, it returns a list of
        three article titles.

        If there is less than three articles in the list, returns a list of
        article titles equal to the number of articles in the original list.

        If there is no articles in the list to parse, return None.
    Exceptions:
        No stated exceptions.
    Relation to main:
        Not directly called in the main module, but will be called when an
        annoucement is triggered with the news parameter checked. Will allow
        the annoucement to then convert the top three articles into a text
        to speech annoucement.
    """

    article_titles = []

    number_of_articles = len(articles)

    if number_of_articles >= 3:
        for article in articles[:3]:
            article_titles.append(article["title"])
        return article_titles

    if number_of_articles > 0:
        for article in articles:
            article_titles.append(article["title"])
        return article_titles

    logging.warning("""FUNCTION FAILURE:get_top_three_articles:No articles to
    parse.""")
    return None




def test_apis(area_name: str, news_api_key: str, weather_api_key: str) -> bool:
    """Test all the fuctions that make API calls to ensure they are working.

    Parameters:
        area_name(str): The area name specified in the config file.

        news_api_key(str): API that can be pulled from the config file and
        used to call the newsapi API.

        weather_api_key(str): API key that can be pulled from the config file
        and used to call the openweathermap API.
    Returns:
        If get_covid_stats or get_weather return None, the function will return
        False as this indicates the APIs are not functioning correctly.

        If the length of the list that get_notifications returns is 0,
        the function will return False as this indicates the API is not
        functioning correctly.

        All instances of an API not working will be logged.

        Returns True if the APIs return the values they should.
    Exceptions:
        No stated exceptions.
    Relation to main:
        When the main module is run, this is the first function that will be
        called. If it returns True, the rest of the code will run. If it
        returns False, the main module will not run.
    """

    api_failure = False

    if get_covid_stats(area_name) is None:
        logging.warning("API FAILURE:COVID API.")
        api_failure = True
    if get_weather(weather_api_key, area_name) is None:
        logging.warning("API FAILURE: Weather API.")
        api_failure = True
    if len(get_notifications(news_api_key)) == 0:
        logging.warning("API FAILURE: News API.")
        api_failure = True

    if api_failure:
        return False

    logging.info("FUNCTION:test_getters:All APIs working")
    return True
