FROM navikey/raspbian-bullseye:latest

RUN apt update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip vim
RUN apt install -y python3-picamera2 --no-install-recommends
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip
RUN pip install schedule pillow RPi.bme280 smbus2 flask flask_apscheduler

# FROM hackrsackr/horti-flask:latest  

WORKDIR /app

ADD . /app/

CMD ["python", "-u", "/app.py"]
