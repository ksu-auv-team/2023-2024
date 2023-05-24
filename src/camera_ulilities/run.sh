docker build -t camera_utilities:latest .

docker run -it --device=/dev/video0 --group-add video camera_utilities:latest