# Kennesaw State University - AUV Team - 2023 through 2024 #

# Task List #
#### Each node has it's own tasks that need to be completed ####
#### Please make sure to note which tasks you are completing within this file before you push to the github ####

## Tasks ##
- [ ] GCS
  - [ ] GUI Creation
  - [ ] Ping Function
      - Is a subsystem algorithm that pings the external subsystems to verify that they are still connected to the network
  - [ ] Controller Input Function
      - Is a subsystem algorithm that allows the user to control the AUV
      - Multiple controller configuration files, all stored within the 'configs/controllers' folder
      - Controller configuration files are in the format of 'controller_name.yml'
          - The format of the controller configuration files are as follows:
      - The user defines the controller configuration file that they want to use when they start the GCS
          - The user can define the controller configuration file that they want to use when they start the GCS by using the '--controller' flag or the '--c' flag
          - If the user does not define a controller configuration file, then the GCS will use the default controller configuration file
  - [ ] SSH Function
      - Is a subsystem algorithm that allows the user to SSH into the external subsystems to start and stop the subsystems
      - Calls the Ping Function to verify that the external subsystems are still connected to the network (runs before SSH into the external subsystems)
  - [ ] Camera Function
    - [ ] Receive images from sub or have a placeholder image within the gui. 
  - [ ] Start Subsystem Function
      - Is a subsystem algorithm that allows the user to start the external subsystems
      - Calls the SSH Function to SSH into the external subsystems
      - Starts Individual threads for each external subsystem
       - CP = Camera Processing
       - MV = Machine Vision
       - MP = Movement Package
       - SP = Sensor Package
       - SM = State Machine
  - [ ] Stop Subsystem Function
      - Loops through all of the external subsystems and stops them and saves their log files
  - [ ] Restart Subsystem Function
      - Loops through all of the external subsystems and restarts them and saves their log files
- [ ] CP
  - [ ] ZED Camera Package
    - [ ] ZED SDK Installation
        - The ZED SDK is only available for Ubuntu and Windows
    - [ ] ZED SDK Configuration
    - [ ] ZED Camera Calibration
    - [ ] ZED Camera Stereo Vision
    - [ ] ZED Camera Depth Sensing
    - [ ] ZED Camera Streaming to Port
  - [ ] Regular Camera Package
    - [ ] Bottom Camera Calibration
    - [ ] Bottom Camera Streaming to Port
- [ ] MV
  - [ ] Camera Input
      - Listen to the port that the CP is streaming to (only if AUV is toggled '--AUV')
  - [ ] Object Detection
      - Separate the objects from the background
      - Detect the objects
      - Classify the objects (calls the Object Classification function)
      - Return the objects in a dictionary '{classified_object: [x, y, z, width, height, depth, confidence]}'
  - [ ] Object Tracking
      - If the object x, y, z values are different from the previous frame, then update the dictionary
  - [ ] Object Classification
      - Using YOLOV8, classify the object
  - [ ] State Machine Output
      - Send the dictionary to the State Machine
- [ ] HI
  - [ ] Still in planning phase
- [ ] SM
  - [ ] Still in planning phase

## Helpful Links ##
Python Documentation: https://docs.python.org/3/
Python Tutorial: https://www.youtube.com/watch?v=eWRfhZUzrAc
Python State Machine Library: https://python-statemachine.readthedocs.io/en/latest/
