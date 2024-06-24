from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

def processMission1():
    pass

def processMission2():
    pass

def processMission3():
    pass

def processMission4():
    pass

def processMission5():
    pass

def getSensorData():
    pass

def getObjectData():
    pass

def sendInputData():
    pass


class basicMissions(StateMachine):
    # Setup the logging to a file
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='logs/stateMachine/basicMissions.log',  # Log messages will be written to this file
        filemode='w'         # Use 'w' to overwrite the file each time, or 'a' to append to the file
    )
    
    # Define the states
    Start = State('Start', initial=True)
    
    idle = State('Idle')
    
    mission_1 = State('Mission 1')
    mission_2 = State('Mission 2')
    mission_3 = State('Mission 3')
    mission_4 = State('Mission 4')
    mission_5 = State('Mission 5')
    
    stop = State('Stop')
    
    # Define the transitions
    start_to_idle = Start.to(idle)
    
    idle_to_mission_1 = idle.to(mission_1)
    mission_1_to_idle = mission_1.to(idle)
    
    idle_to_mission_2 = idle.to(mission_2)
    mission_2_to_idle = mission_2.to(idle)
    
    idle_to_mission_3 = idle.to(mission_3)
    mission_3_to_idle = mission_3.to(idle)
    
    idle_to_mission_4 = idle.to(mission_4)
    mission_4_to_idle = mission_4.to(idle)
    
    idle_to_mission_5 = idle.to(mission_5)
    mission_5_to_stop = mission_5.to(stop)
    
    def on_start_to_idle(self):
        logging.info('Starting the AUV')
        
    def on_idle_to_mission_1(self):
        logging.info('Starting Mission 1')
        self.processMission1()
        
    def on_mission_1_to_idle(self):
        logging.info('Mission 1 complete')
        
    def on_idle_to_mission_2(self):
        logging.info('Starting Mission 2')
        self.processMission2()
    
    def on_mission_2_to_idle(self):
        logging.info('Mission 2 complete')
        
    def on_idle_to_mission_3(self):
        logging.info('Starting Mission 3')
        self.processMission3()
        
    def on_mission_3_to_idle(self):
        logging.info('Mission 3 complete')
        
    def on_idle_to_mission_4(self):
        logging.info('Starting Mission 4')
        self.processMission4()
        
    def on_mission_4_to_idle(self):
        logging.info('Mission 4 complete')
        
    def on_idle_to_mission_5(self):
        logging.info('Starting Mission 5')
        self.processMission5()
        
    def on_mission_5_to_stop(self):
        logging.info('Mission 5 complete. Stopping the AUV')
        
    def on_stop(self):
        logging.info('AUV has stopped')
        
if __name__ == '__main__':
    m = basicMissions()
    # graph = DotGraphMachine(m)
    # dot = graph()
    # dot.write_png('static/docs/basicMissions.png')
    
    while True:
        sensor_data = getSensorData()
        object_data = getObjectData()
        
        if (sensor_data['voltage1'] or sensor_data['voltage2'] or sensor_data['voltage3']) < 10:
            m.stop()
            break
        elif sensor_data['error']:
            m.stop()
            break
        