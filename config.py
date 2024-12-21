"""
config.py
This file contains constants and configuration settings for the microscope control system.
"""

# DAQ DEVICE LIST [CHANNEL, FAMILY, NAME]
""" List of devices connected to the DAQ [channel, family, name] """
DEVA0 = devices.AOdevice(0, "", "")
DEVA1 = devices.AOdevice(1, "", "")
DEVA2 = devices.AOdevice(2, "", "")
DEVA3 = devices.AOdevice(3, "", "")
DEVB0 = devices.AIDevice(0, "Photodiode", "PhotodiodeT")
DEVB1 = devices.AIDevice(1, "Photodiode", "PhotodiodeR")
DEVB2 = devices.AIDevice(2, "Photodiode", "Lamp")
DEVB3 = devices.AIDevice(3, "Photodiode", "PhotodiodeOther")
DEVB4 = devices.AIDevice(4, "Accessory", "SignalGenerator")
DEVB5 = devices.AIDevice(5, "", "")
DEVB6 = devices.AIDevice(6, "", "")
DEVB7 = devices.AIDevice(7, "", "")
DEVC0 = devices.PODevice(0, "Source", "Vortran")
DEVC1 = devices.PODevice(1, "Accessory", "Tektronix")
DEVC2 = devices.PODevice(2, "Source", "SLS205")
DEVC3 = devices.PODevice(3, "Spectrometer", "CCS200")
DEVC4 = devices.PODevice(4, "", "")
DEVC5 = devices.PODevice(5, "", "")
DEVC6 = devices.PODevice(6, "", "")
DEVC7 = devices.PODevice(7, "", "")

DEVICELIST= [DEVA0, DEVA1, DEVA2, DEVA3,
             DEVB0, DEVB1, DEVB2, DEVB3, DEVB4, DEVB5, DEVB6, DEVB7,
             DEVC0, DEVC1, DEVC2, DEVC3, DEVC4, DEVC5, DEVC6, DEVC7]

ZABERCOM = 8
ZABER_POSLIM = {"Ax1_min": 0,
                "Ax1_max": 0,
                "Ax2_min": 0,
                "Ax2_max": 0}
ZABERVEL = 

LASERCOM = 3

PIMOD = "E-873"
PISER = "121007658"

SPECTRID = b"USB0::0x1313::0x8089::M00928154::RAW"

SIGNALID = 'USB0::0x0957::0x0407::MY43004556::INSTR'

# Camera Configuration
CAMERA_DEVICE_ID = "CAM12345"  # Example device ID for the camera
CAMERA_DEFAULT_RESOLUTION = (1920, 1080)  # Width x Height in pixels
CAMERA_FRAME_RATE = 30  # Frames per second

# Stage Configuration
STAGE_DEVICE_ID = "STAGE67890"
STAGE_DEFAULT_SPEED = 5  # Speed in mm/s
STAGE_BOUNDS = {  # Limits for movement in mm
    "x_min": 0,
    "x_max": 100,
    "y_min": 0,
    "y_max": 100,
    "z_min": 0,
    "z_max": 50,
}

# Light Source Configuration
LIGHT_SOURCE_DEVICE_ID = "LIGHT1234"
LIGHT_DEFAULT_INTENSITY = 75  # Intensity as a percentage
LIGHT_WAVELENGTHS = [450, 550, 650]  # Available wavelengths in nm

# Communication Settings
DEFAULT_PORT = "COM3"  # Default communication port
BAUD_RATE = 9600  # Serial communication speed
TIMEOUT = 1  # Communication timeout in seconds

# Logging Settings
LOG_FILE_PATH = "logs/microscope_control.log"
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
