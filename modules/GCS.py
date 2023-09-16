
# ================= TODO =================

#TODO: Add console
#TODO: Make buttons for the top right corder
#TODO: Keybind Spacebar to "power sub off"
#TODO: Create the "variable settings" section bottom right purple area
#TODO: Make program look nicer


# ======= OTHER MODULES / PEOPLE REQUIRED =======

#TODO: Add program icon (waiting on Juan)
#TODO: Properly handle camera (currently taking live feed when it will really just be getting a numpy array)
#TODO: Add / Handle Depth Camera
#TODO: Add / Handle Sonar
#TODO: Add / Handle Controller
#TODO: Add / Handle Buttons
#TODO: Move power function over to Sate Machine
#TODO: Add working program start / stop buttons  (currently just shells)
#TODO: Get the "variable settings" to actually do something (currently i have no idea what that is going to look like)


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


# ================= CONFIG =================
f = open(__file__.split("GCS")[0]+'configs\\config.json')
config = json.load(f)

COMPONENTS = config["ROBOT"]

ICON_PATH = config["GCS"]["ICON_PATH"]
training_sim = config["GCS"]["training_sim"]
training_real_world = config["GCS"]["training_real_world"]
manual_control = config["GCS"]["manual_control"]
autonomous_control = config["GCS"]["autonomous_control"]
auto_navigate_error = config["GCS"]["auto_navigate_error"]

f.close()

# ============ NON APP SPECIFIC VARIABLES ============

#INPUTS
web_camera_input = cv2.VideoCapture(0) #temp pulls straight from camera since no official input exists yet
depth_camera_input = ...
button_input = ...
controller_input = ...
sonar_input = ...

#SSH
ssh_connection = ...


#! ==================== TO BE REMOVED ====================
#! TO BE REMOVED AND PUT INTO THE STATE MACHINE

batteries_on: bool = False
motors_on: bool = False
servos_on: bool = False

def power_sub(power_bool: bool):
    if power_bool:
        batteries_on = True
    else:
        batteries_on = False

#motors start with no power, this will allow power to connect to them
def power_motors(power_bool: bool):
    if power_bool:
        motors_on = True
    else:
        motors_on = False     

def power_servos(power_bool: bool):
    if power_bool:
        servos_on = True
    else:
        servos_on = False
        
        
# ============ CRITICAL FUNCTIONS ============

#?Leaving this out of the app so it can be easily exported and used **IF** ever needed
def start_sub_program():
    #open main.py
    return

def stop_sub_program():
    #call the quit() function in main.py
    return
            

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
        
        # ================= WINDOW SETTINGS =================
        
        WINDOW.title()
        WINDOW.title("Ground Control Station")
        #WINDOW.iconphoto(True, tk.PhotoImage(file=ICON_PATH))
        
        #Setting sizes
        WINDOW.columnconfigure([0, 1], weight=1, minsize=100)
        WINDOW.columnconfigure(2, weight=2, minsize=200)
        WINDOW.columnconfigure(3, weight=1, minsize=100)
        
        # ================= FRAME CREATION =================
        
        self.video_frame = tk.Frame(WINDOW)
        self.video_frame["bg"] = "red"
        self.video_frame.grid(
            row = 0, 
            column = 1, 
            rowspan=3, 
            columnspan=2, 
            sticky = "nsew", 
            padx=2, 
            pady=2
        )
        
        self.data_display_frame = tk.Frame(WINDOW)
        self.data_display_frame["bg"] = "orange"
        self.data_display_frame.columnconfigure([0, 1], weight=1)
        self.data_display_frame.grid(
            row = 0, 
            column = 0, 
            rowspan = 4, 
            sticky = "nsew", 
            padx=2, 
            pady=2
        )
        
        self.sonar_frame = tk.Frame(WINDOW)
        self.sonar_frame["bg"] = "yellow"
        self.sonar_frame.grid(
            row = 0, 
            column = 3, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
        
        self.graph_frame = tk.Frame(WINDOW)
        self.graph_frame["bg"] = "limegreen"
        self.graph_frame.grid(
            row = 1, 
            column = 3, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
        
        self.orin_frame = tk.Frame(WINDOW)
        self.orin_frame["bg"] = "dodgerblue"
        self.orin_frame.columnconfigure([0, 1], weight=1)
        self.orin_frame.grid(
            row = 2, 
            column = 3, 
            sticky = "nsew", 
            padx=2, 
            pady=2
        )
        
        self.mode_selection_frame = tk.Frame(WINDOW)
        self.mode_selection_frame["bg"] = "purple"
        self.mode_selection_frame.grid(
            row = 3, 
            column = 3, 
            rowspan = 2, 
            sticky = "nsew", 
            padx=2, 
            pady=2
        )
        
        self.indicator_frame = tk.Frame(WINDOW)
        self.indicator_frame["bg"] = "black"
        self.indicator_frame.columnconfigure([0, 1], weight=1)
        self.indicator_frame.grid(
            row = 3, 
            column = 1, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
        
        self.console_frame = tk.Frame(WINDOW)
        self.console_frame["bg"] = "black"
        self.console_frame.grid(
            row = 3, 
            column = 2, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
        
        # ================= WEIDGET CREATION =================
        
        # ORIN FRAME WIDGETS
        self.orin_label = tk.Label(self.orin_frame)
        self.orin_label["text"] = "ORIN CONNECTION"
        self.orin_label.grid(row = 0, column=0, sticky = "nsew", rowspan = 1, columnspan = 2, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_user_label = tk.Label(self.orin_frame)
        self.orin_user_label["text"] = "User:"
        self.orin_user_label.grid(row = 1, column=0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_user_input = tk.Entry(self.orin_frame)
        self.orin_user_input["textvariable"] = self.orin_user
        self.orin_user_input.grid(row = 1, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_pass_label = tk.Label(self.orin_frame)
        self.orin_pass_label["text"] = "Pass:"
        self.orin_pass_label.grid(row = 2, column=0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_pass_input = tk.Entry(self.orin_frame)
        self.orin_pass_input["show"] = "*"
        self.orin_pass_input["textvariable"] = self.orin_pass
        self.orin_pass_input.grid(row = 2, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_host_label = tk.Label(self.orin_frame)
        self.orin_host_label["text"] = "Host:"
        self.orin_host_label.grid(row = 3, column=0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_host_input = tk.Entry(self.orin_frame)
        self.orin_host_input["textvariable"] = self.orin_host
        self.orin_host_input.grid(row = 3, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_port_label = tk.Label(self.orin_frame)
        self.orin_port_label["text"] = "Port:"
        self.orin_port_label.grid(row = 4, column=0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_port_input = tk.Entry(self.orin_frame)
        self.orin_port_input["textvariable"] = self.orin_port
        self.orin_port_input.grid(row = 4, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_connect_button = tk.Button(self.orin_frame)
        self.orin_connect_button["text"] = "Connect"
        self.orin_connect_button["bg"] = "limegreen"
        self.orin_connect_button["command"] = self.connect_orin
        self.orin_connect_button.grid(row = 5, column=0, sticky = "nsew", padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        self.orin_disconnect_button = tk.Button(self.orin_frame)
        self.orin_disconnect_button["text"] = "Disconnect"
        self.orin_disconnect_button["bg"] = "red"
        self.orin_disconnect_button["command"] = self.disconnect_orin
        self.orin_disconnect_button.grid(row = 5, column=1, sticky = "nsew", padx = 5, pady = 5, ipadx = 3, ipady = 3)
        
        # VIDEO FRAME WIDGETS
        self.video_display = tk.Label(self.video_frame)
        self.video_display.grid(sticky = "nsew", rowspan = 1, columnspan = 2)

        # RADAR FRAME WIDGETS
        self.radar_display = tk.Label(self.sonar_frame)
        self.radar_display.grid(sticky = "nsew", rowspan = 1, columnspan = 1)

        # DATA DISPLAY
        self.data_combobox = ttk.Combobox(self.data_display_frame)
        self.data_combobox['state'] = "readonly"
        self.data_combobox.grid(
            row = 0,
            column = 0,
            columnspan= 2,
            stick = "nsew",
            padx = 2,
            pady = 2
        )
        
        #?bind combobox changed event
        self.data_combobox.bind('<<ComboboxSelected>>', self.combobox_update)
        
        self.voltage_label = tk.Label(self.indicator_frame)
        self.voltage_label["text"] = "Voltage"
        self.voltage_label["bg"] = "limegreen"
        self.voltage_label.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.voltage_value = tk.Label(self.indicator_frame)
        self.voltage_value["text"] = 0
        self.voltage_value.grid(row = 0, column = 2, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.humidity_label = tk.Label(self.indicator_frame)
        self.humidity_label["text"] = "Humidity"
        self.humidity_label["bg"] = "limegreen"
        self.humidity_label.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.humidity_value = tk.Label(self.indicator_frame)
        self.humidity_value["text"] = 0
        self.humidity_value.grid(row = 1, column = 2, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.tube_temp_label = tk.Label(self.indicator_frame)
        self.tube_temp_label["text"] = "Tube Temp"
        self.tube_temp_label["bg"] = "limegreen"
        self.tube_temp_label.grid(row = 2, column = 0, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.tube_temp_value = tk.Label(self.indicator_frame)
        self.tube_temp_value["text"] = 0
        self.tube_temp_value.grid(row = 2, column = 2, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.orin_temp_label = tk.Label(self.indicator_frame)
        self.orin_temp_label["text"] = "Orin Temp"
        self.orin_temp_label["bg"] = "limegreen"
        self.orin_temp_label.grid(row = 3, column = 0, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        self.orin_temp_value = tk.Label(self.indicator_frame)
        self.orin_temp_value["text"] = 0
        self.orin_temp_value.grid(row = 3, column = 2, columnspan = 2, sticky = "nsew", padx = 5, pady = 5)
        
        
        self.components = {}

        for i, k in enumerate(COMPONENTS):
            #since the values of the combobox were not default set, tkinter sets the values paramater as a string instead of a tuple like it's supposed to be (wtf tkinter)
            #so we have to account for it being a string instead of just concating a tuple
            if type(self.data_combobox["values"]) == str:
                self.data_combobox["values"] = (k,)
            else:
                self.data_combobox["values"] += (k,)
            
            dictionary = COMPONENTS[k]
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
                        recording=dictionary["RECORDING"]
                    )
                )                
                
                #assign the just created component to a variable so we can edit it
                component = self.components[k][-1]
                
                component.label_object["text"] = dictionary["NAME"]+" "+str(n+1)+":"
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
                
                for stat in dictionary["RECORDING"]:
                    #create a label and value holder for each stat that is to be recorded for the component
                    component.value_objects[stat] = [tk.Label(self.data_display_frame), tk.Label(self.data_display_frame)]
                    label = component.value_objects[stat][0]
                    value = component.value_objects[stat][1]
                    
                    label["text"] = stat
                    label.grid(
                        row = rowcount, 
                        column=0, 
                        sticky = "e", 
                        padx = 5, 
                        pady = 5
                    )
                    label.grid_remove()
                    
                    value["text"] = 0
                    value.grid(
                        row = rowcount, 
                        column=1, 
                        sticky = "w", 
                        padx = 5, 
                        pady = 5
                    )
                    value.grid_remove()
                    
                    rowcount += 1
                    

        #? I plan on putting these top right tab like size, maybe 10 pixels tall, with an info hover
        # self.power_sub_on_button = tk.Button(self.indicator_frame)
        # self.power_sub_on_button["text"] = "Power Sub On"
        # self.power_sub_on_button["command"] = power_sub(True)
        
        # self.power_sub_off_button = tk.Button(self.indicator_frame)
        # self.power_sub_off_button["text"] = "Power Sub On"
        # self.power_sub_off_button["command"] = power_sub(False)
        #! ADD SPACEBAR AS A HOT KEY FOR TURNING THE SUB OFF
        
        # self.start_program_button = tk.Button(self.indicator_frame)
        # self.start_program_button["text"] = "Power Sub On"
        # self.start_program_button["command"] = start_sub_program
        
        # self.stop_program_button = tk.Button(self.indicator_frame)
        # self.stop_program_button["text"] = "Power Sub On"
        # self.stop_program_button["command"] = stop_sub_program
        
        # self.power_motors_on_button = tk.Button(self.indicator_frame)
        # self.power_motors_on_button["text"] = "Power Sub On"
        # self.power_motors_on_button["command"] = power_motors(True)
        
        # self.power_motors_off_button = tk.Button(self.indicator_frame)
        # self.power_motors_off_button["text"] = "Power Sub On"
        # self.power_motors_off_button["command"] = power_motors(False)
        
        # self.power_servos_on_button = tk.Button(self.indicator_frame)
        # self.power_servos_on_button["text"] = "Power Sub On"
        # self.power_servos_on_button["command"] = power_servos(True)
        
        # self.power_servos_off_button = tk.Button(self.indicator_frame)
        # self.power_servos_off_button["text"] = "Power Sub On"
        # self.power_servos_off_button["command"] = power_servos(False)

        # self.power_sub_on_button.grid(row = 0, column = 0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.power_sub_off_button.grid(row = 1, column = 0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.start_program_button.grid(row = 0, column = 1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.stop_program_button.grid(row = 1, column = 1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.power_motors_on_button.grid(row = 0, column = 2, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.power_motors_off_button.grid(row = 1, column = 2, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.power_servos_on_button.grid(row = 0, column = 3, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        # self.power_servos_off_button.grid(row = 1, column = 3, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)

    
    # ================= SUB PART CLASSES =================

    class Component:
        def __init__(self, name: str, label_object, recording:list = []):
            self.label_object = label_object 
            self.value_objects = {}
            self.name = tk.StringVar(value = name)
            self.recording = {}
            self.display_string = ""
            
            for i, v in enumerate(recording):
                # use a / to differentiate between different values
                if i > 1:
                    self.display_string += " / "
                
                self.recording[v] = 0
            
            #cut off excess /
            if len(self.display_string) > 3:
                if self.display_string[-2] == "/":
                    self.display_string = self.display_string[:-3]
                
            self.display = tk.StringVar(value = self.display_string)

        def update_values(self):
            self.display_string = ""
            for i, v in enumerate(self.recording):
                # use a / to differentiate between different values
                if i > 1:
                    self.display_string += " / "
                
                self.display_string += str(v)
            
            self.display.set(self.display_string)
            
    def combobox_update(self, event):
        current_subsystem = self.data_combobox.get()
        
        #hide any currently shown subsystem components
        for i, subsystem in enumerate(self.components):
            if subsystem != current_subsystem:
                for component in self.components[subsystem]:
                    component.label_object.grid_remove()
                    
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
    
    def connect_orin(self):
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
    
    def stream_video(self):
        #read the data and seperate it into its index, and frame (we don't need the index so its just an _)
        _, frame = web_camera_input.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #turn it into an image :O
        img = Image.fromarray(cv2image)
        #make the image compatible with TK and allow it to achieve live feed
        imgtk = ImageTk.PhotoImage(image=img)
        #Display the image
        self.video_display.imgtk = imgtk
        self.video_display.configure(image=imgtk)
        #after displaying the image, run the function again, to achieve a live video effect
        self.video_display.after(1, self.stream_video) 
        #still need to test if this will effect the workability of the program
        
    def close_application(self):
        VIDEO_THREAD.join() # close the started thread
        
        #if its ssh connected, the disconnect that ssh
        if self.orin_connected:
            self.disconnect_orin()
            
        #!DO NOT TURN ANYTHING OFF WHEN CLOSING THE WINDOW EXCEPT SSH
        #? This is because during comp we will connect the program, start the sub on autonomous mode, and then disconnect
            
        WINDOW.destroy() # destroy the window, since we are overriding the origional functionality

# ================= RUN =================

if __name__ == "__main__":
    WINDOW = tk.Tk()
    GCS = GCSApp(WINDOW)
    WINDOW.protocol("WM_DELETE_WINDOW", GCS.close_application) #custom close, so we can make sure everything is power off and logged out of correctly
    VIDEO_THREAD = threading.Thread(target=GCS.stream_video)
    VIDEO_THREAD.start() #activate the video streaming
    WINDOW.mainloop()
