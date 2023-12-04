from flask import Flask, request, jsonify
from transformers import pipeline
import torchaudio
import io
import torch
from pydub import AudioSegment
import numpy as np

app = Flask(__name__)

#the pipeline object in huggingface transformers is a high-level api that abstracts away preprocessing steps for easy out-of-the-box model inference using pretrained models
#ref: https://huggingface.co/blog/asr-chunking
pipe = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")

@app.route('/ping', methods=['GET'])
def ping():
    '''Simple function to test server health'''
    return 'pong'

@app.route('/asr', methods=['POST'])
def transcribe_audio():
    '''
    Handles POST requests on /asr. Checks for binary audio file, parses using pydub AudioSegment then converts to torch tensor for transcription.
    
    '''
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    try:
        raw_data = request.files['file'].stream.read()

        audio = AudioSegment.from_mp3(io.BytesIO(raw_data))
        audio_array = np.array(audio.get_array_of_samples())
        audio_tensor = torch.tensor(audio_array, dtype=torch.float32)
        rate = audio.frame_rate

        transform = torchaudio.transforms.Resample(rate, 16000) #model used requires a sample rate of 16000, so any input data must be resampled
        transformed_audio = transform(audio_tensor).squeeze().numpy()
        duration = len(audio)/1000.0 #the duration of the audio file is the length divided by 1000
        transcription = pipe(transformed_audio)
    
        return jsonify({"transcription": transcription['text'], "duration": duration})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run(port=8001)
    app.run(host='0.0.0.0', port=8001)

