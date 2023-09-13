
# ================= CAN DO SOLO =================

#TODO: Make the component values (pwm, voltage, amp) actually update when changed
#TODO: Add SSH Connectability
#TODO: Add basic depth, humidity, temp, ect statistics
#TODO: Add program icon
#TODO: Make program look nicer


# ================= OTHER MODULES REQUIRED =================

#TODO: Properly handle camera (currently taking live feed when it will really just be getting a numpy array)
#TODO: Add / Handle Depth Camera
#TODO: Add / Handle Sonar
#TODO: Add / Handle Controller
#TODO: Add / Handle Buttons
#TODO: Add working power buttons (currently just shells)
#TODO: Add working program start / stop buttons  (currently just shells)
#TODO: Get variable settings to actually do something (currently i have no idea what they are going to look like)


# ================= IMPORTS =================

# imported as our main GUI library
import tkinter as tk
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

BATTERY_COUNT = config["ROBOT"]["BATTERY_COUNT"] or 4
MOTOR_COUNT = config["ROBOT"]["MOTOR_COUNT"] or 8
SERVO_COUNT = config["ROBOT"]["SERVO_COUNT"] or 2
ICON_PATH = config["GCS"]["ICON_PATH"] or ""

f.close()

# ============ NON APP SPECIFIC VARIABLES ============

# VARIABLE SETTINGS
training_sim = False
training_real_world = False
manual_control = False
autonomous_control = False

#INPUTS
web_camera_input = cv2.VideoCapture(0) #temp pulls straight from camera since no official input exists yet
depth_camera_input = ...
button_input = ...
controller_input = ...
sonar_input = ...


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
        self.orin_ip: str = tk.StringVar() or 'rasberrypi.local'
        self.orin_port: int = tk.IntVar() or 22
        self.orin_user: str = tk.StringVar() or 'user'
        self.orin_pass: str = tk.StringVar() or 'pass'
        
        # ORIN CURRENTLY CONNECTED TO
        self.connected_ip = 0
        self.connected_port = 0

        # TOGGLES
        self.orin_connected: bool = False
        
        # ================= WINDOW SETTINGS =================
        
        WINDOW.title()
        WINDOW.title("Ground Control Station")
        #WINDOW.iconphoto(True, tk.PhotoImage(file=ICON_PATH))
        WINDOW.columnconfigure(1, weight=1, minsize=250)
        WINDOW.rowconfigure(0, weight=1, minsize=100)
        WINDOW.rowconfigure(1, weight=1, minsize=100)
        WINDOW.rowconfigure(2, weight=1, minsize=100)
        
        #WINDOW CONSTANTS
        self.PPI: int = WINDOW.winfo_pixels("1i")
        
        # ================= FRAME CREATION =================
        
        self.orin_frame = tk.Frame(WINDOW)
        self.orin_frame["bg"] = "red"
        self.orin_frame.grid(row = 0, column = 2, rowspan = 2, sticky = "nsew", padx=2, pady=2)
        
        self.video_frame = tk.Frame(WINDOW)
        self.video_frame["bg"] = "limegreen"
        self.video_frame.grid(row = 0, column = 1, rowspan=2, sticky = "nsew", padx=2, pady=2)
        
        self.radar_frame = tk.Frame(WINDOW)
        self.radar_frame["bg"] = "yellow"
        self.radar_frame.grid(row = 0, column = 0, sticky="nsew", padx=2, pady=2)
        
        self.data_display_frame = tk.Frame(WINDOW)
        self.data_display_frame["bg"] = "dodgerblue"
        self.data_display_frame.grid(row = 1, column = 0, rowspan = 2, sticky = "nsew", padx=2, pady=2)
        
        self.button_frame = tk.Frame(WINDOW)
        self.button_frame["bg"] = "orange"
        self.button_frame.grid(row = 2, column = 1, columnspan=2, sticky="nsew", padx=2, pady=2)
        
        # ================= WEIDGET CREATION =================
        
        # ORIN FRAME WIDGETS
        self.orin_label = tk.Label(self.orin_frame)
        self.orin_label["text"] = "ORIN CONNECTION"
        
        self.orin_user_label = tk.Label(self.orin_frame)
        self.orin_user_label["text"] = "User:"
        
        self.orin_user_input = tk.Entry(self.orin_frame)
        self.orin_user_input["textvariable"] = self.orin_user
        
        self.orin_pass_label = tk.Label(self.orin_frame)
        self.orin_pass_label["text"] = "Pass:"
        
        self.orin_pass_input = tk.Entry(self.orin_frame)
        self.orin_pass_input["width"] = 30
        self.orin_pass_input["show"] = "*"
        self.orin_pass_input["textvariable"] = self.orin_pass
        
        self.orin_ip_label = tk.Label(self.orin_frame)
        self.orin_ip_label["text"] = "IP:"
        
        self.orin_ip_input = tk.Entry(self.orin_frame)
        self.orin_ip_input["width"] = 30
        self.orin_ip_input["textvariable"] = self.orin_ip
        
        self.orin_port_label = tk.Label(self.orin_frame)
        self.orin_port_label["text"] = "Port:"
        
        self.orin_port_input = tk.Entry(self.orin_frame)
        self.orin_port_input["width"] = 30
        self.orin_port_input["textvariable"] = self.orin_port
        
        self.connect_button = tk.Button(self.orin_frame)
        self.connect_button["text"] = "Connect"
        self.connect_button["command"] = self.connect_orin(True)

        self.orin_label.grid(row = 0, column=0, sticky = "nsew", rowspan = 1, columnspan = 2, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_user_label.grid(row = 1, column=0, sticky = "e", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_user_input.grid(row = 1, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_pass_label.grid(row = 2, column=0, sticky = "e", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_pass_input.grid(row = 2, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_ip_label.grid(row = 3, column=0, sticky = "e", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_ip_input.grid(row = 3, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_port_label.grid(row = 4, column=0, sticky = "e", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.orin_port_input.grid(row = 4, column=1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.connect_button.grid(row = 5, column=0, sticky = "nsew", rowspan = 1, columnspan = 2, padx = 5, pady = 5, ipadx = 3, ipady = 3)

        # VIDEO FRAME WIDGETS
        self.video_display = tk.Label(self.video_frame)
        self.video_display.grid(sticky = "nsew", rowspan = 1, columnspan = 2)

        # RADAR FRAME WIDGETS
        self.radar_display = tk.Label(self.radar_frame)
        self.radar_display.grid(sticky = "nsew", rowspan = 1, columnspan = 1)

        # DATA DISPLAY
        self.batteries = []
        self.motors = []
        self.servos = []

        for i in range(BATTERY_COUNT):
            self.batteries.append(self.Battery(label_object=tk.Label(self.data_display_frame, text="Battery "+str(i)+":"), value_object=tk.Label(self.data_display_frame, text="0")))
            self.batteries[i].label_object.grid(row = i-(i%2), column=1+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            self.batteries[i].value_object.grid(row = i-(i%2), column=2+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            #self.batteries[i].update_value()

        for i in range(BATTERY_COUNT, BATTERY_COUNT+MOTOR_COUNT):
            count = i-BATTERY_COUNT
            self.motors.append(self.Motor(label_object=tk.Label(self.data_display_frame, text="Motor "+str(count)+":"), value_object=tk.Label(self.data_display_frame, text="0")))
            self.motors[count].label_object.grid(row = i-(i%2), column=1+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            self.motors[count].value_object.grid(row = i-(i%2), column=2+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            #self.motors[i].update_value()
            
        print(3*"=")
        for i in range(BATTERY_COUNT+MOTOR_COUNT, BATTERY_COUNT+MOTOR_COUNT+SERVO_COUNT):
            count = i-(BATTERY_COUNT+MOTOR_COUNT)
            self.servos.append(self.Servo(label_object=tk.Label(self.data_display_frame, text="Servo "+str(count)+":"), value_object=tk.Label(self.data_display_frame, text="0")))
            self.servos[count].label_object.grid(row = i-(i%2), column=1+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            self.servos[count].value_object.grid(row = i-(i%2), column=2+(i%2*2), sticky = "nsew", rowspan = 1, columnspan = 1, padx = 5, pady = 5, ipadx = 3, ipady = 3)
            #self.servos[i].update_value()
            
        # BUTTON FRAME
        self.power_sub_on_button = tk.Button(self.button_frame)
        self.power_sub_on_button["text"] = "Power Sub On"
        self.power_sub_on_button["command"] = power_sub(True)
        
        self.power_sub_off_button = tk.Button(self.button_frame)
        self.power_sub_off_button["text"] = "Power Sub On"
        self.power_sub_off_button["command"] = power_sub(False)
        
        self.start_program_button = tk.Button(self.button_frame)
        self.start_program_button["text"] = "Power Sub On"
        self.start_program_button["command"] = start_sub_program
        
        self.stop_program_button = tk.Button(self.button_frame)
        self.stop_program_button["text"] = "Power Sub On"
        self.stop_program_button["command"] = stop_sub_program
        
        self.power_motors_on_button = tk.Button(self.button_frame)
        self.power_motors_on_button["text"] = "Power Sub On"
        self.power_motors_on_button["command"] = power_motors(True)
        
        self.power_motors_off_button = tk.Button(self.button_frame)
        self.power_motors_off_button["text"] = "Power Sub On"
        self.power_motors_off_button["command"] = power_motors(False)
        
        self.power_servos_on_button = tk.Button(self.button_frame)
        self.power_servos_on_button["text"] = "Power Sub On"
        self.power_servos_on_button["command"] = power_servos(True)
        
        self.power_servos_off_button = tk.Button(self.button_frame)
        self.power_servos_off_button["text"] = "Power Sub On"
        self.power_servos_off_button["command"] = power_servos(False)

        self.power_sub_on_button.grid(row = 0, column = 0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.power_sub_off_button.grid(row = 1, column = 0, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.start_program_button.grid(row = 0, column = 1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.stop_program_button.grid(row = 1, column = 1, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.power_motors_on_button.grid(row = 0, column = 2, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.power_motors_off_button.grid(row = 1, column = 2, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.power_servos_on_button.grid(row = 0, column = 3, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
        self.power_servos_off_button.grid(row = 1, column = 3, sticky = "nsew", rowspan = 1, columnspan = 1, padx = 2, pady = 2)
    
    # ================= SUB PART CLASSES =================

    class Battery:
        def __init__(self, label_object, value_object):
            self.label_object = label_object 
            self.value_object = value_object
            self.voltage = tk.IntVar()
            self.amps = tk.IntVar()
        
        def update_value(self):
            self.value_object.text = str(self.voltage)+" / "+str(self.amps)
        

    class Motor:
        def __init__(self, label_object, value_object):
            self.label_object = label_object # object that displays the name of the motor, ex "Motor 1"
            self.value_object = value_object # object that displays the pwm of the motor
            self.pwm = tk.IntVar()
        
        def update_value(self):
            self.pwm.set(3)
            self.value_object.text = "3"

    class Servo:
        def __init__(self, label_object, value_object):
            self.label_object = label_object 
            self.value_object = value_object
            self.pwm = tk.IntVar()
        
        def update_value(self):
            self.value_object.text = self.pwm
    
    # ================= FUNCTIONS =================
    
    def connect_orin(self, connection_bool: bool, recursive_bool: bool = False):
        if connection_bool:
            # if its already connected and it isn't trying to connect to the exact same ip and port
            if self.orin_connected and self.orin_ip != self.connected_ip and self.orin_port != self.connected_port:
                orin_connected = False
                self.connect_orin(False, True)
            else:
                self.orin_connected = True
        elif not connection_bool:
            if recursive_bool:
                self.orin_connected = True
            else:
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
        self.connect_orin(False)
        WINDOW.destroy() # destroy the window, since we are overriding the origional functionality

# ================= RUN =================

if __name__ == "__main__":
    WINDOW = tk.Tk()
    GCS = GCSApp(WINDOW)
    WINDOW.protocol("WM_DELETE_WINDOW", GCS.close_application) #custom close, so we can make sure everything is power off and logged out of correctly
    VIDEO_THREAD = threading.Thread(target=GCS.stream_video)
    VIDEO_THREAD.start() #activate the video streaming
    WINDOW.mainloop()
