
# ================= TODO =================

#TODO: Correct the position of the variable settings widgets
#TODO: Add pwm graph

#TODO: Connect the terminal to actual eletrical warnings
#TODO: Properly handle camera (currently taking live feed when it will really just be getting a numpy array)
#TODO: Add / Handle Depth Camera
#TODO: Add / Handle Sonar
#TODO: Add / Handle Controller
#TODO: Add / Handle Buttons


# ================= IMPORTS =================

# imported as our main GUI library
import tkinter as tk
import tkinter.ttk as ttk
# imported so we can pull images from cameras
import cv2
# so we can run the video streaming and the program itself without any noticable lag
import threading
# imported to handle images
from PIL import ImageTk, Image
# imported to handle the config file
import json
# imported for the orin ssh connection
import fabric
# imported for time stamps
from datetime import datetime
# imported for improved startup times
import asyncio
# added for the spacebar shutdown hotkey
import keyboard
#imported for camera
import numpy as np


# ================= CONFIG =================
config_file = __file__.split("2024")[0]+'2024\\configs\\'
f = open(config_file+"surface.json", 'r')
surface_config = json.load(f)

COMPONENTS = surface_config["ROBOT"]
ICO_PATH = __file__.split("2024")[0]+"2024\\"+surface_config["ASSETS"]["ICO_PATH"]
PNG_PATH = __file__.split("2024")[0]+"2024\\"+surface_config["ASSETS"]["PNG_PATH"]
auto_navigate_error = surface_config["ERRORS"]["auto_navigate"]

f.close()

f = open(config_file+"sub.json", 'r')
sub_config = json.load(f)
f.close()

# ============ NON APP SPECIFIC VARIABLES ============

#INPUTS
web_camera_input = ... #cv2.VideoCapture(0) #temp pulls straight from camera since no official input exists yet
depth_camera_input = ...
button_input = ...
controller_input = ...
sonar_input = ...

#SSH
ssh_connection = ...
robot_active = False


#! ==================== TO BE REMOVED ====================

#? only needed if we dont compile the gcs
import ctypes
myappid = 'ksu.clubs.auv.gcs' # arbitrary string that just defines pythonw.exe as a host
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#? imported for time benchmarks
import time


# ============ OTHER FUNCTIONS ============

def get_fps(recorded_times):
    fps = 0
    for t in recorded_times:
        fps += t
    return 1/(fps/len(recorded_times))
            

# ================= WINDOW =================

class GCSApp:
    def __init__(self, WINDOW):
        # SUB ENVIORMENT STATS
        self.depth: int = tk.IntVar()
        self.humidity: int = tk.IntVar()
        self.tube_temp: int = tk.IntVar()
        self.orin_temp: int = tk.IntVar()

        # ORIN
        self.orin_host: str = tk.StringVar(value="rasberrypi.local")
        self.orin_port: int = tk.IntVar(value=22)
        self.orin_user: str = tk.StringVar(value="user")
        self.orin_pass: str = tk.StringVar(value="pass")
        
        # ORIN CURRENTLY CONNECTED TO
        self.connected_host = 0
        self.connected_port = 0

        # TOGGLES
        self.orin_connected: bool = False
        
        #VARIABLE SETTINGS
        self.variable_settings = {}
        
        #DEV STATS
        self.time_last = time.time()
        self.recorded_times = []
        
        # ================= WINDOW SETTINGS =================
        
        WINDOW.title()
        WINDOW.title("Ground Control Station")
        WINDOW.state('zoomed')
        WINDOW.wm_iconbitmap(ICO_PATH) #Top left icon picture
        #WINDOW.iconphoto(True, tk.PhotoImage(file=PNG_PATH))
        
        #Setting sizes
        WINDOW.columnconfigure(
            2, 
            weight=1, 
            minsize=200
        )
        WINDOW.rowconfigure(
            1, 
            weight=1, 
            minsize=100, 
            uniform = 
            'row'
        )
        WINDOW.rowconfigure(
            [0,3], 
            weight=1, 
            minsize=100, 
            uniform = 'row'
        )
        
        
        # ================= HOTKEY SETTINGS =================
        
        keyboard.add_hotkey(
            hotkey="space", 
            callback=self.stop_sub_program
        )
        
        # ================= FRAME CREATION =================
        
        self.video_frame = tk.Frame(WINDOW)
        self.video_frame["bg"] = "black"
        self.video_frame.grid(
            row = 0, 
            column = 1, 
            rowspan=3, 
            columnspan=3, 
            sticky = "nsew", 
            padx=1, 
            pady=1
        )
        
        self.data_display_frame = tk.Frame(WINDOW)
        self.data_display_frame["bg"] = "black"
        self.data_display_frame.columnconfigure([0, 1], weight=1)
        self.data_display_frame.grid(
            row = 0, 
            column = 0, 
            rowspan = 4, 
            sticky = "nsew", 
            ipadx=15
        )
        
        self.sonar_frame = tk.Frame(WINDOW)
        self.sonar_frame["bg"] = "black"
        #self.sonar_frame.columnconfigure(0, weight=1, uniform="right_col")
        self.sonar_frame.grid(
            row = 0, 
            column = 4, 
            sticky="nsew"
        )
        
        self.graph_frame = tk.Frame(WINDOW)
        self.graph_frame["bg"] = "black"
        #self.graph_frame.columnconfigure(0, weight=1, uniform="right_col")
        self.graph_frame.grid(
            row = 1, 
            column = 4, 
            sticky="nsew", 
            pady=1
        )
        
        self.orin_frame = tk.Frame(WINDOW)
        self.orin_frame["bg"] = "black"
        self.orin_frame.columnconfigure([0, 1], weight=1, minsize=50, uniform="right_col")
        self.orin_frame.grid(
            row = 2, 
            column = 4, 
            sticky = "nsew"
        )
        
        self.mode_selection_frame = tk.Frame(WINDOW)
        self.mode_selection_frame["bg"] = "black"
        self.mode_selection_frame.columnconfigure([0, 1], weight=1)
        self.mode_selection_frame.grid(
            row = 3, 
            column = 4, 
            rowspan = 1, 
            sticky = "nsew"
        )
        
        self.indicator_frame = tk.Frame(WINDOW)
        self.indicator_frame["bg"] = "black"
        self.indicator_frame.columnconfigure([0, 1], weight=1, minsize=20, uniform="col")
        self.indicator_frame.grid(
            row = 3, 
            column = 1, 
            sticky="nsew", 
            padx=1
        )
        
        self.console_frame = tk.Frame(WINDOW)
        self.console_frame["bg"] = "black"
        self.console_frame.grid(
            row = 3, 
            column = 2, 
            columnspan=1,
            sticky="nsew"
        )
        self.console_frame.columnconfigure(0, weight=1)
        self.console_frame.rowconfigure(0, weight=1)
        
        self.button_frame = tk.Frame(WINDOW)
        self.button_frame["bg"] = "black"
        self.button_frame.grid(
            row = 3, 
            column = 3, 
            rowspan=1, 
            columnspan=1, 
            sticky = "nsew", 
            padx=1
        )
        
        # ================= WEIDGET CREATION =================
        
        # VIDEO FRAME WIDGETS
        self.video_display = tk.Label(self.video_frame)
        self.video_display.grid(sticky = "nsew", rowspan = 3, columnspan = 2)

        # DATA DISPLAY
        self.data_combobox = ttk.Combobox(self.data_display_frame)
        self.data_combobox['state'] = "readonly"
        self.data_combobox.grid(
            row = 0,
            column = 0,
            columnspan= 2,
            stick = "nsew",
            padx = 5,
            pady = 5
        )
        self.data_combobox.bind('<<ComboboxSelected>>', self.combobox_update) #bind combobox changed event
        
        self.components = {} #create a dictionary list of all components, so it can be easily accessed after being created dynamically

        for k, dictionary in COMPONENTS.items():
            #since the values of the combobox were not default set, tkinter sets the values paramater as a string instead of a tuple like it's supposed to be (wtf tkinter)
            #so we have to account for it being a string instead of just concating a tuple
            if type(self.data_combobox["values"]) == str:
                self.data_combobox["values"] = (k,)
            else:
                self.data_combobox["values"] += (k,)
            
            count = dictionary["COUNT"]
            
            #set the list of components for this subsystem as blank since it will give us an error if it doesn't exist
            self.components[k] = []
            
            #the row number that the current tk object should be created on
            rowcount = 1 #default to 1 because the combo box is row 0
            
            for n in range(count):
                #the reason we dont set the value_objects here is because they must be dynamically created, so it is created below...
                self.components[k].append(
                    self.Component(name=k,
                        label_object=tk.Label(self.data_display_frame), 
                    )
                )         
                
                #assign the just created component to a variable so we can edit it
                component = self.components[k][-1]
                
                component.label_object["text"] = dictionary["NAME"]+" "+str(n+1)+":"
                component.label_object["font"] = "Helvetica 10 bold"
                component.label_object["bg"] = "black"
                component.label_object["fg"] = "limegreen"
                component.label_object.grid(
                    row = rowcount, 
                    column=0, 
                    columnspan = 2,
                    sticky = "nsew", 
                    padx = 5, 
                    pady = 5
                )
                #this will turn the label_object invisible while still having tkinter remember its position
                component.label_object.grid_remove()
                
                #increase the row count because the component name label was just created
                rowcount += 1
                
                for stat, stat_type in dictionary["RECORDING"].items():
                    #properly create the recording dictionary that can use either IntVar, DoubleVar, or StringVar
                    if stat_type == "int":
                        component.recording[stat] = tk.IntVar(value = 1)
                    elif stat_type == "float":
                        component.recording[stat] = tk.DoubleVar(value = 1.23)
                    else:
                        #if some idiot ever forgets to put a stat type, then raise an exception to tell them
                        raise TypeError("TypeError: missing subsytem recorded value type")
                    
                    #create a label and value holder for each stat that is to be recorded for the component
                    component.value_objects[stat] = [tk.Label(self.data_display_frame), tk.Label(self.data_display_frame)]
                    label = component.value_objects[stat][0]
                    value = component.value_objects[stat][1]
                    
                    label["text"] = stat
                    label["bg"] = "black"
                    label["fg"] = "white"
                    label.grid(
                        row = rowcount, 
                        column=0, 
                        sticky = "e", 
                        padx = 5, 
                        pady = 5
                    )
                    label.grid_remove()
                    
                    value["textvariable"] = component.recording[stat]
                    value["bg"] = "black"
                    value["fg"] = "white"
                    value.grid(
                        row = rowcount, 
                        column=1, 
                        sticky = "w", 
                        padx = 5, 
                        pady = 5
                    )
                    value.grid_remove()
                    
                    rowcount += 2
        
        #? SONAR WIDGETS
        self.sonar_display = tk.Label(self.sonar_frame)
        #python will clear the image data right after its opened so we have to use a variable to store that data so we can display it
        #!self.sonar_image = ImageTk.PhotoImage(Image.open(SONAR_IMAGE))
        #!self.sonar_display["image"] = self.sonar_image
        self.sonar_display["bd"] = 0
        self.sonar_display.grid(
            sticky = "nsew",
            padx = 5,
            pady = 2
        )
        
        #? GRAPH WIDGETS
        self.graph_display = tk.Label(self.graph_frame)
        #!self.graph_image = ImageTk.PhotoImage(Image.open(GRAPH_IMAGE))
        #!self.graph_display["image"] = self.graph_image
        self.graph_display["bd"] = 0
        self.graph_display.grid(
            sticky = "nsew"
        )
        
        #? ORIN FRAME WIDGETS
        self.orin_label = tk.Label(self.orin_frame)
        self.orin_label["text"] = "ORIN CONNECTION"
        self.orin_label["font"] = "Helvetica 12 bold"
        self.orin_label["bg"] = "black"
        self.orin_label["fg"] = "white"
        self.orin_label.grid(
            row = 0, 
            column=0, 
            columnspan=4,
            sticky = "nsew", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_user_label = tk.Label(self.orin_frame)
        self.orin_user_label["text"] = "Username"
        self.orin_user_label["bg"] = "black"
        self.orin_user_label["fg"] = "white"
        self.orin_user_label.grid(
            row = 1, 
            column=0, 
            sticky = "e", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_user_input = tk.Entry(self.orin_frame)
        self.orin_user_input["textvariable"] = self.orin_user
        self.orin_user_input.grid(
            row = 1, 
            column=1, 
            columnspan=3,
            sticky = "nsew", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_pass_label = tk.Label(self.orin_frame)
        self.orin_pass_label["text"] = "Password"
        self.orin_pass_label["bg"] = "black"
        self.orin_pass_label["fg"] = "white"
        self.orin_pass_label.grid(
            row = 2, 
            column=0, 
            sticky = "e", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_pass_input = tk.Entry(self.orin_frame)
        self.orin_pass_input["show"] = "*"
        self.orin_pass_input["textvariable"] = self.orin_pass
        self.orin_pass_input.grid(
            row = 2, 
            column=1, 
            columnspan=3,
            sticky = "nsew", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_host_label = tk.Label(self.orin_frame)
        self.orin_host_label["text"] = "Host"
        self.orin_host_label["bg"] = "black"
        self.orin_host_label["fg"] = "white"
        self.orin_host_label.grid(
            row = 3, 
            column=0, 
            sticky = "e", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_host_input = tk.Entry(self.orin_frame)
        self.orin_host_input["textvariable"] = self.orin_host
        self.orin_host_input.grid(
            row = 3, 
            column=1, 
            columnspan=3,
            sticky = "nsew", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_port_label = tk.Label(self.orin_frame)
        self.orin_port_label["text"] = "Port"
        self.orin_port_label["bg"] = "black"
        self.orin_port_label["fg"] = "white"
        self.orin_port_label.grid(
            row = 4, 
            column=0, 
            sticky = "e", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_port_input = tk.Entry(self.orin_frame)
        self.orin_port_input["textvariable"] = self.orin_port
        self.orin_port_input.grid(
            row = 4, 
            column=1, 
            columnspan=3,
            sticky = "nsew", 
            padx = 5, 
            pady = 5, 
        )
        
        self.orin_connect_button = tk.Button(self.orin_frame)
        self.orin_connect_button["text"] = "Connect"
        self.orin_connect_button["bg"] = "#27f963"
        self.orin_connect_button["command"] = self.connect_orin
        self.orin_connect_button.grid(
            row = 5, 
            column=0, 
            columnspan=2,
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.orin_disconnect_button = tk.Button(self.orin_frame)
        self.orin_disconnect_button["text"] = "Disconnect"
        self.orin_disconnect_button["bg"] = "#f93527"
        self.orin_disconnect_button["command"] = self.disconnect_orin
        self.orin_disconnect_button.grid(
            row = 5, 
            column=2, 
            columnspan=2,
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )

        #? MODE SELECTION WIDGETS (Variable Settings)
        #go through the keys
        gcs_config_keys = sub_config["CONTROL_MODE"].keys()
        for key in gcs_config_keys:
            #dynamically create the robot settings
            self.variable_settings[key] = tk.Checkbutton(
                self.mode_selection_frame, 
                text=key.replace("_", " "), 
                onvalue=True, 
                offvalue=False,
                command=self.toggle_config
            )
            #since its dynamic, we have to store everything in a dictionary
            self.variable_settings[key+"_variable"] = tk.BooleanVar(value=sub_config["CONTROL_MODE"][key]) #here we just set the key_variable to what the checkbox is suposed to be (true/false)
            self.variable_settings[key]["variable"] = self.variable_settings[key+"_variable"]
            self.variable_settings[key].grid(
                sticky = "nsw"
            )
            #? don't forget to match these with the background and figure out why the checkmark is bugging out
            self.variable_settings[key]["bg"] = "black"
            self.variable_settings[key]["activebackground"] = "skyblue"
            self.variable_settings[key]["activeforeground"] = "white"
            self.variable_settings[key]["selectcolor"] = "gray"
            
            #change color depending on whether the setting is activated or not
            if self.variable_settings[key+"_variable"].get():
                self.variable_settings[key]["fg"] = "#50fa7b"
            else:
                self.variable_settings[key]["fg"] = "white"
        
        #? SUB CONTROL BUTTONS
        self.init_sub_button = tk.Button(
            self.button_frame,
            command=self.initialize_submarine,
            fg="black",
            bg="gold",
            padx = 2, 
            pady = 2
        )
        self.init_sub_button["text"] = "Initialize Sub"
        self.init_sub_button.grid()
        
        self.start_sub_button = tk.Button(
            self.button_frame,
            command=self.start_sub_program,
            fg="black",
            bg="#50fa7b",
            padx = 2, 
            pady = 2
        )
        self.start_sub_button["text"] = "Start Sub"
        self.start_sub_button.grid()
        
        self.stop_sub_button = tk.Button(
            self.button_frame,
            command=self.stop_sub_program,
            fg="black",
            bg="#f93527",
            padx = 2, 
            pady = 2
        )
        self.stop_sub_button["text"] = "Stop Sub"
        self.stop_sub_button.grid()

        #?INDICATOR WIDGETS
        self.voltage_label = tk.Label(self.indicator_frame)
        self.voltage_label["text"] = "Voltage"
        self.voltage_label["bg"] = "#50fa7b"
        self.voltage_label.grid(
            row = 0, 
            column = 0, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.voltage_value = tk.Label(self.indicator_frame)
        self.voltage_value["text"] = 0
        self.voltage_value["font"] = "Helvetica 12 bold"
        self.voltage_value["bg"] = "black"
        self.voltage_value["fg"] = "white"
        self.voltage_value.grid(
            row = 0, 
            column = 1, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.humidity_label = tk.Label(self.indicator_frame)
        self.humidity_label["text"] = "Humidity"
        self.humidity_label["bg"] = "#50fa7b"
        self.humidity_label.grid(
            row = 1, 
            column = 0, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.humidity_value = tk.Label(self.indicator_frame)
        self.humidity_value["text"] = 0
        self.humidity_value["font"] = "Helvetica 12 bold"
        self.humidity_value["bg"] = "black"
        self.humidity_value["fg"] = "white"
        self.humidity_value.grid(
            row = 1, 
            column = 1, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.tube_temp_label = tk.Label(self.indicator_frame)
        self.tube_temp_label["text"] = "Tube Temp"
        self.tube_temp_label["bg"] = "#50fa7b"
        self.tube_temp_label.grid(
            row = 2, 
            column = 0, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.tube_temp_value = tk.Label(self.indicator_frame)
        self.tube_temp_value["text"] = 0
        self.tube_temp_value["font"] = "Helvetica 12 bold"
        self.tube_temp_value["bg"] = "black"
        self.tube_temp_value["fg"] = "white"
        self.tube_temp_value.grid(
            row = 2, 
            column = 1, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.orin_temp_label = tk.Label(self.indicator_frame)
        self.orin_temp_label["text"] = "Orin Temp"
        self.orin_temp_label["bg"] = "#50fa7b"
        #self.orin_temp_label["fg"] = "#3C3E4A"
        self.orin_temp_label.grid(
            row = 3, 
            column = 0, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
        
        self.orin_temp_value = tk.Label(self.indicator_frame)
        self.orin_temp_value["text"] = 0
        self.orin_temp_value["font"] = "Helvetica 12 bold"
        self.orin_temp_value["bg"] = "black"
        self.orin_temp_value["fg"] = "white"
        self.orin_temp_value.grid(
            row = 3, 
            column = 1, 
            sticky = "nsew", 
            padx = 5, 
            pady = 5
        )
    
        #? CONSOLE WIDGETS
        # if theres time, maybe turn this into an ssh terminal as well?
        # https://stackoverflow.com/questions/63597533/how-to-add-a-console-to-a-tkinter-window
        self.console_display = tk.Listbox(self.console_frame)
        self.console_display["selectmode"] = tk.SINGLE
        self.console_display["activestyle"] = "none"
        self.console_display["selectbackground"] = "#3C3E4A"
        self.console_display["bg"] = "black"
        self.console_display["fg"] = "#f93527"
        self.console_display["font"] = "Helvetica 10 bold"
        self.console_display["bd"] = 0
        self.console_display.grid(
            row=0, 
            column=0,
            sticky = "nsew"
        )
        
        
    # ================= SUB PART CLASSES =================

    class Component:
        def __init__(self, name: str, label_object, recording:list = {}):
            self.label_object = label_object 
            self.value_objects = {}
            self.name = tk.StringVar(value = name)
            self.recording = recording
            self.display_string = ""
            
        def update_values(self):
            for k, v in self.recording.items():
                return
            
            
    def combobox_update(self, event):
        current_subsystem = self.data_combobox.get()
        
        #hide any currently shown subsystem components
        for i, subsystem in enumerate(self.components):
            #make sure they didn't just select the same subsystem, that would cause for useless computation if we hide and show that same subsystem
            if subsystem != current_subsystem:
                #hide the labels
                for component in self.components[subsystem]:
                    component.label_object.grid_remove()
                    
                    #hide the values and those values' labels
                    for stat in component.value_objects:
                        component.value_objects[stat][0].grid_remove()
                        component.value_objects[stat][1].grid_remove()
        
        #show the specified subsystem components
        for component in self.components[current_subsystem]:
            component.label_object.grid()
            
            for stat in component.value_objects:
                component.value_objects[stat][0].grid()
                component.value_objects[stat][1].grid()
            
            
    # ================= FUNCTIONS =================
    
    def toggle_config(self):
        #record the keys for the robot settings
        gcs_config_keys = sub_config["CONTROL_MODE"].keys()
        for key in gcs_config_keys:
            #make sure that the variables are different before trying to change them
            if sub_config["CONTROL_MODE"][key] != self.variable_settings[key+"_variable"].get():
                sub_config["CONTROL_MODE"][key] = self.variable_settings[key+"_variable"].get() #change it
                g = open(config_file, 'w')
                json.dump(sub_config, g, indent=4, sort_keys=False) #write the changed values to the sub config
                g.close()
                
                #change color depending on whether the setting is activated or not
                if self.variable_settings[key+"_variable"].get():
                    self.variable_settings[key]["fg"] = "#50fa7b"
                else:
                    self.variable_settings[key]["fg"] = "white"
    
    
    def connect_orin(self): #! something feels wrong about the connection setting, i should probably test this :)
        # if its already connected and it isn't trying to connect to the exact same host and port
        if self.orin_connected and self.orin_host.get() != self.connected_host and self.orin_port.get() != self.connected_port:
            self.disconnect_orin()
            
            with fabric.Connection(host=self.orin_host.get(), user=self.orin_user.get(), port=self.orin_port.get()) as ssh_connection:
                return
        else:
            with fabric.Connection(host=self.orin_host.get(), user=self.orin_user.get(), port=self.orin_port.get()) as ssh_connection:
                #ssh_connection.run('')
                return
            
            self.orin_connected = True
                
                
    def disconnect_orin(self):
        ssh_connection.close()
        self.orin_connected = False
        
    def initialize_submarine(self):
        self.statemachine = SM.Submarine()

    def start_sub_program(self):
        try:
            self.statemachine.send("start_submarine")
        except:
            self.console_display.insert("end", " ["+str(datetime.now())+"] Can't Start Submarine, Submarine is not Initialized.")

    def stop_sub_program(self):
        try:
            self.statemachine.send("power_off")
        except AttributeError:
            self.console_display.insert("end", " ["+str(datetime.now())+"] Can't Stop Submarine, Submarine is not Initialized.")
        
    
    def stream_video(self):
        time_a = time.time()
        #read the data and seperate it into its index, and frame (we don't need the index so its just an _)
        _, frame = web_camera_input.read()
        if type(frame) != np.ndarray:
            self.console_display.insert("end", " ["+str(datetime.now())+"] No Camera Found, Please Restart To Try Again.")
            return
            
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #turn it into an image :O
        img = Image.fromarray(cv2image)
        #make the image compatible with TK and allow it to achieve live feed
        imgtk = ImageTk.PhotoImage(image=img)
        #Display the image
        self.video_display.imgtk = imgtk
        self.video_display.configure(image=imgtk)
        
        #record how long it took to load the frame
        self.recorded_times.append(time.time()-time_a)
        
        #display fps updates every 30 seconds to the console
        if time.time() - self.time_last > 30:
            self.time_last = time.time()
            self.console_display.insert("end", " ["+str(datetime.now())+"] Camera FPS: " + str(get_fps(self.recorded_times)))
            self.recorded_times = []
        
        #after displaying the image, run the function again, to achieve a live video effect
        self.video_display.after(1, self.stream_video)
        
        
    def close_application(self):
        #incase the video_thread is not defined (testing or future changes)
        try:
            #make sure the thread is running before we try and close it
            if VIDEO_THREAD.is_alive():
                VIDEO_THREAD.join() # close the started thread
        except:
            pass
        
        #if its ssh connected, the disconnect that ssh
        if self.orin_connected:
            self.disconnect_orin()
            
        #!DO NOT TURN ANYTHING OFF WHEN CLOSING THE WINDOW EXCEPT SSH
        #? This is because during comp we will connect the program, start the sub on autonomous mode, and then disconnect
            
        WINDOW.destroy() # destroy the window, since we are overriding the origional functionality
        
async def get_video_data():
    try:
        #read the data and seperate it into its index, and frame (we don't need the index so its just an _)
        _, frame = web_camera_input.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #turn it into an image :O
        img = Image.fromarray(cv2image)
        #make the image compatible with TK and allow it to achieve live feed
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk
    except Exception as e:
        camera_restart_required = False

# ================= RUN =================

if __name__ == "__main__":
    WINDOW = tk.Tk()
    GCS = GCSApp(WINDOW)
    WINDOW.protocol("WM_DELETE_WINDOW", GCS.close_application) #custom close, so we can make sure everything is power off and logged out of correctly
    VIDEO_THREAD = threading.Thread(target=GCS.stream_video)
    VIDEO_THREAD.start() #activate the video streaming
    WINDOW.mainloop()