
from zaber_motion.ascii import Connection
from zaber_motion.ascii import Axis


"""
MANUAL CONTROL ASR120B100B

For manual control, the driver for the ASR120B100B has 2 dials controlling axis 1 and axis 2 respectively. These control the axes without sending commands through to the serial port. Pressing and holding either dial for 5 seconds while powering up the controller will perform a factory reset. All custom settings and data will be cleared and factory defaults restored when the dial released. Holding either dial in for 1 second will switch the control mode between displacement and velocity (stepwise motion or constant travel). In velocity mode, each incremental turn of the dial adjusts the speed of travel according to the velocityprofile setting (linear, quartic, or cubic). Pressing a dial in will stop travel along the corresponding axis.
"""

class ASR():
    
    def __init__(self, port):
        """
    
        Parameters
        ----------
        port : int
            The COM port through which the ASR device is to be connected

        Returns
        -------
        None.

        """
        self.port = f'COM{port}'
        self.device = None
        self.axis1 = None
        self.axis2 = None
        
    def __enter__(self):
        try:
            """
            Establish connection to the ASR device
            """
            self.device = Connection.open_serial_port(self.port).detect_devices(True)[0]
            print("ASR Connected")
            """
            Define the device axes
            """
            self.axis1 = Axis(self.zaberdevice, 1)
            self.axis2 = Axis(self.zaberdevice, 2)
            """ 
            Axis settings
            """
            self.axis1.settings.set("maxspeed")/4
            self.axis2.settings.set("maxspeed")/4
            print("Axes established:")
            """
            Perform homing if necessary (request user approval)
            """
            while True:
                if self.axis1.is_homed() or self.axis2.is_homed() == 0:
                    """
                    Limit the travel speed during homing
                    """
                    for axis in [self.axis1, self.axis2]:
                        maxspeed = axis.settings.get("maxspeed")
                        axis.settings.set("limit.approach.maxspeed",maxspeed)
                    """
                    Carry out homing
                    """
                    prompt = input("Confirm the microscope is safe to home? (y/n)")
                    if prompt == "y":
                        for axis in [self.axis1, self.axis2]:
                            if not axis.is_homed():
                                self.home(axis)
                    elif prompt == "n":
                        self.__exit__(None,None,None)
                        break
                    else:
                        ValueError("Unrecognised input. Specify y or n") 
                        raise
        except Exception as e:
            ConnectionError(f"Couldn't connect to ASR: {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            try:
                self.connection.__exit__(None, None, None)
                print("ASR Disconnected")
            except Exception as e:
                ConnectionError(f"Couldn't disconnect from ASR device: {e}")
                raise
        else:
            pass
        
    def home(self,axis):
        """
        Home each axis on the ASR device in turn. Ensure any stage inserts are removed to prevent damage to in-situ components.

        Returns
        -------
        None.

        """
        try:
            axis.home(wait_until_idle=True)
            print(f"{axis} Homed")
        except Exception as e:
            print(f"Couldn't home {axis}': {e}")
            
    def getPosition(self,axis,units):
        """
        Query the current position of the specified axis on the ASR device
    
        Parameters
        ----------
        units : string
            The unit of measurement. Supported values are mm, um, nm, or native.
    
        Returns
        -------
        float
            The current position of the specified axis on the ASR device
        
        Raises
        ------
        ValueError
            Unable to retrieve location information
        """
        unit = ASR.utils.lengthConversion(units)
        try:
            pos = [f"{axis}.get_position(zaber_motion.Units.{unit})"]
            return pos
        except Exception as e:
            print(f"Couldn't retrieve location information: {e}")
            raise 

    def moveAbsolute(self,axis,target,units):
        """
        Translate the stage to a new absolute location        

        Parameters
        ----------
        axis: ASR.device.axis
            The chosen axis on the connected device
        target: float
            Desired stage position along a chosen axis
        units: string
            Distance units. Available units are mm, um, nm, or native encoder units.

        Returns
        -------
        None.

        """
        unit = self.utils.lengthConversion(units)
        try:
            axis.move_absolute(target,unit,wait_until_idle=True)
        except Exception as e:
            print(e)
                
        
    def moveRelative(self,axis,step,units):
        """
        Translate the stage by a some distance

        Parameters
        ----------
        axis: string
            The device axis to be translated
        step : float
            Distance to move the stage along an axis
        units : string
            Distance units. Available units are mm, um, nm, or native encoder units.

        Returns
        -------
        None.

        """
        unit = self.utils.lengthConversion(units)
        try:
            axis.move_relative(step,unit,wait_until_idle=True)
        except Exception as e:
            print(e)
        
    class utils:
        
        speed_map = {
            "cm/s": "VELOCITY_CENTIMETRES_PER_SECOND",
            "cm": "VELOCITY_CENTIMETRES_PER_SECOND",
            "mm/s": "VELOCITY_MILLIMETRES_PER_SECOND",
            "mm": "VELOCITY_MILLIMETRES_PER_SECOND",
            "um/s": "VELOCITY_MICROMETRES_PER_SECOND",
            "um": "VELOCITY_MICROMETRES_PER_SECOND",
            "nm/s": "VELOCITY_NANOMETRES_PER_SECOND",
            "nm": "VELOCITY_NANOMETRES_PER_SECOND"
            }
        
        length_map = {
            "mm": "LENGTH_MILLIMETRES",
            "millimeter": "LENGTH_MILLIMETRES",
            "millimeters": "LENGTH_MILLIMETRES",
            "um": "LENGTH_MICROMETRES",
            "micrometer": "LENGTH_MICROMETRES",
            "micrometers": "LENGTH_MICROMETRES",
            "microns": "LENGTH_MICROMETRES",
            "nm": "LENGTH_NANOMETRES",
            "nanometer": "LENGTH_NANOMETRES",
            "nanometers": "LENGTH_NANOMETRES",
            "native": "NATIVE",
            "default": "NATIVE"
            }
        
        @staticmethod
        def velocityConversion(units):
            if units:
                unit = units.strip().lower()
                if unit in ASR.utils.speed_map:
                    return unit
                else:
                    raise ValueError("Unrecognised units. Try cm/s, mm/s, um/s, or nm/s")
                    
        @staticmethod    
        def lengthConversion(units):
            if units:
                unit = units.strip().lower()
                if unit in ASR.utils.length_map:
                    return unit
                else:
                    raise ValueError("Unrecognised units. Try mm, um, nm, or native")
                
    class settings:
        
        settings_map = {"Stage acceleration": "accel",
                       "Device ID": "device.id",
                       "Driver temperature": "driver.temperature",
                       "Encoder measured position": "encoder.pos",
                       "Position error": "encoder.pos.error",
                       "Axis position": "pos",
                       "Manual control direction": "knob.dir",
                       "Translation step per control increment": "knob.distance",
                       "Manual control enabled": "knob.enable",
                       "Travel speed under manual control": "knob.maxspeed",
                       "Manual control mode": "knob.mode",
                       "Speed profile under manual control": "knob.speedprofile"}
        
        def __init__(self,device):
            self.device = device
            
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type:
                print(f"An error occurred: {exc_value}")
        
        def set(self, setting, value):
            """
            Set a specific ASR setting for the given device.

            Parameters
            ----------
            setting : string
                The device setting to be altered
            value : string
                The value of the device setting to be altered

            Returns
            -------
            None.

            """
            internal_key = self.settings_map.get(setting)
            if not internal_key:
                print(f"'{setting}' is not a recognized setting.")
                return
        
            try:
                self.obj.settings.set_string(internal_key, value)
                value = self.device.settings.get_string(internal_key)
                print(f"{setting}: {value}")
            except Exception as e:
                print(f"Could not update '{setting}': {e}")
                            
        
        def get(self, setting):
            """
            Retrieve a specific ASR setting for the given device.
        
            Parameters
            ----------
            setting : str
                The human-readable name of the setting to retrieve.
        
            Returns
            -------
            dict
                A dictionary containing the requested setting and its value, 
                or an empty dictionary if the setting is not available.
            """
        
            # Map the requested setting to the internal key
            internal_key = self.settings_map.get(setting)
            if not internal_key:
                print(f"'{setting}' is not a recognized setting for this device.")
                return
            
            # Attempt to retrieve the setting value
            try:
                value = self.obj.settings.get_string(internal_key)
                if value is not None:
                    print(f"{setting}: {value}")
                else:
                    print(f"'{setting}' is available but has no value.")
            except Exception as e:
                print(f"Could not retrieve '{setting}': {e}")

        
    
if __name__ == "__main__":
    
    # Instantiation of the ASR object
    stage = ASR(3)
    
    # Interact with the device settings
    stage.settings(stage.device).get("maxspeed")
    stage.settings(stage.device).set("maxspeed","10")

    # Recover the position of each axis on the connected device
    pos = [stage.getPosition(axis, "mm") for axis in [stage.axis1, stage.axis2]]
    
    # Move the device axis in various ways
    stage.moveAbsolute(stage.axis1, 0, "mm")
    stage.moveAbsolute(stage.axis2, 0, "mm")
    stage.moveRelative(stage.axis1, 0, "mm")
    stage.moveRelative(stage.axis2, 0, "mm")
    
    # Reference the device axes
    stage.home(stage.axis1)
    stage.home(stage.axis2)
    
    
    
        