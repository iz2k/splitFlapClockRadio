# splitFlapClockRadio

>---
**Table of contents**
- [DIY brief](#diy-brief)
- [3D design](#3d-design)
  * [SplitFlapDigit](#splitflapdigit)
  * [Cover](#cover)
- [Electronics hardware](#electronics-hardware)
- [SplitFlap controller firmware](#splitflap-controller-firmware)
- [Main Control Software](#main-control-software)
  * [Python backend](#python-backend)
  * [Angular Frontend](#angular-frontend)
    + [Dashboard](#dashboard)
    + [Clock](#clock)
    + [Radio](#radio)
    + [Spotify](#spotify)
    + [Sensors](#sensors)
    + [Weather](#weather)
    + [Historic](#historic)
---

The splitFlapClockRadio is an old stylish, classic alarm clock with up to date features, such as automatic time adjustment, weather forecast, air quality sensors, FM radio or Spotify playback. This is an updated version of the [Flip-Clock](https://github.com/iz2k/flip-clock), with slight modifications on the split-flap mechanics and integrated electronics. This device has been designed for DIY hobbists and can be manufactured for 100$ BOM.

| Outside | Inside |
|--------|--------|
|![IMG_20210209_083904](https://user-images.githubusercontent.com/57298545/107334415-f90e7b00-6ab6-11eb-870c-04272cc194e6.jpg)|![IMG_20210208_174947 - copia](https://user-images.githubusercontent.com/57298545/107334590-307d2780-6ab7-11eb-8268-aec639bd62d2.jpg)|

The splitFlapClockRadio features the following characteristics:
- Local time and weather on 3D printed split-flaps.
- 2W I2S Class-D Stereo Amplifier
- FM radio
- Spotify
- Air Quality measurements (eCO2 and TVOC)
- 32 x RGB LED array light
- Spoken weather forecasts (openWeatherMap + TTS)
- Volume and Media control rotary encoder wheels
- Powered by a Raspberry Pi 3A+

The project is divided in four main sections: 3D design, electronics hardware design, split-flap controller MCU firmware (C++) and main software (Python backend + Angular frontend).

## DIY brief
- [ ] Print 3D parts
- [ ] Manufacture PCB (<20$ with [JLCPB](https://jlcpcb.com/))
- [ ] Populate PCB with [Hot Air Gun](https://satkit.com/es/aoyue-int738-sistema-de-reparacion-profesional-soldador-60w)
- [ ] Flash MSP430 MCU
- [ ] Set-up fresh RaspberryPiOS Lite SD card ([tutorial](https://www.raspberrypi.org/software/))
- [ ] Install splitFlapClockRadio barebone:
`wget -O - https://raw.githubusercontent.com/iz2k/splitFlapClockRadio/master/sw/shInstall/barebone.sh | bash `
- [ ] Reboot and enjoy!

## 3D design

### SplitFlapDigit

Each split-flap digit consists of a support structure with two bearings. The axle is placed inside the bearings holding two flap holders. All the flaps are mounted within those holders. The movement of the digit is achieved with a stepper motor and two gears. A reflective IR sensor is used to detect falling flaps, and a hall sensor to synchronize the absolute position of the drum.
![image](https://user-images.githubusercontent.com/57298545/107249527-beafca00-6a33-11eb-8ed1-5991706c14ce.png)

In order to get numbers and weather icons painted into the flaps, custom stencils have been designed and printed. The stencil design is avaiable at [iz2k/splitFlap-stencil](https://github.com/iz2k/splitFlap-stencil) repository.
![stencil](https://github.com/iz2k/splitFlap-stencil/raw/master/_img/palce-in-base.jpg)

### Cover
The cover consist on 3 main parts and 2 control wheels:
- Floor
- Top cover
- Frontal
- Volume wheel
- Media wheel
![image](https://user-images.githubusercontent.com/57298545/107335295-0d9f4300-6ab8-11eb-85b8-67c0990727da.png)


| Front Right |
|--------|
|![IMG_20210209_083859](https://user-images.githubusercontent.com/57298545/107334414-f875e480-6ab6-11eb-9e04-c3190adce9fc.jpg)|

| Front Left |
|--------|
|![IMG_20210209_083912](https://user-images.githubusercontent.com/57298545/107334416-f90e7b00-6ab6-11eb-81c4-429d74a9faec.jpg)|

| Rear |
|--------|
|![IMG_20210209_083929](https://user-images.githubusercontent.com/57298545/107334412-f7dd4e00-6ab6-11eb-9475-58213e905a96.jpg)|

## Electronics hardware
The electronics hardware integrates the following components:
- AC/DC converter
- MSP430FR2476 MCU as splitFlap controller
- 3 x ULN2003 stepper driver
- 3 x OPB733 reflective IR sensor
- 3 x DRV5055 hall sensor
- 1 x Si4731 FM radio tuner
- 2 x MAX98357 I2S audio amplifier (stereo)
- 32 x WS2812-2020 RGB LED
- Air Quality sensors: 1 x BME680 + 1 x SGP30/SGP40

![splitFlapClockRadio_3D_Image](https://user-images.githubusercontent.com/57298545/107251257-6f1dce00-6a34-11eb-9b59-c8c990091193.png)
## SplitFlap controller firmware

The firmware runs on a MSP430 MCU and controls the driver of the three integrated stepper motors. The firmware keeps track of the falling flaps based on the reflected IR detector and synchronizes every cycle based on a hall efect sensor. The MCU can be commanded through I2C bus using SMBUS commands.

## Main Control Software
Tha main functionality of the clock is controlled by the Python backend. It controlls all the peripherals and makes the system work upon user interface with the rotary encoders or the orders triggered through the frontend.

The frontend is an Angular application that allows checking and modifying the current status and configuration of the system. It is accesible withtin the WLAN through a web browser ponting to the configured hostname of the Raspberry Pi.

### Python backend
The backend is divided in different packages to control specific peripherals of the systems:
- Alarm: controls activation of the configured alarms.
- Audio: controls the alsa sound system to trigger sounds and control volume.
- Clock: controls the split-flap controller via SMBUS.
- Config: controls the configuration file.
- DB: interfaces a MariaDB database to log periodic weather and Air Quality data.
- OsInfo: passes current OS infor to the frontend.
- RadioTuner: controls the integrated Si4731 FM tuner IC
- RgbStrip: controls the WS2812 RGB LED strip.
- SpotifyPlayer: activates raspotify device and controls the playback of spotify via spotify-cli.
- UserInterface: controls the Volume and Media rotary encoders.
- WeatherStation: gets weather information through OpenWeatherMap API and controls Air Quality sensors.
- WebServer: integrated Flask webserver to connect with the frontend via REST requests and/or websockets.

The backend is by default installed as a system service (autostart enabled), but can be stopped and launched manually to check its output.
``` bash
sudo service splitFlapClockRadioBackend stop
sudo splitFlapClockRadioBackend
```
![image](https://user-images.githubusercontent.com/57298545/107243714-945b0e00-6a2d-11eb-862e-01a95cedf969.png)

### Angular Frontend
The frontend is also divided in different modules:
#### Dashboard
- Quik view of current status
![image](https://user-images.githubusercontent.com/57298545/107244658-8e196180-6a2e-11eb-89ed-aa831ceeba2d.png)

#### Clock
- Current time and alarm list
![image](https://user-images.githubusercontent.com/57298545/107245531-89a17880-6a2f-11eb-8e75-ae096139154d.png)
- SplitFlap calibration
![image](https://user-images.githubusercontent.com/57298545/107338725-2c9fd400-6abc-11eb-9cd0-a662c4163d8c.png)
- Alarm configuration
![image](https://user-images.githubusercontent.com/57298545/107338887-59ec8200-6abc-11eb-8fb1-2cb28ecb5442.png)

#### Radio
- FM radio tuner control and stored station list.
![image](https://user-images.githubusercontent.com/57298545/107244930-ddf82880-6a2e-11eb-8b59-517c98c929c2.png)

#### Spotify
- Playback control and stored media item list
![image](https://user-images.githubusercontent.com/57298545/107339397-f020a800-6abc-11eb-84e3-ada73b83d36d.png)
- Authentication
![image](https://user-images.githubusercontent.com/57298545/107339695-4392f600-6abd-11eb-972d-0bc9fde1fe30.png)
- Music search
![image](https://user-images.githubusercontent.com/57298545/107339561-1c3c2900-6abd-11eb-8ac3-34a389041a2f.png)

#### Sensors
- Air Quality sensor data and calibration.
![image](https://user-images.githubusercontent.com/57298545/107339919-7fc65680-6abd-11eb-860f-ada6bd95d3f1.png)

#### Weather
- Weather data, location configuration and API keys.
![image](https://user-images.githubusercontent.com/57298545/107245825-e309a780-6a2f-11eb-8f45-2ad97b1a4df5.png)

#### Historic
- Logged weather and Air Quality data
![image](https://user-images.githubusercontent.com/57298545/107340168-bb612080-6abd-11eb-91b9-05b793ba30bc.png)