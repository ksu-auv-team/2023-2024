FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    v4l-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "src/camera_utilities.py"]
