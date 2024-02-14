
FROM python:3.12.2
COPY . /app
WORKDIR /app
RUN apt update && apt install -y gcc-multilib ffmpeg libsm6 libxext6 && \
     pip install --no-cache-dir -r requirements.txt
ENTRYPOINT bash run.sh