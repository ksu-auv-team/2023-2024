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
    idle = State(initial=True)
    autonomous = State()
    manual = State()
    sim_training = State()
    real_training = State()
    shutdown = State(final=True)
    
    search_for_target = State() # search for the target
    target_found = State() # calculate the distance, angle, elevation, and other stats to get to the target
    position_towards_target = State() # position itself towards the target
    move_to_target = State() # move to the target
    execute_task = State() # has gotten the target
    
    start_submarine = (
        idle.to(autonomous, cond="as_enabled")
        | idle.to(manual, cond="mc_enabled")
        | idle.to(sim_training, cond="sts_enabled")
        | idle.to(real_training, cond="rts_enabled")
    )
    
    manual_control = manual.from_(
        autonomous, 
        idle, 
        sim_training, 
        real_training, 
        search_for_target, 
        target_found, 
        position_towards_target, 
        move_to_target, 
        execute_task
    )
    
    return_manual_control = (
        manual.to(autonomous, cond="as_from_mc")
        | manual.to(sim_training, cond="sts_from_mc")
        | manual.to(real_training, cond="rts_from_mc")
        | manual.to(search_for_target) # removed for now since idk about saving data
        # | manual.to(target_found)
        # | manual.to(position_towards_target)
        # | manual.to(move_to_target)
        # | manual.to(execute_task)
    )
    
    mission_cycle = (
        autonomous.to(search_for_target)
        | sim_training.to(search_for_target)
        | real_training.to(search_for_target)
        | search_for_target.to(target_found, after="mission_cycle")
        | target_found.to(position_towards_target, after="mission_cycle")
        | position_towards_target.to(move_to_target, after="mission_cycle")
        | move_to_target.to(execute_task, after="mission_cycle")
        | execute_task.to(search_for_target)
    )
    
    set_idle = idle.from_(
        autonomous, 
        manual, 
        sim_training, 
        real_training, 
        search_for_target, 
        target_found, 
        position_towards_target, 
        move_to_target, 
        execute_task
    )
    
    power_off = shutdown.from_(
        idle,
        autonomous, 
        manual, 
        sim_training, 
        real_training, 
        search_for_target, 
        target_found, 
        position_towards_target, 
        move_to_target, 
        execute_task
    )
    
    def __init__(self, *args, **kwargs):
        self.previous_state = ... # record out previous state
        self.current_position = {"x":0, "y":0, "z":0, "alpha":0, "beta":0, "gama":0} #? https://en.wikipedia.org/wiki/Euler_angles
        self.target_position_difference = {"x":0, "y":0, "z":0, "alpha":0, "beta":0, "gama":0}
        self.target_position_list = list(self.target_position_difference.values())
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
        
    def as_from_mc(self):
        if self.previous_state == "autonomous":
            return True
        return False

    def sts_from_mc(self):
        if self.previous_state == "sim_training":
            return True
        return False
    
    def rts_from_mc(self):
        if self.previous_state == "real_training":
            return True
        return False
