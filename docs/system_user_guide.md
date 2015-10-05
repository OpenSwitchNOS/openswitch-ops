System
======

[TOC]

## Overview <a id="systemoverview"></a>##
This guide provides detail for managing and monitoring platform componants on the switch. All the configuration commands work in configure context.
Some of the physical components of the switch can be
Fans
Temperature sensors
Power supply modules
LED
This feature lets the user configure fan speed, LED state.

### Setting up the basic configuration <a id="systembasic"></a>

1. ++Setting the fan speed++
'fan-speed *(slow  medium | fast | max )*' lets the user configure the fans to operate at specified speed . By default all the fans operate at normal speed and will change according to the temperature of the system.
```
switch# configure terminal
switch(config)# fan-speed slow
switch(config)#
```

2. ++Setting LED state++
'led *led-name* *(on | off | flashing)*' lets the user to set the state of the LED . By default all the LEDs will be in off state.
User should know the name of the LED of whose state is to be set.
In the example below *'base-loc'* LED is set to *on*.
```
switch# configure terminal
switch(config)# led base-loc on
switch(config)#
```

### Verifying the configuration <a id="systemverify"></a>
1. ++View fan information++
'show system fan' command displays the detailed information of fans in the system.
```
switch#show system fan
Fan information
...............................................................
Name     Speed  Direction      Status        RPM
...............................................................
base-2R  slow  front-to-back  ok            5700
base-5L  slow  front-to-back  ok            6600
base-3L  slow  front-to-back  ok            6600
base-4L  slow  front-to-back  ok            6600
base-5R  slow  front-to-back  ok            5700
base-2L  slow  front-to-back  ok            6650
base-3R  slow  front-to-back  ok            5700
base-1R  slow  front-to-back  ok            5750
base-1L  slow  front-to-back  ok            6700
base-4R  slow  front-to-back  ok            5700
..............................................................
Fan speed override is set to : slow
..............................................................
```
2. ++View LED information++
'show system led' command displays LED information.
```
switch#sh system led
Name           State     Status
.....................................
base-loc       on       ok
```

3. ++View power-supply information++
'show system power-supply' command displays detailed power supply information.
```
switch#sh system power-supply
Name           Status
............................
base-1         ok
base-2         Input Fault
```

4. ++View temperature sensor information++
'show system temperature' command displays temperature sensor information.
```
switch#sh system temperature
Temperature information
....................................................
            Current
Name     temperature    Status         Fan state
            (in C)
....................................................
base-1    22.00          normal         normal
base-3    18.50          normal         normal
base-2    20.50          normal         normal
```

## CLI <a id="systemcli"></a>##
<!--Provide a link to the CLI command related to the feature. The CLI files will be generated to a CLI directory.  -->
Click [here](https://openswitch.net/cli_feature_name.html#cli_command_anchor) for the CLI commands related to the system.
