from statemachine import StateMachine, State
# imported to handle the config file
import json
# used for the .sleep function for testing
import time

# st = sim_training
# rt = real_training
# mc = manual control
# as = autonomous_sequence
# sts = sim_training_sequence
# rts = real_training_sequence

def get_control_bools() -> dict:
    f = open(__file__.split("modules")[0]+'configs\\config.json')
    config = json.load(f)
    gcs_config = config["GCS"]
    f.close()
    # returning only the control bools so we can do some programming magic for advanced if statements
    return {"manual_control": gcs_config["manual_control"], 
            "autonomous_control":gcs_config["autonomous_control"], 
            "sim_training":gcs_config["training_sim"], 
            "real_training":gcs_config["training_real_world"]
            }

class Submarine(StateMachine):
    idle = State(initial=True) #Hover in place
    autonomous = State() #
    manual = State()
    shutdown = State(final=True)
    
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
    
    start_submarine = (
        idle.to(autonomous, cond="as_enabled")
        | idle.to(manual, cond="mc_enabled")
    )
    
    manual_control = manual.from_(
        autonomous, 
        idle, 
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
    
    return_manual_control = (
        manual.to(autonomous, cond="as_from_mc")
    )
    
    gate_cycle(
        autonomous.to(follow_marker)
        | follow_marker.from_(
            touch_marker,
            drop_marker,
            fire_torpedo,
        )
        | follow_marker.to(t1_cycle, cond="")
        | follow_marker.to(t2_cycle, cond="")
        | follow_marker.to(t3_cycle, cond="")
        | follow_marker.to(t4_cycle, cond="")
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
        | move_to_target.to(open_bin, cond="self.bin") #only start moving to open_bin we are on that step (will have to hammer out a more solid detection system later)
        | open_bin.to(find_marker)
        
        | find_marker.to(position_towards_target)
        | move_to_target.to(pickup_marker, cond="self.marker") #only start moving to pickup_marker we are on that step (will have to hammer out a more solid detection system later)
        | pickup_marker.to(drop_marker)
        | drop_marker.to(find_bin)
        # | check_bounds.to() #! we need to always make sure we are in the octagon
    )
    
    set_idle = idle.from_(
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
        
        #? the robots targets (they might become strings instead of objects later)
        self.gate: object = ... #this will hold what gate we want to go through #when we enter the gate, we want to set this to nothing or ...
        self.marker: object = ... #the marker that we have targeted 
        self.bin: object = ... #the bin we have targeted
        self.stargate: object = ... #the stargate that we have targeted
        
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
        
        self.in_bounds: bool = False #whether we were in bounds last time we checked
        
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
    
    # record last state before switching
    def before_enter_autonomous_sequence(self):
        print("checking for camera")
        camera = True
        
        if camera:
            print("Camera found, entering autonomous mode")
            self.previous_state = self.current_state.value
        else:
            print("camera not found")
            print("block state switch (using guards)")
        return
    
    def on_enter_autonomous_sequence(self):
        print("feed zed camera image into AI")
        print("AI searches database of images")
        print("AI uses diagnostics and then controls the movement of the sub")
        return 
    
    def on_enter_idle(self):
        print("check diagnostics, right the sub, and return to the surface")
        return
    
    # record last state before switching 
    def before_enter_simulation_training(self):
        print("checking for simulation environment")
        inSimulationEnvironment = True
        
        if inSimulationEnvironment:
            print("correct environment for simulation training")
            print("commencing simulation")
            self.previous_state = self.current_state.value
        else:
            print("incorrect environment")
            print("block state switch (using guards)")
        return
    
    def on_enter_simulation_training(self):
        print("run unity simulation in tandem with GCS and diagnostics")
        print("allow for manual control input")
        print("pass diagnostic info to unity sim")
        print("pass relevent unity sim training feedback to GCS and SM")
        print("record info from sim training")
        return
    
    def before_enter_simulation_training_sequence(self):
        print("sts transition is only available if currently in st")
        return
    
    def on_enter_simulation_training_sequence(self):
        print("perform sequence")
        print("pass in-simulation info to AI for learning")
        print("record camera data")
                
        print("when the sequence finishes, return to simulation training")
        return
    
    def before_enter_real_training(self):
        print("Ask user whether real training will be commenced with manual or autonomous control")
        print("buttons for both in GCS")
        controlType = input("Commence with Manual or Autonomous control?")
        
        if controlType == "Manual":
            print("run 'before_enter_manual_control'")
            
            if self.current_state.value == 'Manual':
                print("run manual real training program")
                
        elif controlType == "Autonomous":
            print("run 'before_enter_autonomous_control'")
            
            if self.current_state.value == 'Autonomous':
                print("run autonomous real training program")
        return
    
    def on_enter_autonomous_real_training(self):
        # unsure of what this looks like
        return
    
    def on_enter_manual_real_training(self):
        # unsure of what this looks like
        return
    
    def before_enter_real_training_sequence(self):
        print("rts transition is only available if currently in autonomous rt")
        return
    
    def on_enter_real_training_sequence(self):
        print("perform sequence")
        print("pass in-simulation info to AI for learning")
        print("record camera data")
                
        print("when the sequence finishes, return to simulation training")
        return
    
    def on_enter_state(self, target, event):
        print(f"{self.name} enter: {target.id} from {event}")
    
    # TRANSITIONS
    # the transition funtions MUST return a boolean
    
    def as_enabled(self) -> bool:
        if dict(get_control_bools())["autonomous_control"]:
            return True
        return False    
    
    def mc_enabled(self, target, event) -> bool:
        # made a varibale here just so we dont open and close the file multiple times
        control_bools = get_control_bools()
        # what `any(list(control_bools.values()))` does is it checks all the control settings and checks if ANY of them are true, 
        # if at least one is true then it will return true, otherwise false. We do this so the robot will default manual mode if no mode is selected
        if dict(control_bools)["manual_control"] or not any(list(control_bools.values())):
            return True
        return False
    
    def sts_enabled(self) -> bool:
        if dict(get_control_bools())["sim_training"]:
            return True
        return False
    
    def rts_enabled(self) -> bool:
        if dict(get_control_bools())["real_training"]:
            return True
        return False
        
    def return_control(self):
        #get the currently requestion state transition (as to mc, idle to mc, etc. as tell whether its most previous state was that)
        #the idea is that if the previous state was move_to_target, then if the transition that is being requested is that, then approve.
        #so we don't have 50 billion functions all doing the same thing slightly differently
        
        return False
    
    def as_from_mc(self):
        if self.previous_state == "autonomous":
            return True
        return False
