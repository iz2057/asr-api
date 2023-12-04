# HTX Take Home

This repo creates a speech-to-text microservice for the purpose of the HTX take home. The repo is structured as follows:

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

# Getting Started

## asr_api.py: 
The speech-to-text model utilizes the *wav2vec2-large-960h* from huggingface, which in turn runs on a pytorch backend. The prediction api `asr_api.py` runs on Flask, receives audio files in raw binary format, and returns a transcription of the audio file. To simulate api calls, calls are generated from `cv-decode.py`, which calls `asr_api` with a post request containing the binary audio data. 

Presumably, this is meant to simulate asynchronous calls to `asr_api` in a production environment, so each api call is processed independently, meaning there is no batch transcription by the pytorch model. However, asynchronous api calling has been implemented in cv-decode.py using the `concurrent-futures` package for multiple simultaneous api calls for greater speed.

```bash
docker build asr_api .
docker run asr_api -p 8001:8001
```
then
```bash
python cv-decode.py
```

## elastic-backend: 
Open `.env` and configure environmental variables
```bash
docker-compose up
```
then to index data to the elastic-search server
```bash
python cv-index.py
```

### Debugging: 
- If elasticsearch is failing to start, it might be due to insufficient virtual memory. Try running `sysctl -w vm.max_map_count=262144`, references [here (elasticsearch)](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html) and [here (stackoverflow)](https://stackoverflow.com/questions/67528888/1-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-increase-to-a.)
- Be sure to run `pip install elasticsearch` in order to run cv-index.py if the elasticsearch package is already installed.

## search-ui:
Instructions here are based on the search-ui github [here](https://github.com/elastic/app-search-reference-ui-react)

Requires [npm](https://www.npmjs.com/).

Dependencies:
- Node v16.13.0
```bash
# Run this to install Node 16.13.0
nvm install 16.13.0

# Run this to use the installed Node version 
nvm use 16.13.0

# Run this to set everything up
npm install

# Run this to start your application and open it up in a new browser window
npm start
```