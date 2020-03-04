# rpi_bonnet_dashboard
A network speed indicator for raspberry pi with the adafruit OLED bonnet

## Installation
In order to use the bonnet, first you have to enable the I2C_bus.
A tutorial for it is available [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)


### Software requirements

First, if you don't have it already, you have to install pip3 and git:
```
sudo apt-get update
sudo apt-get install python3-pip git
```
Then install pipenv
```
pip3 install --user pipenv
```
Note: the command above keeps everything into a `~/.local` directory. You can
update the current user's `PATH` by adding the following lines into your
`.bashrc` (or equivalent):

```
export PY_USER_BIN="$(python -c 'import site; print(site.USER_BASE + "/bin")')"
export PATH="$PY_USER_BIN:$PATH"
```
Install some prerequisites for Pillow:

```
sudo apt-get install libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
```

Now clone the repository and jump into the downloaded directory with:
```
git clone https://github.com/EdBuilds/rpi_bonnet_dashboard.git
cd rpi_bonnet_dashboard
```
Install modules from pipfile (this might take a couple of minutes):
```
pipenv install
```
If all the modules were installed without errors, you can now run the application with:
```
pipenv run python3 dashboard.py
```
## Detaching from terminal
There is no service yet for the dashboard, stay tuned for updates.
If you want to run the application from ssh and then close the session without closing the program, you can call:
```
nohup pipenv run python3 dashboard.py > network_speed_log 2>&1 &
```

## To do list

* run speedtest only on button press
* multiple dashboard pages
* Display Pi-hole statistics
* Display system statistics
* switching between dashboards with buttons
* automatic cycling between dashboard pages
* create a systemd service for the dashboard
* create an automatic installer script

