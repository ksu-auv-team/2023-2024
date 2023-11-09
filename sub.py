from statemachine import StateMachine, State
# imported to handle the config file
import json
# used for the .sleep function for testing
import time

import modules.CM as cm
import modules.CO as co

def mc_enabled() -> dict:
    f = open(__file__.split("modules")[0]+'configs\\sub.json')
    sub_config = json.load(f)
    f.close()
    # returning only the control bools so we can do some programming magic for advanced if statements
    return sub_config["manual_control"]

class Submarine(StateMachine):
    #Supreme States (can be access anywhere anytime no matter what)
    idle = State(initial=True) #on, but does nothing (basically shutdown, but it doesn't power anything off)
    hover = State() #Hover in place
    autonomous = State() #Broad name for the standard auto state switching, might remove this state in the future
    manual = State() #Manual controller control
    surface = State() #Check gyroscope and orient itself correctly then surface
    shutdown = State(final=True) #Turn off sub (this does not surface the sub)
    
    find_gate = State() #find the gate we want to go through
    enter_gate = State() #go through the gate we previously targeted
    follow_marker = State() #Follow the markers on the ground
    position_towards_target = State() # position itself towards the target
    move_to_target = State() # move to the target
    
    #? task depends on what gate is choosen
    #Task 1: [4 iterations per task assignment], (aka do this 4 times every time we are assigned to do this task)
    find_bouy = State() #finds the correct bouy that has the desired marker (will have to be done 4 times)
    touch_marker = State() #Touch the markers that match which side of that gate you choose
    
    #Task 2: [2 iterations per task assignment]
    find_bin = State()# finds the bin that needs to be opened to drop a marker into it
    open_bin = State()
    drop_marker = State() #Drop a marker into the bin
    
    #Task 3: [2 iterations per task assignment]
    find_stargate = State()
    fire_torpedo = State() #fires a torpedo into a stargate, more points if the stargate is open than closed (make check to identify)

    #Task 4: [X iterations per task assignment]
    find_marker = State() #finds the marker that needs to be picked up
    pickup_marker = State() #picks up the marker
    check_bounds = State() #checks if it is within bound of the course (set octagon for task 4) #! State may be subject to removal
    #?Repeat states from task 2
    
    start_submarine = idle.to(
        hover,
        manual,
        cond="control_mode"
    )
    
    manual_control = manual.from_(
        idle,
        autonomous, 
        hover, 
        surface,
        follow_marker,
        position_towards_target,
        move_to_target,
        find_bouy,
        touch_marker,
        find_marker,
        pickup_marker,
        check_bounds,
        find_stargate,
        fire_torpedo,
        find_bin,
        open_bin,
        drop_marker,
        cond="controller_connected"
    )
    
    return_manual_control = manual.to(
        idle,
        autonomous, 
        hover, 
        surface,
        follow_marker,
        position_towards_target,
        move_to_target,
        find_bouy,
        touch_marker,
        find_marker,
        pickup_marker,
        check_bounds,
        find_stargate,
        fire_torpedo,
        find_bin,
        open_bin,
        drop_marker,
        cond="return_control"
    )
    
    t1_cycle = (
        find_bouy.to(position_towards_target) #find the target bouy
        | position_towards_target.to(move_to_target) #position ourselves towards the targeted bouy
        | move_to_target.to(touch_marker) #move towards the targeted bouy
        | touch_marker.to(find_bouy) #touch the correct side of the bouy
    )
    
    t2_cycle = (
        find_bin.to(position_towards_target) #find our target bin
        | position_towards_target.to(move_to_target) #position ourselves towards the targeted bin
        | move_to_target.to(open_bin) #move towards our targeted bin
        | open_bin.to(open_bin) #open the targeted bin
        | drop_marker.to(find_bin) #drop the marker into the bin, if we have another iteration, then go back to finding the next bin
    )
    
    t3_cycle = (
        find_stargate.to(position_towards_target)
        | position_towards_target.to(move_to_target)
        | move_to_target.to(fire_torpedo, cond="has_torpedo")
        | fire_torpedo.to(find_stargate)
    )
    
    t4_cycle = (
        find_bin.to(find_marker)
        | find_marker.to(position_towards_target)
        | position_towards_target.to(move_to_target)
        | move_to_target.to(open_bin, cond="found_bin") #only start moving to open_bin we are on that step (will have to hammer out a more solid detection system later)
        | open_bin.to(find_marker)
        
        | move_to_target.to(pickup_marker, cond="found_marker") #only start moving to pickup_marker we are on that step (will have to hammer out a more solid detection system later)
        | pickup_marker.to(drop_marker, cond="has_marker")
        | drop_marker.to(check_bounds)
        | check_bounds.to(find_bin) # we need to always make sure we are in the octagon
    )
    
    gate_cycle = (
        autonomous.to(find_gate)
        | find_gate.to(enter_gate)
        | enter_gate.to(follow_marker)
        
        | follow_marker.from_(
            touch_marker,
            drop_marker,
            fire_torpedo,
            #!set a thing that records the gate that was just completed, 
            #! this can be done with a condition that always returns true or we can try guards
        )
        | follow_marker.to(find_bouy, before="set_t1")
        | follow_marker.to(find_bin, before="set_t2")
        | follow_marker.to(find_stargate, before="set_t3")
        | follow_marker.to(find_bin, before="set_t4")
    )
    
    set_hover = hover.from_(
        idle,
        autonomous, 
        manual, 
        surface,
        follow_marker,
        position_towards_target,
        move_to_target,
        find_bouy,
        touch_marker,
        find_marker,
        pickup_marker,
        check_bounds,
        find_stargate,
        fire_torpedo,
        find_bin,
        open_bin,
        drop_marker,
    )
    
    to_surface = surface.from_(
        idle,
        hover,
        autonomous, 
        manual, 
        follow_marker,
        position_towards_target,
        move_to_target,
        find_bouy,
        touch_marker,
        find_marker,
        pickup_marker,
        check_bounds,
        find_stargate,
        fire_torpedo,
        find_bin,
        open_bin,
        drop_marker,
    )
    
    power_off = shutdown.from_(
        idle,
        hover,
        autonomous, 
        manual, 
        surface,
        follow_marker,
        position_towards_target,
        move_to_target,
        find_bouy,
        touch_marker,
        find_marker,
        pickup_marker,
        check_bounds,
        find_stargate,
        fire_torpedo,
        find_bin,
        open_bin,
        drop_marker,
    )
    
    def __init__(self, controller: cm.CM = False, *args, **kwargs):
        self.controller: cm.CM = controller #the object in which we will be getting all our controller data, probably cm.get_data()
        
        self.previous_state: str = "" # records the previous state
        self.time_start: float = time.time() #records the time that the sub was turned on
        self.auto_time_start: float = 0.0 #records the time when the sub first entered autonomous mode
        self.task: int = 0 #what task number we are doing, corresponds to the task cycle, Ex self.task = 1 so we are on t1_cycle
        
        #? all the objects the robot will be interacting with
        #they can also all be False booleans, this is for easy if statements
        self.gate: co.Gate = ... #this will hold what gate we want to go through #when we enter the gate, we want to set this to nothing or ...
        self.marker: co.Marker = ... #the marker that we have targeted 
        self.bin: co.Bin = ... #the bin we have targeted
        self.stargate: co.Stargate = ... #the stargate that we have targeted
        
        #? has the robot released it?
        self.torpedo_count: int = 2 #how many torpedos are currently loaded (will keep track of how many were fired)
        
        #? how many times have we done this?
        self.t1_interation: int = 0 #max is 4
        self.t2_interation: int = 0 #max is 2
        self.t3_interation: int = 0 #max is 2
        self.t4_interation: int = 0 #max is unknown
        
        self.markers_completed: list = [] #a list of all markers touched or otherwise completed during the current task cycle
        self.gates_completed: list = [] #a list of all gate symbols we have gone through (hopefully can keep track of the areas we've been to)
        self.in_bounds: bool = True #whether we were in bounds last time we checked
        
        super().__init__(*args, **kwargs)
        
    def on_enter_state(self, target, event, source):
        #at the beginning we move from __init__ state to the hover state in which source is null and will error us, 
        # so we just check and say its void if we cant find a source
        if not source:
            print(f"{event} enter: {target.value} from void") #log this
            return
        print(f"{event} enter: {target.value} from {source.value}") #log this
   
    # before we switch to manual mode, record out last state so we can go back to it using "return_manual_control"
    def before_manual_control(self, event: str, source: State, target: State):
        if self.controller:
            self.previous_state = self.current_state.value
        else:
            #! send error to GCS (surface.py) console (if its hooked up) & log it
            pass
    
    def on_enter_manual_control(self):
        f'X: {self.data[0]} | Y: {self.data[1]} | Z: {self.data[2]} | Roll: {self.data[3]} | Yaw: {self.data[4]} | Pitch: {self.data[5]}'
        return
    
    def on_enter_hover(self):
        #proceed to hover the submarine (and orient it correctly if needed)
        #! this shouldn't need an AI to do
        return
    
    def on_enter_surface(self):
        #proceed to surface the submarine (and orient it correctly if needed)
        #! this might need AI for object avoidence if we choose to do so
        return
    
    def after_touch_marker(self):
        self.t1_interation += 1
        
        if self.t1_interation >= 4:
            self.markers_completed = []
            #! move to next task / gate cycle
    
    def after_drop_marker(self, event):
        self.marker = False
        
        if event == "t2_cycle":
            self.t2_interation += 1
            
            if self.t2_interation >= 2:
                #! move to next task / gate cycle
                return
            
        elif event == "t4_cycle":
            self.t4_interation += 1
        
    def after_fire_torpedo(self):
        self.torpedo_count -= 1
        self.t3_interation += 1 #attempted an iteration? we have limited torpedos so i'll just count it for now
                                #! might need an AI so we can tell if the torpedo went in or not, therefore we 
                                #! can intelligently decide whether to iterate the task or not
        
        if self.t3_interation >= 2:
            #! move to next task / gate cycle
            return
    
    #? TRANSITIONS
    # the transition funtions MUST return a boolean
    def controller_connected(self) -> bool:
        #check if self.controller has a controller connected to it, also make sure that its not just a true value bool :)
        return True if self.controller and type(self.controller) == cm.CM else False
    
    def control_mode(self, source, target) -> bool:     
        if target.id == "manual" and self.controller and mc_enabled():
            return True
        elif target.id == "hover":
            self.auto_time_start = time.time()
            return True
        return False
        
    def return_control(self, target) -> bool:
        if target.id == self.previous_state:
            self.auto_time_start = time.time()
            return True
        return False
    
    def found_bin(self) -> bool:
        return True if self.bin else False
    
    def found_marker(self) -> bool:
        return True if self.marker else False
    
    def has_torpedo(self, source, target) -> bool:
        return True if self.torpedo_count > 0 else False
    
    def has_marker(self, source, target) -> bool:
        return True if self.marker else False
    
    #? compress these 4 functions into 1 if possible
    def set_t1(self) -> None:
        self.task = 1
        
    def set_t2(self) -> None:
        self.task = 2
        
    def set_t3(self) -> None:
        self.task = 3
        
    def set_t4(self) -> None:
        self.task = 4

    #? FUNCTIONS
    def set_controller(self, controller: cm.CM) -> None:
        #made so the GCS can (hopefully) remotely set up a controller after the sub has already been started
        self.controller = controller

sm = Submarine()