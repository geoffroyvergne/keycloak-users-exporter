# Keycloak CSV users importer

## Usage
```
usage: exporter.py [-h] [-f FILE] [-c FILE] [-l LIMIT]

Export Keycloak users to CSV

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  CSV file that will contains users
  -c FILE, --config FILE
                        Config file
  -l LIMIT, --limit LIMIT
                        limit CSV user to export
```

## CSV format
```userName,email,firstName,lastName```
Map .ini Config CSV part to map rows name

## Run
```python exporter.py```
