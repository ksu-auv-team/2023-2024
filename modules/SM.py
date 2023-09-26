from statemachine import StateMachine, State

# st = sim_training
# rt = real_training
# mc = manual control
# as = autonomous_sequence
# sts = sim_training_sequence
# rts = real_training_sequence


class Submarine(StateMachine):
    idle = State(initial=True)
    autonomous = State()
    manual = State()
    sim_training = State()
    real_training = State()
    shutdown = State(final=True)
    emergency_shutdown = State(final=True)
    
    
    idle_transition = idle.to(autonomous, manual, sim_training, real_training, shutdown, emergency_shutdown)
    
    start_submarine = (
        idle.to(autonomous)#, cond="start_in_as")
        | idle.to(manual)#, cond="start_in_mc")
        | idle.to(sim_training)#, cond="start_in_sts")
        | idle.to(real_training)#, cond="start_in_rts")
    )
    
    manual_control = (
        idle.to(manual)#, cond="idle_to_mc_requested")
        | autonomous.to(manual)#, cond="as_to_mc_requested") #should we allow it? will make it easier to correct paths
        | sim_training.to(manual)#, cond="sts_to_ms_requested")
        | real_training.to(manual)#, cond="rts_to_ms_requested")
    )
    
    return_control = (
        manual.to(autonomous)
        | manual.to(sim_training)
        | manual.to(real_training)
    )
    
    competition_cycle = (
        idle.to(autonomous)
        | autonomous.to(idle)#, cond="all_tasks_complete")
    )
    
    power_off = (
        idle.to(shutdown)
        | manual.to(idle)
        | sim_training.to(idle)
        | real_training.to(idle)
        | autonomous.to(idle)
    )
    
    def before_cycle(self, event: str, source: State, target: State): #A.K.A before cycle / power on
        return
    
    def on_enter_idle(self):
        return
    
    def on_enter_autonomous(self):
        return
    
    def on_enter_manual(self):
        return
    
    def on_enter_sim_training(self):
        return
    
    def on_enter_real_training(self):
        return
    
    def on_enter_shutdown(self):
        return

    def on_exit_idle(self):
        print("Go ahead!")

sm = Submarine()
#img_path = 'C:\\Users\\Jack\\Desktop\\test.png'
#sm._graph().write_png(img_path)
