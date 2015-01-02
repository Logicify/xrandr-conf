profile-conf
===========

Simple DE independent utility for managing managing different system configurations depending on conditions.

Typical use case
----------------

Let's imagine you have a few different monitor configurations in various locations:

 1. At home you have one monitor connected to HDMI port of your laptop
 1. At the office you have dock station with 2 monitors connected
 1. Also you often need to disconnect all external displays and use just laptop's screen
  
Reconfiguring with ```xrandr``` each time you change location can be really annoying especially if you have more 
then 3 options.

The Idea
--------

Basically all you need is to define how exactly you would like to configure your devices depending on 
_current system state_.
Let's call this **Profile**. Profile contains of 2 parts: conditions which must be satisfied to activate this profile 
and actual system configuration which should be applied when profile is activated. 
profile-conf will find suitable profiles for current system state and apply configuration for each one.

Let's look on the profile-conf configuration file which defines profiles for examples from previous section.

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
  2Monitors:
    when:
      connected: "HDMI1, HDMI2"
    then:
      - configure-displays:
          "*":
            state: "off"
          HDMI1:
            mode: "$preferredResolution"
            position: '0x0'
            primary: true
          HDMI2:
            mode: "$preferredResolution"
            position: 'right-of HDMI1'
            primary: true
```

Usage
-----

1. The first thing you need is config file describing your profiles (Documentation is not available yet, sorry)
2. Run ```profile-conf``` each time you need to change profile or add _udev_ rule to call it automatically.
3. Optionally bind some global keyboard hotkey to run ```profile-conf``` executable. This can be pretty handy.

Disclaimer
----------

This software is in very early stage. Documentation is not ready yet as well as many of the features which should be ready.
However any feedback is more than appreciated.

Credits
-------
Dmitry Berezovsky, Logicify (http://logicify.com/)