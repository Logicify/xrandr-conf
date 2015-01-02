XRandr Module
=============

This modules provides interface to xrandr tool. It allows to change display settings and layout.
The most common use case is to set monitors layout depending on currently connected devices.

Usage example
-------------
```yaml
profiles:
 SingleExternalMonitor:
    name: "External monitor"
    when:
      connected: "$only(eDP1, HDMI1)"
    then:
      - configure-displays:
          "*":
            state: "off"
          HDMI1:
            mode: '$preferredResolution'
  InternalDisplayOnly:
    when:
      connected: "$only(eDP1)"
    then:
      - configure-displays:
          "*":
            state: "off"
          eDP1:
            mode: "$preferredResolution"
            position: '0x0'
            primary: true
```

In this snippet we defined 2 profiles which will be enabled depending on currently connected displays.
In case when there are **ONLY** eDP1 and HDMI1 are connected we turn off all displays except of HDMI1 which will be
configured to run the max possible resolution.
In case when nothing but eDP1 is connected - just ensure that eDP1 is enabled and runs the best resolution.

Provided conditions
-------------------

### connected
Returns **True** if listed devices are currently connected.
It expects to get [RestrictedList](../context.md#RestrictedList) of the devices to search for.  
####Examples
```connected: "HDMI1, DP1"``` or ```connected: "$all(HDMI1, DP1)"```
This will be true in case if both of HDM1 and DP1 are connected, it is possible that some other devices connected as well.

```connected: "$only(HDMI1, DP1)"```
Similar to the previous one, but it performs _exclusive_ match, which means that ONLY listed devices should be connected.

```connected: "$oneof(HDMI1, DP1)"```
Returns true if any of the listed devices is connected.

Provided executors
-------------------

### configure-displays
This executor allows to set options for each of the currently connected displays.

TBD

System state
------------

TBD