cat /etc/nv_tegra_release
sudo apt update
sudo apt dist-upgrade
sudo apt install nvidia-jetpack
cd ~/Downloads

# Uncomment the line that matches your OS Version
# Ubuntu 20.04
wget https://download.stereolabs.com/zedsdk/4.0/cu121/ubuntu20

# Ubuntu 22.04
# wget https://download.stereolabs.com/zedsdk/4.0/cu121/ubuntu22 

# Run the ZED SDK installer
chmod +x ZED_SDK_Linux_*.run
./ZED_SDK_Linux_*.run