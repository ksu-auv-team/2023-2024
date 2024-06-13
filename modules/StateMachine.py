from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

class StateMachine(StateMachine):
    # Define the states
    Idle = State('Idle')
    Scan = State('Scan')
    Movement = State('Movement')
    Locate = State('Locate')
    Grab = State('Grab')
    Release = State('Release')
    Torpedo_Launch_1 = State('Torpedo_Launch_1')
    Torpedo_Launch_2 = State('Torpedo_Launch_2')
    Object_Detection_Algorithm_1 = State('Object_Detection_Algorithm_1')
    Object_Detection_Algorithm_2 = State('Object_Detection_Algorithm_2')
    Object_Detection_Algorithm_3 = State('Object_Detection_Algorithm_3')
    Object_Detection_Algorithm_4 = State('Object_Detection_Algorithm_4')
    Object_Detection_Algorithm_5 = State('Object_Detection_Algorithm_5')
    Object_Detection_Algorithm_6 = State('Object_Detection_Algorithm_6')
    Mission_1 = State('Mission_1', initial=True)
    Mission_2 = State('Mission_2')
    Mission_3 = State('Mission_3')
    Mission_4 = State('Mission_4')
    Mission_5 = State('Mission_5')
    End = State('End')
    
    # Define the transitions
    # Mission 1
    Mission_1_to_Idle = Mission_1.to(Idle)
    Idle_to_Scan = Idle.to(Scan)
    Scan_to_Object_Detection_Algorithm_1 = Scan.to(Object_Detection_Algorithm_1)
    Object_Detection_Algorithm_1_to_Movement = Object_Detection_Algorithm_1.to(Movement)
    Movement_to_Locate = Movement.to(Locate)
    Locate_to_Scan = Locate.to(Scan)
    Scan_to_Object_Detection_Algorithm_2 = Scan.to(Object_Detection_Algorithm_2)
    Scan_to_Movement = Scan.to(Movement)
    Movement_to_Movement = Movement.to(Movement)
    Movement_to_Idle = Movement.to(Idle)
    Idle_to_Mission_2 = Idle.to(Mission_2)
    
    # Mission 2
    Mission_2_to_Idle = Mission_2.to(Idle)
    Idle_to_Movement = Idle.to(Movement)
    Movement_to_Scan = Movement.to(Scan)
    Scan_to_Object_Detection_Algorithm_3 = Scan.to(Object_Detection_Algorithm_3)
    Object_Detection_Algorithm_3_to_Movement = Object_Detection_Algorithm_3.to(Movement)
    Movement_to_Object_Detection_Algorithm_3 = Movement.to(Object_Detection_Algorithm_3)
    Movement_to_Idle = Movement.to(Idle)
    Idle_to_Mission_3 = Idle.to(Mission_3)
    
    # Mission 3
    Mission_3_to_Idle = Mission_3.to(Idle)
    Idle_to_Scan = Idle.to(Scan)
    Scan_to_Object_Detection_Algorithm_1 = Scan.to(Object_Detection_Algorithm_1)
    Object_Detection_Algorithm_1_to_Movement = Object_Detection_Algorithm_1.to(Movement)
    Movement_to_Grab = Movement.to(Grab)
    Grab_to_Movement = Grab.to(Movement)
    Movement_to_Scan = Movement.to(Scan)
    Scan_to_Object_Detection_Algorithm_4 = Scan.to(Object_Detection_Algorithm_4)
    Object_Detection_Algorithm_4_to_Movement = Object_Detection_Algorithm_4.to(Movement)
    Movement_to_Release = Movement.to(Release)
    Release_to_Movement = Release.to(Movement)
    Movement_to_Idle = Movement.to(Idle)
    Idle_to_Mission_4 = Idle.to(Mission_4)
    
    # Mission 4
    Mission_4_to_Idle = Mission_4.to(Idle)
    Idle_to_Scan = Idle.to(Scan)
    Scan_to_Object_Detection_Algorithm_1 = Scan.to(Object_Detection_Algorithm_1)
    Object_Detection_Algorithm_1_to_Movement = Object_Detection_Algorithm_1.to(Movement)
    Movement_to_Object_Detection_Algorithm_5 = Movement.to(Object_Detection_Algorithm_5)
    Object_Detection_Algorithm_5_to_Torpedo_Launch_1 = Object_Detection_Algorithm_5.to(Torpedo_Launch_1)
    Torpedo_Launch_1_to_Movement = Torpedo_Launch_1.to(Movement)
    Movement_to_Torpedo_Launch_2 = Movement.to(Torpedo_Launch_2)
    Torpedo_Launch_2_to_Movement = Torpedo_Launch_2.to(Movement)
    Movement_to_Idle = Movement.to(Idle)
    Idle_to_Mission_5 = Idle.to(Mission_5)
    
    # Mission 5
    Mission_5_to_Idle = Mission_5.to(Idle)
    Idle_to_Scan = Idle.to(Scan)
    Scan_to_Object_Detection_Algorithm_1 = Scan.to(Object_Detection_Algorithm_1)
    Object_Detection_Algorithm_1_to_Movement = Object_Detection_Algorithm_1.to(Movement)
    Movement_to_Object_Detection_Algorithm_6 = Movement.to(Object_Detection_Algorithm_6)
    Object_Detection_Algorithm_6_to_Movement = Object_Detection_Algorithm_6.to(Movement)
    Movement_to_Grab = Movement.to(Grab)
    Grab_to_Movement = Grab.to(Movement)
    Movement_to_Release = Movement.to(Release)
    Release_to_Movement = Release.to(Movement)
    Movement_to_Idle = Movement.to(Idle)
    Idle_to_End = Idle.to(End)
    

if __name__ == '__main__':
    m = StateMachine()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/state_machine.png')