FROM python:3.9-slim-buster

WORKDIR /app

COPY configs configs
COPY src src

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python3", "src/camera_utilities.py"]