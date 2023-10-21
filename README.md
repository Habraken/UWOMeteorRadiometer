# UWOMeteorRadiometer

Only supports Python 3, Python 2 not supported. Note: For now, it seems it doesn't work with Pi OS 'Bullseye' nor 'Bookworm', so we are stuck with Buster. Please check the wiki for more info.

The steps below are tested on 2021-05-07-raspios-buster-armhf.zip, downloaded from here: [link](https://downloads.raspberrypi.com/raspios_armhf/images/raspios_armhf-2021-05-28/)

As we want to operate the meteor radiometer in complete darkness you may want to disable both the PWR and ACT LEDs of the Raspebbery Pi permanently:

add the following to ```/boot/config.txt```:
```
# Disable the ACT LED.
dtparam=act_led_trigger=none
dtparam=act_led_activelow=off

# Disable the PWR LED.
dtparam=pwr_led_trigger=default-on
dtparam=pwr_led_activelow=off
```
Note: The method for disabling the power LED was updated following a firmware change that fixed a pwr_led_trigger setting on the Pi 3B+ and 4; see this [GitHub issue](https://github.com/raspberrypi/firmware/issues/1742) for details.



## Installation

First, always start with updating and upgrading the pi OS.
```
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

Next,you will need to install the BCM2835 library from the Waveshare website, which is used the by ADC: [BCM2835](http://www.airspayce.com/mikem/bcm2835/bcm2835-1.73.tar.gz).
This is a C library for Raspberry Pi (RPi). It provides access to GPIO and other IO functions on the Broadcom BCM 2835 chip, as used in the RaspberryPi, allowing access to the GPIO pins on the 26 pin IDE plug on the RPi board so you can control and interface with various external devices.

It provides functions for reading digital inputs and setting digital outputs, using SPI and I2C, and for accessing the system timers. Pin event detection is supported by polling (interrupts are not supported).

Works on all versions up to and including RPI 4. Works with all versions of Debian up to and including Debian Buster 10. Reported to be working on Bullseye (Raspbian v11)

This is a link to the page with more information: [link](http://www.airspayce.com/mikem/bcm2835/). To download the library:

```
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.73.tar.gz
```

Unzip it and follow the instructions in the 'INSTALL' file that should be present in the extracted directory. It's a very basic .configure, make, make install procedure. After these steps reboot the raspberry pi.
```
tar zxvf bcm2835-1.73.tar.gz 
cd bcm2835-1.73
sudo ./configure && sudo make && sudo make check && sudo make install
sudo reboot now
```

Next, clone the UWOMeteorRadiometer repository.
```
git clone https://github.com/Habraken/UWOMeteorRadiometer
```

Next, in the UWOMeterRadiometer directory run the ```sudo ./python3_radiometer_installation.sh``` script to install all required packages. This will take a while. (Espesscialy if numpy needs to be compiled!)

> If the above script fails with this error: ```AttributeError: module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'``` you may need to update pip to latest version.     See this [link](https://askubuntu.com/questions/1428181/module-lib-has-no-attribute-x509-v-flag-cb-issuer-check/1433089#1433089) for more information.
>> - Delete old version:
>> ```
>> sudo apt remove python3-pip 
>> ```
>> - Based on the pip Install guide, do the following:
>> ```
>> wget https://bootstrap.pypa.io/get-pip.py
>> sudo python3 get-pip.py
>> ```
> When the uograde of pip was succesful you can re-run the ```python_radiometer_installation.sh``` script again.

Then in the UWOMeteorRadiometer folder run:
```
sudo python3 setup.py install
```
as the final step of the installation process.


## Initial setup and recording

After installation, run the radiometer record script:
```
sudo python3 RadiometerRun.py
```
use ```--help```for options.

Sudo privileges are required by the BCM2835 library and there is no way around them.

After the first run the script will tell you that a config file is needed, otherwise upon a second run a default config file will be created. If you don't have a config file, run the script again and it will be created under ~/RadiometerData/config.txt.

Then edit the station code in the config file and the geo coordinates of the radiometer, and the instrument string (i.e. the description of the station).
Then you can run the record script and it will handle the recording automatically.


## Live view

It is also possible to view the signal from the radiometer directly by running:
```
sudo python3 RadiometerLiveView.py
```

This will show an oscilloscope-like window on the screen. You can scroll the mouse inside the window to zoom in the X axis, and press 'A' to automatically scale the Y axis.


## Viewing recorded data

All raw data is stored under ~/RadiometerData/CapturedData as binary RMD files. At the end of every night data is compressed and stored under ArchivedData. Futhermore, 2 plots are generated: a NightPlot file which shows average and maximum levels recorded by the radiometer is a 1 second time interval, and a MaxMinus plot which shows the difference between the maximum level and the average of the neighbouring average levels: max_i - (avg_(i - 1) + avg_(i + 1))/2.
If server upload is configured, data will be uploaded to the server at the end of every night.

The viewing script is not designed to view the RDM files directly, but to query a specific time and the viewing script will extect, join and cut appropriate RDM files and show the signal on the screen.

For example, if there was an event on July 22 2018 at 02:35:21 UTC, and we want to view data from station CA0001 channel A in a 100 second time interval, we would run:
```
python3 AnalyzeData.py CA0001 A 20180722-023521 100
```
