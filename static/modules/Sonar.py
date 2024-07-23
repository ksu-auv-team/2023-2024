from brping import Ping360
from brping import definitions
import logging
import numpy as np
"""
Ping360 has an effective range of 60 meters (175 feet)
Its range can be calculated using the equation:
velocity_of_sound * sample_period * 12.5e-9 * number_of_samples

Each sample will cover a distance calculated by:
velocity_of_sound * sample_period * 12.5e-9

Ping360 will return hex values which can be casted to a uint8
array. The values in this array correspond to intensity of the 
returning signal (0-255). The resulting array will have index 0
refer to the distance 0 to sample distance, index 1 will cover
the distance sample distance to 2*sample distance, so on and so forth.
"""

# Configure logging
logging.basicConfig(filename='ping360_data.log', level=logging.INFO, format='%(asctime)s:%(angle)s:%(distance)s')

def meters_per_sample(ping_message, v_sound=1480):
        ##Calculates the distance that each sample covers.
        ##the 12.5e-9 is the sample_period time divided by two
        return v_sound * ping_message.sample_period * 12.5e-9

def Sonar360():
        p = Ping360()
        p.connect_serial("/dev/ttyUSB0", 115200) ##Connects to sonar
        p.initialize()##Initializes
        p.set_transmit_frequency(750)##Sets frequency of tranmission, limited to 650 to 850 for practicallity
        p.set_sample_period(1355)##Sets sample period (increase to increase range) (range is 80 to 40000)
        p.set_number_of_samples(1200)##Sets number of samples (increase to increase range). (range is 200 to 1200)
        p.set_gain_setting(0)##Sets gain setting (0 = low, 1 = medium, 2 = high)
        p.set_mode(1)##set as 1 for Ping360
        p.set_transmit_duration(40)##Sets duration of transmission in microseconds

        # Get data
        while True:
                try:
                    for gradian in range(400):
                        highestIndex = 0
                        highestValue = 0
                        d = p.transmitAngle(gradian) ##Fires pulse in a gradian direction
                        distperSample = meters_per_sample(d, 1480) ##Determines the distance of a single sample
                        data = np.frombuffer(d.data, dtype=np.uint8)##Converts data to uint8 array
                        ##Sonar won't sense correctly in a radius of .75 meters around it, calculates the value to prevent measuring in that range
                        if gradian == 0:
                                lower_limit = 0
                                while lower_limit < .75:
                                        lower_limit = lower_limit + distperSample
                                lower_limit = lower_limit/distperSample
                                lower_limit = int(lower_limit)

                        hold = 1


                        for sample in range(lower_limit, d.number_of_samples, 1):
                                if(data[sample]>126): ##Stores values that return a strength over 126 (values range 0-255)
                                        if data[sample] > highestValue: ##Should the signal intensity be higher than previously recorded one then replace
                                                highestValue = data[sample]
                                                highestIndex = sample
                                        

                        
                        if (highestValue < 127): ##If signal intensity is too low then doesn't record values
                            hold = -1
                            ##logging.info(f'Object not Detected at {float(.9*gradian)} degrees.')
                        if (hold != -1):
                            print("Gradian: "+str(gradian)+ " Obstacle Detected ("+ str(highestValue)+") at "+ str(highestIndex*distperSample)+ " meters.")
                            
                            ##Variables for JSON storing
                            outputAngle = float(.9*gradian)
                            outputDistance = float(highestIndex*distperSample)

                            ##Dictionay for JSON
                            logData = {'angle': outputAngle, 'distance': outputDistance}
                            ##logging.info(f'Object Detected at {float(.9*gradian)} degrees, {float(highestIndex*distperSample)} meters.')

                    ##break ##uncomment break to allow for single 360 scan.

                except KeyboardInterrupt:
                    break    

if __name__ == "__main__":
    Sonar360()

