# RPI Weather Station

Logging of temperatue data to a google spreadsheet using a DHT22 sensor and a raspberry pi zero w. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Things you need to install on you raspberry pi zero w before setup.

```
sudo apt-get upgrade && sudo apt-get update

sudo apt-get install python-pip

sudo apt-get install build-essential python-dev

sudo pip install --upgrade oauth2client

sudo apt-get install python-openssl

sudo pip install gspread

```

### Installing

A step by step guide

Adafruit libary for DHT 22 and initial test of the sensor

```
 Clone the adafruit python dht library into a folder of your choosing. After this run "sudo python setup.py install" inside the Adafruid_Python_DHT folder.

 git clone https://github.com/adafruit/Adafruit_Python_DHT.git

 To test if the sensor was connected correctly to the raspberry pi we go into the examples folder and run "sudo ./AdafruitDHT.py 22 4" where 22 represents the DHT22 sensor and 4 the gpio where we connected it. 

```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

# this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


