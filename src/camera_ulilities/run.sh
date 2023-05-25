sudo docker build -t camera_utilities:latest .

sudo docker run -it --device=/dev/video0 --group-add video camera_utilities:latest