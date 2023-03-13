# e-soh-wis2box-demo

### Instructions for running

The wis2box KNMI configuration is set up based on
https://docs.wis2box.wis.wmo.int/en/latest/user/setup.html#.

The configuration files can be found in the `knmi-config` directory.
The `WIS2BOX_HOST_DATADIR` variable in the `dev.env` file should
point to the (absolute) directory where the other config files can be found.

A month of KNMI BUFR files can be found in the `knmi-data` directory.

Now follow the following steps to setup the system and load the data.
* Check out main branch from https://github.com/wmo-im/wis2box

* Put the `dev.env` file from the `e-soh-wis2box-demo` project in the wis2box main project directory.

* Run commands (these are just wrappers for docker compose):
```
python3 wis2box-ctl.py build
python3 wis2box-ctl.py update
python3 wis2box-ctl.py start
python3 wis2box-ctl.py login
```

* From the container, run:
```
wis2box data add-collection $WIS2BOX_DATADIR/surface-weather-observations.yml
wis2box metadata discovery publish $WIS2BOX_DATADIR/surface-weather-observations.yml
# Does this do anything if there is no data yet?
wis2box metadata station publish-collection
exit
```

* Go to minio (http://localhost:9001) and log in.

* Go to `wis2box-incoming` bucket

* Create new path: `/nld/knmi_esoh_demo/data/core/weather/surface-based-observations/synop/`

* Upload your BUFR files to this directory, and wait for it to finish by tailing the logs:
```
python3 wis2box-ctl.py logs wis2box-management
```

* Publish the stations again (might not be needed anymore):
```
python3 wis2box-ctl.py login
wis2box metadata station publish-collection
```
