import time
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import pandas as pd


csv_name = 'cv-valid-dev.csv'
api_endpoint = 'http://localhost:8001/asr'


def parse_audio_to_binary(file_path):
    '''
    Reads audio from file_path and returns it in raw binary format.
    '''
    try:
        with open(file_path, 'rb') as f: 
            raw_data = f.read()
        return raw_data
    
    except Exception as e:
        print(e)
        return None

def call_asr_api(raw_audio):
    '''
    Calls asr_api, returns 'EMPTY TRANSCRIPTION' if transcription fails. NaNs are not handled well by elastic-search, so we need placeholder string.
    '''

    files = {'file': raw_audio}
    response = requests.post(api_endpoint, files=files)
    response = response.json()
    
    if 'error' in response:
        duration, transcription = 0, 'EMPTY TRANSCRIPTION'
    else:
        duration, transcription = response['duration'], response['transcription']

    return duration, transcription

def process_audio_file(row):
    '''
    Wrapper function to process each row of the dataframe file_path column.
    '''
    idx, file_path = row.Index, row.file_path
    raw_audio = parse_audio_to_binary(file_path)
    duration, transcription = call_asr_api(raw_audio)
    return idx, duration, transcription

def main(batch_inference=True, max_workers = os.cpu_count()):
    '''
    Performs transcription on files in cv-valid-test. 
    Batch inference makes multiple asynchronous API calls to asr_api on port 8001 to simulate multiple independent API calls.
    '''
    start = time.time()
    audio_files = os.listdir('../cv-valid-test') #[:100] 100 test runs initially 
    df = pd.DataFrame(audio_files, columns=['file_path'])
    df['file_path'] = df['file_path'].apply(lambda x: os.path.join('../cv-valid-test', x))

    
    if not batch_inference:
        for row in df.itertuples():
            idx, file_path = row.Index, row.file_path
            raw_audio  = parse_audio_to_binary(file_path)
            duration, transcription = call_asr_api(raw_audio)
            df.loc[idx, ['duration', 'transcription']] = [duration, transcription]

    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_audio_file, df.itertuples()))

        # Update DataFrame with results
        for result in results:
            idx, duration, transcription = result
            df.loc[idx, ['duration', 'transcription']] = [duration, transcription]

    df.to_csv(csv_name)
    print(f'total inference took {(time.time()-start)/60:.2f} minutes')
    
if __name__ == '__main__':
    main(batch_inference=True, max_workers = 100)
    # main(batch_inference=False)
    