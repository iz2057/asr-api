from flask import Flask, request, jsonify
from transformers import pipeline
import torchaudio
import io
import torch
from pydub import AudioSegment
import numpy as np

#server health test command: curl http://localhost:8001/ping
#asr_api test command: curl -F 'file=@ cv-valid-test/sample-000003.mp3' http://localhost:8001/asr

app = Flask(__name__)

#the pipeline object in huggingface transformers is a high-level api that abstracts away preprocessing steps for easy out-of-the-box model inference using pretrained models
#ref: https://huggingface.co/blog/asr-chunking
pipe = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/asr', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    try:
        raw_data = request.files['file'].stream.read()

        audio = AudioSegment.from_mp3(io.BytesIO(raw_data))
        audio_array = np.array(audio.get_array_of_samples())
        audio_tensor = torch.tensor(audio_array, dtype=torch.float32)
        rate = audio.frame_rate

        transform = torchaudio.transforms.Resample(rate, 16000)
        transformed_audio = transform(audio_tensor).squeeze().numpy()
        duration = len(audio)/1000.0
        transcription = pipe(transformed_audio)
    
        return jsonify({"transcription": transcription['text'], "duration": duration})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run(port=8001)
    app.run(host='0.0.0.0', port=8001)

