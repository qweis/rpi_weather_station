#!/usr/bin/python


# Depends on the 'gspread' and 'oauth2client' package being installed.  If you
# sudo pip install gspread oauth2client

# Also it's _very important_ on the Raspberry Pi to install the python-openssl
# package because the version of Python is a bit old and can fail with Google's
# new OAuth2 based authentication.  Run the following command to install the
# the package:
#   sudo apt-get update
#   sudo apt-get install python-openssl

import json
import sys
import time
import datetime
import os.path
import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Type of sensor, can be DHT11, DHT22, or AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Sensor connected to Raspberry Pi pin 4
DHT_PIN  = 4

# Display Variables
displaySensorName = ""
displayTempValue = ""
a=u""

# Google Docs OAuth credential JSON file.  Note that the process for authenticating
# with Google docs has changed as of ~April 2015.  You _must_ use OAuth2 to log
# in and authenticate with the gspread library.  Unfortunately this process is much
# more complicated than the old process.  You _must_ carefully follow the steps on
# this page to create a new OAuth service in your Google developer console:
#   http://gspread.readthedocs.org/en/latest/oauth2.html
#
# Once you've followed the steps above you should have downloaded a .json file with
# your OAuth2 credentials.  This file has a name like SpreadsheetData-<gibberish>.json.
# Place that file in the same directory as this python script.
#
# Now one last _very important_ step before updating the spreadsheet will work.
# Go to your spreadsheet in Google Spreadsheet and share it to the email address
# inside the 'client_email' setting in the SpreadsheetData-*.json file.  For example
# if the client_email setting inside the .json file has an email address like:
#   149345334675-md0qff5f0kib41meu20f7d1habos3qcu@developer.gserviceaccount.com
# Then use the File -> Share... command in the spreadsheet to share it with read
# and write acess to the email address above.  If you don't do this step then the
# updates to the sheet will fail!

# dir_name = '/home/pi/Documents/temperatureMonitor/script/'
# base_filename = 'Rpi\ Weather\ Station-db392df02ad3'
# filename_suffix = 'json'

# Google OAUTH JSON File
GDOCS_OAUTH_JSON       = 'Rpi Weather Station-db392df02ad3.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'WeatherData94402'

# How long to wait (in seconds)
FREQUENCY_SECONDS      = 60


def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open(spreadsheet)
	worksheet = sh.worksheet("Inside")
        return worksheet
	worksheet1 = sh.worksheet("Outside")
	return worksheet1
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

# Set up Display
RST =24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=1)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = 2
shape_width = 20
top = padding
bottom = height-padding
x = padding
font = ImageFont.load_default()
draw.text((x, top+25), 'Booting up Skynet', font=font, fill=255)
disp.image(image)
disp.display()


print('Logging one sensor measurements to {0}.'.format(GDOCS_SPREADSHEET_NAME))
print('Press Ctrl-C to quit.')


def main ():

    # Attempt to get sensor reading.
    humidity, temp_c = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp_c is None:
        time.sleep(2)

    # Conversion and rounding
    temp_c_round = '%6.2f' % temp_c
    temp_c = round(temp_c)
    temp_f = temp_c *9/5.0 + 32
    temp_f_round = '%6.2f' % temp_f
   # print(temp_f)
   # print(temp_f_round)

    # Print Temperature on Display
    displaySensorName ="DHT22 Sensor :"
    displayTempValue = temp_f_round + " " + a + "F" 
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), displaySensorName , font=font, fill=255)
    draw.text((x, top+20), displayTempValue, font=font, fill=255)
    draw.line((x, top+45, x+width, top+45), fill=255)
    disp.image(image)
    disp.display()

    # Print Temperature to Terminal if run in forground
    print('Temperature: {0:0.1f} C'.format(temp_c))
    print('Temperature: {0:0.1f} F'.format(temp_f))
    #print('Humidity:    {0:0.1f} %'.format(humidity))

    # Login to GDOCS if necessary.
    worksheet = None
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Append the data in the spreadsheet, including a timestamp
    try:
        worksheet.append_row((datetime.datetime.now(), temp_c_round))
	val = worksheet.acell('B2').value
    except:
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
	
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    print(val)

if __name__ == "__main__":
    main()

