# ASR-API

This repo creates a speech-to-text microservice. The repo is structured as follows:

```
|-- asr_api/
| |-- asr_api.py
| |-- cv-decode.py
| |-- requirements.txt
| |-- Dockerfile
|
|-- elastic-backend/
| |-- docker-compose.yml
| |-- .env
|
|-- search-ui
| |-- ...
```
# Requirements: 
1. Docker (microservice is run on a debian-11-bullseye image on GCP, see Docker installation [here](https://docs.docker.com/engine/install/debian/))
2. Docker-compose, if not already installed with docker
3. Google Cloud SDK (for convenience if deploying on cloud, (here)[https://cloud.google.com/sdk/docs/install])

Additionally, the implementation on GCP can be found in *architure.pdf*. See `demo.ipynb` for a demonstration of the asr_api.

# Demo:
Refer to `demo.ipynb` for a demonstration, or run the following commands: 

asr_api:
```bash
#ping the asr_api
curl 'http://35.236.42.100:8001/ping'
```


Elastic-search:
```bash
#Query elastic-search server for rows with transcription containing the word 'boy'
curl -X GET "http://34.94.242.203:9200/cv-transcriptions/_search" -H 'Content-Type: application/json' -d '
{
  "query": {
    "match": {
      "transcription": "boy"
    }
  }
}'

#Query elastic-search server for rows with duration less than 5 seconds
curl -X GET "http://34.94.242.203:9200/cv-transcriptions/_search" -H 'Content-Type: application/json' -d
  "query": {
    "range": {
      "duration": {
        "lt": 5
      }
    }
  }
}'
```


# Getting Started
```bash
git clone https://github.com/iz2057/asr-api.git
cd asr-api
```

## asr_api: 
The speech-to-text model utilizes the *wav2vec2-large-960h* from huggingface, which in turn runs on a pytorch backend. The prediction api `asr_api.py` runs on Flask, receives audio files in raw binary format, and returns a transcription of the audio file. To simulate api calls, calls are generated from `cv-decode.py`, which calls `asr_api` with a post request containing the binary audio data. 

Presumably, this is meant to simulate asynchronous calls to `asr_api` in a production environment, so each api call is processed independently, meaning there is no batch transcription by the pytorch model. However, asynchronous api calling has been implemented in cv-decode.py using the `concurrent-futures` package for multiple simultaneous api calls for greater speed.

```bash
cd asr_api
docker build asr_api .
docker run asr_api -p 8001:8001
```
then
```bash
python cv-decode.py
```
Note that `cv-decode.py` can be run from anywhere since it is a public IP address, but in this instance it is run from within the GCE VM.

## elastic-backend: 
Open `.env` and configure environmental variables, then
```bash
cd elastic-backend
docker-compose up
```
then to index data to the elastic-search server
```bash
python cv-index.py
```
Note that `cv-index.py` can be run from anywhere since it is a public IP address, but in this instance it is run from either GCE VM or Cloud Function.

### Debugging: 
- If elasticsearch is failing to start, it might be due to insufficient virtual memory. Try running `sysctl -w vm.max_map_count=262144`, references [here (elasticsearch)](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html) and [here (stackoverflow)](https://stackoverflow.com/questions/67528888/1-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-increase-to-a.)
- If the above does not work because sysctl is not available (such as in GCE VM), try the solution listed (here)[https://serverfault.com/questions/681745/unable-to-change-vm-max-map-count-for-elasticsearch] using `su root`. 
- Be sure to run `pip install elasticsearch` in order to run cv-index.py if the elasticsearch package is already installed, or if running in container, add elasticsearch to requirements.

## search-ui:
Code and instructions here are based on the search-ui github page [here](https://github.com/elastic/app-search-reference-ui-react)

Requires [npm](https://www.npmjs.com/).

Dependencies:
- Node v16.13.0
```bash
cd search-ui

# Run this to install Node 16.13.0
nvm install 16.13.0

# Run this to use the installed Node version 
nvm use 16.13.0

# Run this to set everything up
npm install

# Run this to start your application and open it up in a new browser window
npm start
```