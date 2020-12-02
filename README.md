## README
___

### Introduction

This alarm project offers a way for the user to schedule an alarm update that will provide an announcement containing a variety of information, depending on what the user selects. The user may choose to have a news update, weather update or both in their announcement. By default, the announcement will include an update of new coronavirus cases and new coronavirus deaths for the area that the user specifies. The user may also label their alarms with messages to remind they of what will be announced.

In addition to this, there will a stream of notifications for top news stories on the one side of the user interface. The user can choose how often these notifications are refreshed.
___

### Dependencies

In order to run this package you must have the following.

+ A computer.
+ An internet browser (preferably Google Chrome, Firefox may be incompatible).
+ Python 3.9 or above.
+ A text editor.
+ A working internet connection.
+ A command line to run the package from.
+ A weather API key from http://api.openweathermap.org. Follow the instructions on their website to get a free API key.
+ A news API key from https://newsapi.org. Follow the instructions on their website to get a free API key.
___

### Installation

Run the follow [pip](https://pip.pypa.io/en/stable/) (python package managers) commands to install all the necessary modules.

#### Text to speech module

```
pip install pyttsx3
```
#### Flask moduke

```
pip install Flask
```
#### UK COVID-19 module
```
pip install uk-covid19
```
---
### Getting started tutorial

First of all, ensure you have appropriately carried out the following installations above and you have all the required dependencies to run this package.

Next you will want to navigate to the folder wherever you installed the package, open up the package and load up the file **config.json**. You should see the code below.

```json
{
  "title": "Alarm clock",
  "image": "dog.jpg",
  "area_name": "Swindon",
  "refresh_rate": 5,
  "covid_tiers": {
      "tier_1": 10,
      "tier_2": 20,
      "tier_3": 30
    },
  "api_keys":{
      "news_api_key": "",
      "weather_api_key": ""
    },
  "file_paths":{"log_file": "../Logs/sys.log"}
}
```
The title will be the large, central title displayed in the user interface when
it is loaded. It may be whatever you desire, but it must be entered as a string.

The image will be the icon that appears in the user interface. The image is
set to a picture of a dog by default, but may be changed to an image that will
fit. If you wish to change the image, navigate to the following folder in your
file explorer, as so.

```
alarmproject/modules/static/images
```

You may then paste your image here. Then, in the config file, change the "image" value to the name of your image (including its handle). The name must be a string.

The area name can be set to any any area of your choosing, and this will determine the area for which weather data and COVID-19 data are gathered. The area must be a real place, spelled correctly and must not be an empty string or the code will not run. The area name must be a string.

The refresh rate is the rate at which you could like the news API to be called and check for new top news stories. In the above example, the refresh rate is set to 60 and therefore after every 60 page refreshes the news API will be called. The page will be refreshed automatically every 60 seconds, and any manual refreshes will also count as a refresh. The number must be greater than
0 or the code will not run.

The covid tiers are yours to specify. When the announcement function runs, it
will compare how many new cases of COVID-19 there has been in your area with
the tiers that you specify and work out what tier this makes your area, which
it will then announce to you. So for the example config file above, if there
was to be 24 new cases of COVID-19 in my area, it would announce the current
tier as "tier 2". If this value was to be below tier_1, it would announce
the tier as "tier 0". You should specify each tier as an integer value. For
the function to work as designed, all values should be greater than 0, tier 3
should be greater than tier 2 and tier 2 should be greater than tier 1. All
these conditions must be satisfied or the code will not run.

You should place your news API key and your weather API key in the appropriate places in the config file. If you enter an invalid API key, the program will not run. Where you see the characters "", the api keys should be placed within
these quotation marks.

If the filepath of the log file is changed, the file path section should be updated to accommodate for this. By default, the log file will be in the **logs** folders.

Once you have entered all the necessary information, save the config file and
close it down.

Once you have completed setting up the config file, you should open up the command line and navigate through your file system and open up the project folder. Please note the below is an example and every filesystem will be different.

```
cd Users/User/Downloads/alarmproject
```

Once you have correctly navigated to the project folder, type the following command in the command line.

```
python3 main.py
```

Assuming you set up the config file correctly all all the necessary APIs are functioning as intended, the following message should appear in your command line. This means the server has loaded up successfully.

```
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
```

Navigate to http://127.0.0.1:5000/index in a web browser to get started.

Once you have navigated to the page, the user interface should be fairly self explanatory. You may schedule alarms using the central time and date inputs, choosing a label for the alarm and choosing what content you would like to be included in your announcement. Once an alarm has been scheduled, you should see it appear on the right hand side where may cancel it if you so desire. You can schedule multiple alarms, with every different option. On the right hand side you should also see a stream of top news articles with urls towards the host website, you may also dismiss these article notifications. These notifications will be refreshed as often as you specified in the config file.

You should avoid editing the url request as if you do, the program will catch
it and will not allow you to schedule an alarm. You also should not include
the "&" symbol in your label as this will also prevent you from being able
to schedule an alarm.

---

### Testing the code

The is a module called **test.py** included in the package that can be run in order to ensure all functions are working as is intended. As a more general use, it may show you the intended outcome for a variety of different situations which the functions may encounter. While in the **alarmproject/modules** directory, use the below command to run the tests.

```
python3 test_unit.py
```

If the functions are all working as intended, you should see the following message printed to the console.

```
All tests passed successfully.
```

If one or more functions are not working as intended, you may see an error like the one below printed to the console.

```
Traceback (most recent call last):
  File "/Users/mottmarris/current/alarmproject/test_unit.py", line 227, in <module>
    test_log_alarm()
  File "/Users/mottmarris/current/alarmproject/test_unit.py", line 212, in test_log_alarm
    assert alarm_4_in_log == False
AssertionError
```

You may use this error log as a guide to try and debug the package yourself, or you may report the bug to me.

---

### Author

Matthew Morris

---

### Date published

4/12/2020

---

### License

Copyright (c) 2020 Matthew Morris

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
