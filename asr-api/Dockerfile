FROM python:3.8 

WORKDIR /asr

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update -qq && apt-get install ffmpeg -y #this is needed for pydub

COPY . .

EXPOSE 8001

CMD ["python", "asr_api.py"]
