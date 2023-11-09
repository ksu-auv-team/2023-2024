from statemachine import StateMachine, State
# imported to handle the config file
import json
# used for the .sleep function for testing
import time

def mc_enabled() -> dict:
    f = open(__file__.split("modules")[0]+'configs\\sub.json')
    sub_config = json.load(f)
    f.close()
    # returning only the control bools so we can do some programming magic for advanced if statements
    return sub_config["manual_control"]

class Submarine(StateMachine):
    #Supreme States (can be access anywhere anytime no matter what)
    idle = State(initial=True) #Hover in place
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
        autonomous,
        manual,
        cond="default_enabled"
    )
    
    manual_control = manual.from_(
        autonomous, 
        idle, 
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
    
    return_manual_control = manual.to(
        autonomous, 
        idle, 
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
        | move_to_target.to(fire_torpedo)
        | fire_torpedo.to(find_stargate)
    )
    
    t4_cycle = (
        find_bin.to(find_marker)
        | position_towards_target.to(move_to_target)
        | move_to_target.to(open_bin, cond="found_bin") #only start moving to open_bin we are on that step (will have to hammer out a more solid detection system later)
        | open_bin.to(find_marker)
        
        | find_marker.to(position_towards_target)
        | move_to_target.to(pickup_marker, cond="found_marker") #only start moving to pickup_marker we are on that step (will have to hammer out a more solid detection system later)
        | pickup_marker.to(drop_marker)
        | drop_marker.to(check_bounds)
        | check_bounds.to(find_bin) #! we need to always make sure we are in the octagon
    )
    
    gate_cycle = (
        autonomous.to(find_gate)
        | find_gate.to(enter_gate)
        | enter_gate.to(follow_marker)
        
        | follow_marker.from_(
            touch_marker,
            drop_marker,
            fire_torpedo,
        )
        | follow_marker.to(find_bouy, before="set_t1")
        | follow_marker.to(find_bin, before="set_t2")
        | follow_marker.to(find_stargate, before="set_t3")
        | follow_marker.to(find_bin, before="set_t4")
    )
    
    set_idle = idle.from_(
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
    
    def __init__(self, *args, **kwargs):
        self.previous_state: str = "" # records the previous state
        self.time_start: float = 0.0 #records the time that the sub was turned on
        self.auto_time_start: float = 0.0 #records the time when the sub first entered autonomous mode
        self.task: int = 0 #what task number we are doing, corresponds to the task cycle, Ex self.task = 1 so we are on t1_cycle
        
        #? the targets of the robot
        self.gate: str = ... #this will hold what gate we want to go through #when we enter the gate, we want to set this to nothing or ...
        self.marker: str = ... #the marker that we have targeted 
        self.bin: object = ... #the bin we have targeted
        self.stargate: str = ... #the stargate that we have targeted
        
        #? does the robot have it?
        self.bin_opened: bool = False #whether the "self.bin_set" bin has been opened
        self.marker_possesed: bool = False #if the robot has a marker in hand
        
        #? has the robot released it?
        self.marker_dropped: bool = False #whether the marker in hand has been dropped #!(this variable may be subject a type to change)
        self.torpedo_count: int = 2 #how many torpedos are currently loaded (will keep track of how many were fired)
        
        #? how many times have we done this?
        self.t1_interation: int = 0
        self.t2_interation: int = 0
        self.t3_interation: int = 0
        self.t4_interation: int = 0
        
        self.in_bounds: bool = True #whether we were in bounds last time we checked
        
        super().__init__(*args, **kwargs)
   
    # before we switch to manual mode, record out last state so we can go back to it using "return_manual_control"
    def before_manual_control(self, event: str, source: State, target: State):
        print("checking for controller")
        controller = True
        
        if controller:
            print("controller found")
            self.previous_state = self.current_state.value
        else:
            print("controller not found")
            print("block state switch (using guards)")
      
    def on_enter_manual_control(self):
        print("connects controller")
        print("event listeners for controller input")
        return         
    
    def on_enter_idle(self):
        print("check diagnostics, right the sub, and return to the surface")
        return
    
    def on_enter_state(self, target, event, source):
        if not source:
            print(f"{event} enter: {target.value} from void")
            return
        print(f"{event} enter: {target.value} from {source.value}")
    
    # TRANSITIONS
    # the transition funtions MUST return a boolean
    
    def default_enabled(self, source, target) -> bool:        
        return mc_enabled() if target.id == "manual" else True
        
    def return_control(self, target):
        #get the currently requestion state transition (as to mc, idle to mc, etc. as tell whether its most previous state was that)
        #the idea is that if the previous state was move_to_target, then if the transition that is being requested is that, then approve.
        #so we don't have 50 billion functions all doing the same thing slightly differently
        return True if target.id == self.previous_state else False
    
    def found_bin(self):
        return True if self.bin else False
    
    def found_marker(self):
        return True if self.marker else False
    
    #? compress these 4 functions into 1 if possible
    def set_t1(self):
        self.task = 1
        
    def set_t2(self):
        self.task = 2
        
    def set_t3(self):
        self.task = 3
        
    def set_t4(self):
        self.task = 4

sm = Submarine()
sm.start_submarine()