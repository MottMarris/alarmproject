"""This module contains functions that handle notification cancellations and
a module that checks the validity of an alarm url request.
"""

import logging
from getters import access_config_file

log_filepath = access_config_file()[3]


logging.basicConfig(filename=log_filepath, encoding='utf-8',
level=logging.DEBUG)

def cancel_notification(notifications: list[dict],
cancelled_notifications: list[dict], notification_to_cancel: str) -> dict:
    """Finds the notification to cancel in the list of notifications.

    Parameters:
        notifications(list[dict]): A list of notifications, which are in
        dictionary format.

        cancelled_notifications(list[dict]): A list of notifications that have
        been cancelled by the user, also in dictionary format.

        notification_to_cancel(str): The name of the notification that the user
        wishes to cancel.
    Returns:
        Parses the dictionary to to find the notification that has been
        cancelled by the user, comparing the dictionaries "title" value with the
        value of "notification_to_cancel". If it is found, and the notification
        is not already in cancel_notifications, it will return the dictionary.

        If the notification is not found, it will return None.
    Exceptions:
        No stated exceptions.
    Relation to main:
        When the user cancels a notification in the user interface, the main
        module will receive this notification in the form of a url request.
        The url request will be the name of the notification. This function
        then returns the correspoding notification dictionary from the
        notifications data structure. The notification will then be appended
        to the list of cancelled notifications and hence wont be shown to
        the user again, unless the program is restarted.
    """

    for notification in notifications:
        if (notification["title"] == notification_to_cancel and
        notification not in cancelled_notifications):
            logging.info("FUNCTION:cancel_notification: cancelled notification="
            + notification_to_cancel + " - cancelled")
            return notification

    logging.info("FUNCTION:cancel_notification: cancelled notification="
    + notification_to_cancel + "not in notifications")
    return None


def dismiss_cancelled_notifications(notifications: list[dict],
cancelled_notifications: list[dict]):
    """Remove the cancelled notifications from the notifications data structure.

    Parameters:
        notifications(list[dict]): A list of notifications, which are in
        dictionary format.

        cancelled_notifications(list[dict]): A list of notifications that have
        been cancelled by the user, also in dictionary format.
    Returns:
        If the length of the cancelled notifications list is 0, the function
        will just return the list of notifications as there is nothing to
        cancel.

        Otherwise it will parse the list of notifications, checking if the
        notification is in the list of cancelled notifications. If it is,
        it will remove the notification from the list of the notifications.
        Once every notification has been checked, it will return the new list
        of notifications.
    Exceptions:
        No stated exceptions.
    Relation to main:
        This function will be called every time the page refreshes to remove
        the notifications that the user has cancelled from the notifications
        data structure.
    """

    if len(cancelled_notifications) == 0:
        logging.info("""FUNCTION:dismiss_cancelled_notifications:No
        notifications to cancel""")
        return notifications

    for i in range(len(notifications)):
        for notification in notifications:
            if notification in cancelled_notifications:
                notifications.remove(notification)

    logging.info("""FUNCTION:dismiss_cancelled_notifications:Notifications
    dismissed succesfully""")
    return notifications

def check_alarm_url_request(url_request):
    """
    """

    if not url_request:
        return url_request

    if len(url_request) != 16:
        logging.warning("URL REQUEST FAILURE: Url manually edited")
        return False

    if url_request[4] != "-" or url_request[7] != "-":
        logging.warning("URL REQUEST FAILURE: Url manually edited")
        return False

    if url_request[10] != "T" or url_request[13] != ":":
        logging.warning("URL REQUEST FAILURE: Url manually edited")
        return False

    try:
        int(url_request[:4])
        int(url_request[5:7])
        int(url_request[8:10])
        int(url_request[11:13])
        int(url_request[14:])

    except ValueError:
        logging.warning("URL REQUEST FAILURE: Url manually edited")
        return False

    return True

def config_file_checker(refresh_rate, covid_tiers, area_name):

    tier_1 = covid_tiers["tier_1"]
    tier_2 = covid_tiers["tier_2"]
    tier_3 = covid_tiers["tier_3"]

    if not isinstance(area_name, str) or not isinstance(refresh_rate, int):
        return False

    if not isinstance(tier_1, int) or not isinstance(tier_2, int):
        return False

    if not isinstance(tier_3, int):
        return False

    if refresh_rate <= 0 or tier_1 <= 0:
        return False

    if tier_2 <= 0 or tier_3 <= 0:
        return False

    if tier_1 >= tier_2 or tier_1 >= tier_3:
        return False

    if tier_2 >= tier_3:
        return False

    return True
