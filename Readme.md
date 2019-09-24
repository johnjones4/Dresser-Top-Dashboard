# EDashboard

This is a project that displays a simple personal dashboard as an image. It is intended to be used with a hardware build detailed here.

## Requirements

* Python3
* PIP

## Setup

Execute the following to download the project and install the dependencies.

```bash
# git clone git@github.com:johnjones4/e-dashboard.git
# cd e-dashboard
# make setup
```

Setup installs all of the Python dependencies via pip, a copy of Open Sans for text rendering, and, if Make detects a Linux system and thus assumes its on a Raspberry Pi, installs the dependencies to communicate with the E-Ink display detailed _here_. The setup step also creates a file named `config.yaml` which declares a number of details that this code needs to run properly. Within `config.sample.yaml` file are details about what the various variables control.

## Running

To run the project, execute the following:

```bash
# make display
```

It will run the Python code which will generate a file named `/tmp/dashboard.bmp`. If on a Mac, Make will then open the BMP file in Preview. If on Linux, Make assumes its a Raspberry Pi and executes code to display the BMP file on an E-Ink display.

## Installing on a Raspberry Pi

The setup steps on a Raspberry pi are exactly the same as above, but to make sure the code runs on a regular basis to keep the display updated, it's necessary to setup a cron job. To do so, first open your crontab file by running:

```bash
# crontab -e
```

Within the file, add the following line:

```
*/2 * * * * cd /home/pi/e-dashboard && make display 2>&1 | /usr/bin/logger -r e-dashboard
```
