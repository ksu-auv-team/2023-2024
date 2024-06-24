from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests


class basicMovement(StateMachine):
    # Setup the logging to a file
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='logs/stateMachine/basicMovement.log',  # Log messages will be written to this file
        filemode='w'         # Use 'w' to overwrite the file each time, or 'a' to append to the file
    )
    
    # Define the states of the state machine
    start = State('Start', initial=True)
    
    idle = State('State')
    
    forwardQuarter = State('Forward Quarter')
    forwardHalf = State('Forward Half')
    forwardFull = State('Forward Full')
    
    backwardQuarter = State('Backward Quarter')
    backwardHalf = State('Backward Half')
    backwardFull = State('Backward Full')
    
    rotateLeftQuarter = State('Rotate Left Quarter')
    rotateLeftHalf = State('Rotate Left Half')
    rotateLeftFull = State('Rotate Left Full')
    
    rotateRightQuarter = State('Rotate Right Quarter')
    rotateRightHalf = State('Rotate Right Half')
    rotateRightFull = State('Rotate Right Full')
    
    lateralLeftQuarter = State('Lateral Left Quarter')
    lateralLeftHalf = State('Lateral Left Half')
    lateralLeftFull = State('Lateral Left Full')
    
    lateralRightQuarter = State('Lateral Right Quarter')
    lateralRightHalf = State('Lateral Right Half')
    lateralRightFull = State('Lateral Right Full')
    
    stop = State('Stop')
    
    end = State('End', final=True)
    
    # Define the transitions between states
    start_to_idle = start.to(idle)
    
    idle_to_forwardQuarter = idle.to(forwardQuarter)
    idle_to_forwardHalf = idle.to(forwardHalf)
    idle_to_forwardFull = idle.to(forwardFull)
    
    idle_to_backwardQuarter = idle.to(backwardQuarter)
    idle_to_backwardHalf = idle.to(backwardHalf)
    idle_to_backwardFull = idle.to(backwardFull)
    
    idle_to_rotateLeftQuarter = idle.to(rotateLeftQuarter)
    idle_to_rotateLeftHalf = idle.to(rotateLeftHalf)
    idle_to_rotateLeftFull = idle.to(rotateLeftFull)
    
    idle_to_rotateRightQuarter = idle.to(rotateRightQuarter)
    idle_to_rotateRightHalf = idle.to(rotateRightHalf)
    idle_to_rotateRightFull = idle.to(rotateRightFull)
    
    idle_to_lateralLeftQuarter = idle.to(lateralLeftQuarter)
    idle_to_lateralLeftHalf = idle.to(lateralLeftHalf)
    idle_to_lateralLeftFull = idle.to(lateralLeftFull)
    
    idle_to_lateralRightQuarter = idle.to(lateralRightQuarter)
    idle_to_lateralRightHalf = idle.to(lateralRightHalf)
    idle_to_lateralRightFull = idle.to(lateralRightFull)
    
    forwardQuarter_to_stop = forwardQuarter.to(stop)
    forwardHalf_to_stop = forwardHalf.to(stop)
    forwardFull_to_stop = forwardFull.to(stop)
    
    backwardQuarter_to_stop = backwardQuarter.to(stop)
    backwardHalf_to_stop = backwardHalf.to(stop)
    backwardFull_to_stop = backwardFull.to(stop)
    
    rotateLeftQuarter_to_stop = rotateLeftQuarter.to(stop)
    rotateLeftHalf_to_stop = rotateLeftHalf.to(stop)
    rotateLeftFull_to_stop = rotateLeftFull.to(stop)
    
    rotateRightQuarter_to_stop = rotateRightQuarter.to(stop)
    rotateRightHalf_to_stop = rotateRightHalf.to(stop)
    rotateRightFull_to_stop = rotateRightFull.to(stop)
    
    lateralLeftQuarter_to_stop = lateralLeftQuarter.to(stop)
    lateralLeftHalf_to_stop = lateralLeftHalf.to(stop)
    lateralLeftFull_to_stop = lateralLeftFull.to(stop)
    
    lateralRightQuarter_to_stop = lateralRightQuarter.to(stop)
    lateralRightHalf_to_stop = lateralRightHalf.to(stop)
    lateralRightFull_to_stop = lateralRightFull.to(stop)
    
    stop_to_idle = stop.to(idle)
    
    stop_to_end = stop.to(end)
    
    def sendMovement(self, movement):
        # Send the movement command to the AUV
        if len(movement) == 1:
            if movement[0] == 'stop':
                logging.info('Sending movement command: %s', movement)
            else:
                logging.error('Invalid movement command: %s', movement)
        elif len(movement) == 2:
            if movement[0] == 'forward' or movement[0] == 'backward':
                if movement[1] == 'quarter' or movement[1] == 'half' or movement[1] == 'full':
                    logging.info('Sending movement command: %s', movement)
                else:
                    logging.error('Invalid movement command: %s', movement)
            else:
                logging.error('Invalid movement command: %s', movement)
        elif len(movement) == 3:
            if movement[0] == 'rotate':
                if movement[1] == 'left' or movement[1] == 'right':
                    if movement[2] == 'quarter' or movement[2] == 'half' or movement[2] == 'full':
                        logging.info('Sending movement command: %s', movement)
                    else:
                        logging.error('Invalid movement command: %s', movement)
                else:
                    logging.error('Invalid movement command: %s', movement)
            elif movement[0] == 'lateral':
                if movement[1] == 'left' or movement[1] == 'right':
                    if movement[2] == 'quarter' or movement[2] == 'half' or movement[2] == 'full':
                        logging.info('Sending movement command: %s', movement)
                    else:
                        logging.error('Invalid movement command: %s', movement)
                else:
                    logging.error('Invalid movement command: %s', movement)
            else:
                logging.error('Invalid movement command: %s', movement)
        else:
            logging.error('Invalid movement command: %s', movement)
    
    def on_start(self):
        logging.info('Starting the state machine')
        
    def on_idle(self):
        logging.info('The AUV is idle')
        
    def on_forwardQuarter(self):
        self.sendMovement(['forward', 'quarter'])
        logging.info('The AUV is moving forward at quarter speed')
        
    def on_forwardHalf(self):
        self.sendMovement(['forward', 'half'])
        logging.info('The AUV is moving forward at half speed')
        
    def on_forwardFull(self):
        self.sendMovement(['forward', 'full'])
        logging.info('The AUV is moving forward at full speed')
        
    def on_backwardQuarter(self):
        self.sendMovement(['backward', 'quarter'])
        logging.info('The AUV is moving backward at quarter speed')
        
    def on_backwardHalf(self):
        self.sendMovement(['backward', 'half'])
        logging.info('The AUV is moving backward at half speed')
        
    def on_backwardFull(self):
        self.sendMovement(['backward', 'full'])
        logging.info('The AUV is moving backward at full speed')
        
    def on_rotateLeftQuarter(self):
        self.sendMovement(['rotate', 'left', 'quarter'])
        logging.info('The AUV is rotating left at quarter speed')
        
    def on_rotateLeftHalf(self):
        self.sendMovement(['rotate', 'left', 'half'])
        logging.info('The AUV is rotating left at half speed')
        
    def on_rotateLeftFull(self):
        self.sendMovement(['rotate', 'left', 'full'])
        logging.info('The AUV is rotating left at full speed')
        
    def on_rotateRightQuarter(self):
        self.sendMovement(['rotate', 'right', 'quarter'])
        logging.info('The AUV is rotating right at quarter speed')
        
    def on_rotateRightHalf(self):
        self.sendMovement(['rotate', 'right', 'half'])
        logging.info('The AUV is rotating right at half speed')
        
    def on_rotateRightFull(self):
        self.sendMovement(['rotate', 'right', 'full'])
        logging.info('The AUV is rotating right at full speed')
        
    def on_stop(self):
        self.sendMovement(['stop'])
        logging.info('The AUV has stopped')
        
    def on_end(self):
        logging.info('Ending the state machine')
        
    def on_transition(self, from_state, to_state):
        self.sendMovement(['stop'])
        logging.info('Transitioning from %s to %s', from_state, to_state)
        
    def on_exit(self, state):
        logging.info('Exiting state %s', state)
        
    def on_enter(self, state):
        logging.info('Entering state %s', state)
        
    def on_stay(self, state):
        if state == 'idle':
            self.sendMovement(['stop'])
        elif state == 'stop':
            self.sendMovement(['stop'])
        elif state == 'end':
            self.sendMovement(['stop'])
        elif state == 'start':
            self.sendMovement(['stop'])
        elif state == 'forwardQuarter':
            self.sendMovement(['forward', 'quarter'])
        elif state == 'forwardHalf':
            self.sendMovement(['forward', 'half'])
        elif state == 'forwardFull':
            self.sendMovement(['forward', 'full'])
        elif state == 'backwardQuarter':
            self.sendMovement(['backward', 'quarter'])
        elif state == 'backwardHalf':
            self.sendMovement(['backward', 'half'])
        elif state == 'backwardFull':
            self.sendMovement(['backward', 'full'])
        elif state == 'rotateLeftQuarter':
            self.sendMovement(['rotate', 'left', 'quarter'])
        elif state == 'rotateLeftHalf':
            self.sendMovement(['rotate', 'left', 'half'])
        elif state == 'rotateLeftFull':
            self.sendMovement(['rotate', 'left', 'full'])
        elif state == 'rotateRightQuarter':
            self.sendMovement(['rotate', 'right', 'quarter'])
        elif state == 'rotateRightHalf':
            self.sendMovement(['rotate', 'right', 'half'])
        elif state == 'rotateRightFull':
            self.sendMovement(['rotate', 'right', 'full'])
        elif state == 'lateralLeftQuarter':
            self.sendMovement(['lateral', 'left', 'quarter'])
        elif state == 'lateralLeftHalf':
            self.sendMovement(['lateral', 'left', 'half'])
        elif state == 'lateralLeftFull':
            self.sendMovement(['lateral', 'left', 'full'])
        elif state == 'lateralRightQuarter':
            self.sendMovement(['lateral', 'right', 'quarter'])
        elif state == 'lateralRightHalf':
            self.sendMovement(['lateral', 'right', 'half'])
        elif state == 'lateralRightFull':
            self.sendMovement(['lateral', 'right', 'full'])
        else:
            self.sendMovement(['stop'])
            logging.error('Invalid state: %s', state)
        logging.info('Staying in state %s', state)

if __name__ == '__main__':
    m = basicMovement()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/basicMovement.png')
