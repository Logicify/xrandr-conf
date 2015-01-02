CLI Interface
=============

The core of the *profile-conf* is command line utility which acts as an environment for modules. Typically you just need
to run it without any arguments to find all suitable profiles and apply them, however there is some more capabilities
and configuration options available

Synopsis
--------

```
profile-conf [argumets]
```
Run profile-conf. It will try to find configuration file in default location.
```
profile-conf -h
profile-conf --help
```
Outputs reference information

Arguments
---------

### -l, --list
List all available profiles.
#### Example
```
$> profile-conf -l
TBD
```

### -q, --query
Captures current system state and outputs result in readable form.
This can be very useful for debugging/composing config file
#### Example
```
$> profile-conf -q
TBD
```

### -p, --find-profiles
Detects which profiles could be applied
#### Example
```
$> profile-conf -p
TBD
```

### -a &lt;profile_name&gt; \[-f, --force\], --apply &lt;profile_name&gt; \[-f, --force\]
Applies given profile.
If -f flag is set profile will be applied regardless of conditions, otherwise an error will be returned
  in case when current system state doesn't satisfy conditions of the given profile.
#### Example
```
$> profile-conf -fa InternalDisplayOnly
```

### -c &lt;path_to_config&gt;, --config=&lt;path_to_config&gt;
Sets path of the config file which should be used.
If this option is not set application will try to find config in default locations:
* &lt;HOME_DIR&gt;/.config/profile-conf/config.yaml
* /etc/profile-conf/config.yaml


#### Example
```
$> profile-conf -c ~/profile-conf.yaml
```

### -b &lt;module1\[,module2\]&gt;, --blacklist=&lt;module1\[,module2\]&gt;
Disable given modules. This means that modules will not be loaded during bootstrap so all conditions and actions 
which should be handled by these modules will be ignored. Also system state will not include output of blacklisted modules.
Note: this options has higher priority then respective config section.