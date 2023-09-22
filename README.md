# MBTA-console
>CLI to get info for the MBTA subway system

![](mbta_map.jpeg)

Python console for querying data from MBTA API

The user will be able to print to console:

1) Long names for all light rails and heavy rails

2) Name of subway route with most stops and the number of stops on that route

3) Name of subway route with fewest stops and the number for stops on that route

4) List of all the stops that connect two or more subway routes along with the relevant route names for
each of those stops

5) Rail route between two given stops

## Installation

1. Download source files (e.g.)

```sh
git clone git@github.com:agover97/MBTA-console.git
```

2. Setup virtual environment 

You may need to install venv on Debian/Ubuntu systems:
```sh
python3 --version
apt install python[VERSION]-venv
```


```sh
cd MBTA-console/
python3 -m venv ./venv
source venv/bin/activate
(venv) $
```

3. Install dependencies

```sh
(venv) $ python -m pip install -r requirements.txt
```

Note: This installation setup with tested on a virtual machine running Ubuntu 22.04.3 LTS
https://ubuntu.com/download/desktop


## Usage example



## Testing


