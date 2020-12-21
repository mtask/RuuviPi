RuuviPi is a Flask based python application that provides JSON datasource to visualize data from [Ruuvi tags](https://ruuvi.com/) in [Grafana](https://grafana.com/).

# Deployment

Below is a quick setup guide for the RuuviPi API. More detailed instructions can be found in [here](https://mtask.github.io/2020/12/22/raspberrypi-and-ruuvitag-part-two.html).

## Install dependencies

```
sudo apt install bluez bluez-hcidump python3-pip
pip3 install ruuvitag_sensor flask python-dateutil
```

## Run the application

* Run development server

```
python3 ruuviDataSource.py
```

* Gunicorn

```
gunicorn --bind 127.0.0.1:8080 wsgi:app
```

## Setup grafana

Install Grafana [JSON plugin](https://grafana.com/grafana/plugins/simpod-json-datasource) and configure RuuviPi's URL as a data source and 
specify it as a data source for a panel with table format.
