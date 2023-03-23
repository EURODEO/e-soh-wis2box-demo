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

### Performance

The following tests were done on a MacBook Pro with Apple M1 Pro processor.
Four cores (out of a total of 10) and 16 GB of memory were assigned to Docker,
unless otherwise noted.

#### Loading data

We load one month of KNMI data for about 60 stations.
This consists of 672 (=28x24) BUFR files, one for each observation time.
Each BUFR files contains multiple messages for the different stations.

We load the data by putting all file in the correct location in the `incoming`
Minio bucket. The data load takes more than an hour to complete.
240 MB of space is used by Elastic after loading 11 MB of BUFR files.

If the wis2box-management container (which does the bulk of the work during data load)
is killed during the load, the loading does not continue when the container is restarted.

#### API load test
We set up a load test of the Feature API of the wis2box using locust (https://locust.io/).
Each request ask for a month of data for a single parameter (one of four)
for a single station (one of seven). The `full` Feature API response is by default
very verbose (740 KB for a month of data), so we also test a `light` response
with most metadata left out (167 KB for a month of data).
`gz` compression is used for all responses.

Each "user" does a new request as soon as the previous request finished.
Multiple users do parallel requests.

We get the following results:

| cores | users | request type | req/s |
|------:|------:|--------------|------:|
|     4 |     1 | full         |    25 | 
|     4 |    20 | full         |    90 | 
|     4 |     1 | light        |    30 | 
|     4 |    20 | light        |   115 | 
|     8 |     1 | full         |    24 | 
|     8 |    20 | full         |   140 | 
|     8 |     1 | light        |    30 | 
|     8 |    20 | light        |   170 | 

### Comments

Based on my very limited testing of wis2box, I have the following comments:
- It is designed in a way to leverage existing technology like Elastic
- Ingestion of 40K station observations (each with multiple parameters) take one hour on my test setup
- To allow bulk loading of data, the `WIS2BOX_BROKER_QUEUE_MAX` size needs to be set to unlimited (or a high number). If not, intermediate points will be dropped.
- Killing and restarting `wis2box-management` container leads to ingestion data loss
- The internal elastic storage is verbose, due to the Feature JSON format and storing all the messages (needed for Replay funcitonality)
- Query performance is good for a Python API (due to offloading of heavy lifting to Elastic?)