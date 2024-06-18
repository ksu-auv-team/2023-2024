'''temp holding
Idle_to_Quarter_Speed_Turn_Left = Idle.to(Quarter_Speed_Turn_Left)
Quarter_Speed_Turn_Left_to_Quarter_Speed_Right = Quarter_Speed_Turn_Left.to(Quarter_Speed_Turn_Right)
Quarter_Speed_Turn_Right_to_Quarter_Speed_Turn_Left = Quarter_Speed_Turn_Right.to(Quarter_Speed_Turn_Left)
Quarter_Speed_Turn_Left_to_Idle = Quarter_Speed_Turn_Left.to(Idle)
Idle_to_Half_Speed_Forward = Idle.to(Half_Speed_Forward)
Half_Speed_Forward_to_Idle = Half_Speed_Forward.to(Idle)
Idle_to_Scan = Idle.to(Scan)
Scan_to_Quarter_Speed_Vertical_Up = Scan.to(Quarter_Speed_Vertical_Up)
Quarter_Speed_Vertical_Up_to_Idle = Quarter_Speed_Vertical_Up.to(Idle)
Idle_to_Quarter_Speed_Lateral_Right = Idle.to(Quarter_Speed_Lateral_Right)
Quarter_Speed_Lateral_Right_to_Idle = Quarter_Speed_Lateral_Right.to(Idle)
Idle_to_Quarter_Speed_Forward = Idle.to(Quarter_Speed_Forward)
Quarter_Speed_Forward_to_Idle = Quarter_Speed_Forward.to(Idle)
Idle_to_Scan = Idle.to(Scan)
Scan_to_Idle = Scan.to(Idle)
Idle_to_Quarter_Speed_Backward = Idle.to(Quarter_Speed_Backward)
Quarter_Speed_Backward_to_Idle = Quarter_Speed_Backward.to(Idle)
Idle_to_Quarter_Speed_Lateral_Left = Idle.to(Quarter_Speed_Lateral_Left)
Quarter_Speed_Lateral_Left_to_Idle = Quarter_Speed_Lateral_Left.to(Idle)
Idle_to_Quarter_Speed_Forward = Idle.to(Quarter_Speed_Forward)
Quarter_Speed_Forward_to_Idle = Quarter_Speed_Forward.to(Idle)
Idle_to_Half_Speed_Forward = Idle.to(Half_Speed_Forward)
Half_Speed_Forward_to_Idle = Half_Speed_Forward.to(Idle)
Idle_to_Quarter_Speed_Turn_Right = Idle.to(Quarter_Speed_Turn_Right)
Quarter_Speed_Turn_Right_to_Idle = Quarter_Speed_Turn_Right.to(Idle)
Idle_to_Quarter_Speed_Forward = Idle.to(Quarter_Speed_Forward)
Quarter_Speed_Forward_to_Idle = Quarter_Speed_Forward.to(Idle)
'''

from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

class AUVStateMachine(StateMachine):
    # Define the states
    # Start and End States
    Start = State('Start', initial=True)
    End = State('End')
    
    # Idle State
    Idle = State('Idle')
    
    # Movement States
    Quarter_Speed_Forward = State('Quarter_Speed_Forward')
    Half_Speed_Forward = State('Half_Speed_Forward')
    Full_Speed_Forward = State('Full_Speed_Forward')
    
    Quarter_Speed_Backward = State('Quarter_Speed_Backward')
    Half_Speed_Backward = State('Half_Speed_Backward')
    Full_Speed_Backward = State('Full_Speed_Backward')
    
    Quarter_Speed_Turn_Left = State('Quarter_Speed_Turn_Left')
    Half_Speed_Turn_Left = State('Half_Speed_Turn_Left')
    Full_Speed_Turn_Left = State('Full_Speed_Turn_Left')
    
    Quarter_Speed_Turn_Right = State('Quarter_Speed_Turn_Right')
    Half_Speed_Turn_Right = State('Half_Speed_Turn_Right')
    Full_Speed_Turn_Right = State('Full_Speed_Turn_Right')
    
    Quarter_Speed_Lateral_Left = State('Quarter_Speed_Lateral_Left')
    Half_Speed_Lateral_Left = State('Half_Speed_Lateral_Left')
    Full_Speed_Lateral_Left = State('Full_Speed_Lateral_Left')
    
    Quarter_Speed_Lateral_Right = State('Quarter_Speed_Lateral_Right')
    Half_Speed_Lateral_Right = State('Half_Speed_Lateral_Right')
    Full_Speed_Lateral_Right = State('Full_Speed_Lateral_Right')
    
    Quarter_Speed_Vertical_Up = State('Quarter_Speed_Vertical_Up')
    Half_Speed_Vertical_Up = State('Half_Speed_Vertical_Up')
    Full_Speed_Vertical_Up = State('Full_Speed_Vertical_Up')
    
    Quarter_Speed_Vertical_Down = State('Quarter_Speed_Vertical_Down')
    Half_Speed_Vertical_Down = State('Half_Speed_Vertical_Down')
    Full_Speed_Vertical_Down = State('Full_Speed_Vertical_Down')
    
    Quarter_Speed_Pitch_Up = State('Quarter_Speed_Pitch_Up')
    Half_Speed_Pitch_Up = State('Half_Speed_Pitch_Up')
    Full_Speed_Pitch_Up = State('Full_Speed_Pitch_Up')
    
    Quarter_Speed_Pitch_Down = State('Quarter_Speed_Pitch_Down')
    Half_Speed_Pitch_Down = State('Half_Speed_Pitch_Down')
    Full_Speed_Pitch_Down = State('Full_Speed_Pitch_Down')
    
    # Scan States
    Scan = State('Scan')
    
    # Gripper States
    Grab = State('Grab')
    Release = State('Release')
    
    # Torpedo States
    Torpedo_Launch_1 = State('Torpedo_Launch_1')
    Torpedo_Launch_2 = State('Torpedo_Launch_2')
    
    # Define the transitions between states
    Start_to_Idle = Start.to(Idle)
    
    # Mission 1 Transitions (Pass the Gate)
    
    # Mission 2 Transitions (Find the path)
    
    # Mission 3 Transitions (Circle the Bouy)
    
    # Mission 4 Transitions (Marker in Bin)
    
    # Mission 5 Transitions (Torpedoes)
    
    # Mission 6 Transitions (Collect Samples)

if __name__ == '__main__':
    m = AUVStateMachine()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/state_machine.png')
