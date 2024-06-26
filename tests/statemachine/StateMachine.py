from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

class AUVStateMachine(StateMachine):
    # Define states
    idle = State('Idle', initial=True)
    start_position = State('Start Position')
    scanning_gate = State('Scanning Gate')
    traveling_to_gate = State('Traveling to Gate')
    scanning_side = State('Scanning Side')
    passing_through_gate = State('Passing Through Gate')
    rotating_yaw = State('Rotating Yaw')
    path_finding = State('Path Finding')
    following_path = State('Following Path')
    detecting_buoy = State('Detecting Buoy')
    touching_buoy = State('Touching Buoy')
    moving_past_buoy = State('Moving Past Buoy')
    locating_marker = State('Locating Marker')
    carrying_marker = State('Carrying Marker')
    placing_marker = State('Placing Marker')
    scanning_mission = State('Scanning Mission')
    firing_torpedo = State('Firing Torpedo')
    locating_prop = State('Locating Prop')
    moving_under_prop = State('Moving Under Prop')
    grabbing_prop = State('Grabbing Prop')
    releasing_prop = State('Releasing Prop')

    # Define transitions
    idle_to_start_position = idle.to(start_position)
    start_position_to_scanning_gate = start_position.to(scanning_gate)
    scanning_gate_to_traveling_to_gate = scanning_gate.to(traveling_to_gate)
    traveling_to_gate_to_scanning_side = traveling_to_gate.to(scanning_side)
    scanning_side_to_passing_through_gate = scanning_side.to(passing_through_gate)
    passing_through_gate_to_rotating_yaw = passing_through_gate.to(rotating_yaw)
    rotating_yaw_to_idle = rotating_yaw.to(idle)
    
    idle_to_path_finding = idle.to(path_finding)
    path_finding_to_following_path = path_finding.to(following_path)
    following_path_to_idle = following_path.to(idle)
    
    idle_to_detecting_buoy = idle.to(detecting_buoy)
    detecting_buoy_to_touching_buoy = detecting_buoy.to(touching_buoy)
    touching_buoy_to_moving_past_buoy = touching_buoy.to(moving_past_buoy)
    moving_past_buoy_to_idle = moving_past_buoy.to(idle)
    
    idle_to_locating_marker = idle.to(locating_marker)
    locating_marker_to_carrying_marker = locating_marker.to(carrying_marker)
    carrying_marker_to_placing_marker = carrying_marker.to(placing_marker)
    placing_marker_to_idle = placing_marker.to(idle)
    
    idle_to_scanning_mission = idle.to(scanning_mission)
    scanning_mission_to_firing_torpedo = scanning_mission.to(firing_torpedo)
    firing_torpedo_to_idle = firing_torpedo.to(idle)
    
    idle_to_locating_prop = idle.to(locating_prop)
    locating_prop_to_moving_under_prop = locating_prop.to(moving_under_prop)
    moving_under_prop_to_grabbing_prop = moving_under_prop.to(grabbing_prop)
    grabbing_prop_to_releasing_prop = grabbing_prop.to(releasing_prop)
    releasing_prop_to_idle = releasing_prop.to(idle)
    
    def on_enter_start_position(self):
        # Coin flip to determine the start position
        position = 'heads' if random.choice([True, False]) else 'tails'
        print(f"Starting position: {position}")
        self.start_position_to_scanning_gate()
    
    def on_enter_scanning_gate(self):
        # Use Object Detection Algorithm #1 to scan for the gate
        print("Scanning for gate using Object Detection Algorithm #1")
        gate_found = True  # Placeholder for actual detection result
        if gate_found:
            self.scanning_gate_to_traveling_to_gate()
    
    def on_enter_traveling_to_gate(self):
        # Travel to the gate using the movement package
        print("Traveling to gate using movement package")
        self.traveling_to_gate_to_scanning_side()
    
    def on_enter_scanning_side(self):
        # Use Object Detection Algorithm #2 to detect the correct side of the gate
        print("Scanning gate side using Object Detection Algorithm #2")
        side_found = True  # Placeholder for actual detection result
        if side_found:
            self.scanning_side_to_passing_through_gate()
    
    def on_enter_passing_through_gate(self):
        # Travel through the correct side of the gate using the movement package
        print("Passing through the gate")
        self.passing_through_gate_to_rotating_yaw()
    
    def on_enter_rotating_yaw(self):
        # Complete three rotations around the yaw direction
        print("Completing three rotations around the yaw direction")
        self.rotating_yaw_to_idle()
    
    def on_enter_path_finding(self):
        # Move using the Movement Package and Object Detection Algorithm #3
        print("Path finding using Object Detection Algorithm #3")
        path_found = True  # Placeholder for actual detection result
        if path_found:
            self.path_finding_to_following_path()
    
    def on_enter_following_path(self):
        # Follow the path outlined using the Movement Package
        print("Following path")
        self.following_path_to_idle()
    
    def on_enter_detecting_buoy(self):
        # Move forward until Object Detection Algorithm #1 detects the Red Buoy
        print("Detecting buoy using Object Detection Algorithm #1")
        buoy_detected = True  # Placeholder for actual detection result
        if buoy_detected:
            self.detecting_buoy_to_touching_buoy()
    
    def on_enter_touching_buoy(self):
        # Move towards the buoy until the arm touches it
        print("Touching buoy with arm")
        self.touching_buoy_to_moving_past_buoy()
    
    def on_enter_moving_past_buoy(self):
        # Move past the buoy and return to the idle state
        print("Moving past buoy")
        self.moving_past_buoy_to_idle()
    
    def on_enter_locating_marker(self):
        # Scan for the marker using Object Detection Algorithm #1
        print("Locating marker using Object Detection Algorithm #1")
        marker_found = True  # Placeholder for actual detection result
        if marker_found:
            self.locating_marker_to_carrying_marker()
    
    def on_enter_carrying_marker(self):
        # Carry the marker to the bin
        print("Carrying marker to the bin")
        self.carrying_marker_to_placing_marker()
    
    def on_enter_placing_marker(self):
        # Place the marker in the correct side of the bin
        print("Placing marker in the bin")
        self.placing_marker_to_idle()
    
    def on_enter_scanning_mission(self):
        # Scan for the mission using Object Detection Algorithm #1
        print("Scanning for mission using Object Detection Algorithm #1")
        mission_found = True  # Placeholder for actual detection result
        if mission_found:
            self.scanning_mission_to_firing_torpedo()
    
    def on_enter_firing_torpedo(self):
        # Fire torpedoes at the identified targets
        print("Firing torpedoes")
        self.firing_torpedo_to_idle()
    
    def on_enter_locating_prop(self):
        # Locate the prop using Object Detection Algorithm #1
        print("Locating prop using Object Detection Algorithm #1")
        prop_found = True  # Placeholder for actual detection result
        if prop_found:
            self.locating_prop_to_moving_under_prop()
    
    def on_enter_moving_under_prop(self):
        # Move under the prop
        print("Moving under prop")
        self.moving_under_prop_to_grabbing_prop()
    
    def on_enter_grabbing_prop(self):
        # Grab the prop
        print("Grabbing prop")
        self.grabbing_prop_to_releasing_prop()
    
    def on_enter_releasing_prop(self):
        # Release the prop in the collection basket
        print("Releasing prop in collection basket")
        self.releasing_prop_to_idle()

if __name__ == '__main__':
    m = AUVStateMachine()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/pngs/AUVStateMachine.png')
