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
logging.basicConfig(filename='ping360_data.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def meters_per_sample(ping_message, v_sound=1480):
        ##Calculates the distance that each sample covers.
        ##the 12.5e-9 is the sample_period time divided by two
        return v_sound * ping_message.sample_period * 12.5e-9

def Sonar360():
        p = Ping360()
        p.connect_serial("COM3", 115200) ##Connects to sonar
        p.initialize()##Initializes
        p.set_transmit_frequency(750)##Sets frequency of tranmission, limited to 650 to 850 for practicallity
        p.set_sample_period(1355)##Sets sample period (increase to increase range) (range is 80 to 40000)
        p.set_number_of_samples(600)##Sets number of samples (increase to increase range). (range is 200 to 1200)
        p.set_gain_setting(0)##Sets gain setting (0 = low, 1 = medium, 2 = high)
        p.set_mode(1)##set as 1 for Ping360
        p.set_transmit_duration(40)##Sets duration of transmission in microseconds

        continueObject = False ##Used to deal with objects that are below intensity sensing threshold
        # Get data
        while True:
                try:
                    for gradian in range(400):
                        highestIndex = 0
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

                        hold = -1

                        ##checks if object sensed from lower intensity continues at other gradian.
                        ##if intensity of next gradian is not within expected bounds then turns
                        ##off detection of object continuing
                        if continueObject:
                                continueObject = False
                                for sample in range(lower_limit, d.number_of_samples, 1):
                                         if sample == continueObjectIndex or sample == continueObjectIndex -1 or sample == continueObjectIndex + 1:
                                                if(data[sample] > pastData[continueObjectIndex]-10 or data[sample] < pastData[continueObjectIndex]+10):
                                                       highestIndex = sample
                                                       continueObjectIndex = sample
                                                       continueObject = True
                                                       break

                        for sample in range(lower_limit, d.number_of_samples, 1):
                                if(data[sample]>126): ##Stores values that return a strength over 126 (values range 0-255)
                                        if data[sample] > highestIndex: ##Should the signal intensity be higher than previously recorded one then replace
                                                highestIndex = sample
                                
                                                
                                if gradian != 0:
                                        if(data[sample] > pastData[sample] + 80):
                                                if data[sample] > highestIndex:
                                                        highestIndex = sample
                                                continueObject = True ##Used to handle sensing an object over multiple gradians despite intensity being below 126
                                                continueObjectIndex = sample
                                                                       
                                               
                                               
                                                
                        pastData = data
                        if (data[highestIndex] < 127): ##If signal intensity is too low then doesn't record values
                            hold = -1
                        if (hold != -1):
                            print("Gradian: "+str(gradian)+ " Obstacle Detected ("+ str(data[highestIndex])+") at "+ str(highestIndex*distperSample)+ " meters.")
                            ##logging("Gradian: "+str(gradian)+ " Obstacle Detected ("+ str(data[hold])+") at "+ str(highestIndex*distperSample)+ " meters.")
                    break ##uncomment break to allow for single 360 scan.

                except KeyboardInterrupt:
                    break    

if __name__ == "__main__":
    Sonar360()

