from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine
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
        | search_for_target.to(target_found)
        | target_found.to(position_towards_target)
        | position_towards_target.to(move_to_target)
        | move_to_target.to(execute_task)
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
        self.target_position_list = list(self.target_position_dict.values())
        super().__init__(*args, **kwargs)
        
    # before we switch to manual mode, record out last state so we can go back to it using "return_manual_control"
    def before_manual_control(self, event: str, source: State, target: State):
        self.previous_state = self.current_state.value
    
    def on_enter_state(self, target, event):
        print(f"{self.name} enter: {target.id} from {event}")
    
    # def on_enter_autonomous(self):
    #     self.asm = Submarine.AutonomousMode(self)
    #     return self.asm
    
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
    
    # class AutonomousMode(StateMachine):
    #     search_for_target = State(initial=True) # search for the target
    #     target_found = State() # calculate the distance, angle, elevation, and other stats to get to the target
    #     position_towards_target = State() # position itself towards the target
    #     move_to_target = State() # move to the target
    #     execute_task = State() # has gotten the target
        
    #     mission_cycle = (
    #         search_for_target.to(target_found)
    #         | target_found.to(position_towards_target)
    #         | position_towards_target.to(move_to_target)
    #         | move_to_target.to(execute_task)
    #         | execute_task.to(search_for_target)
    #     )
        
    #     def __init__(self, submarine_instance):
