#to build on docker host first: docker build --no-cache=true -f Dockerfile https://github.com/brianr82/sensorsim.git -t brianr82/sensorsim:latest
#usage example: docker run -it -e PI_IP='10.12.7.45' -e PI_PORT='1880' -e NUM_MSG='100' -e SENSOR_ID='simsensor001' singlesensorsim
FROM python:3.6-slim
RUN mkdir app
WORKDIR app
COPY / /app
RUN apt-get update && apt-get install -y build-essential \
    cmake \
    wget \
    git \
    libgtk2.0-dev \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

RUN pip install opencv-contrib-python-headless
RUN pip install cassandra-driver

CMD python ./main.py $camera_id $cassandra_ip