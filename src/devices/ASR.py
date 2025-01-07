
import zaber_motion

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
        self.zaberdevice = None
        self.connection = None
        self.axes = []
        self.settings = self.Settings()
        
    def __enter__(self):
        try:
            """
            Establish connection to the ASR device
            """
            self.connection = Connection.open_serial_port(self.port)
            self.zaberdevice = self.connection.detect_devices(True)[0]
            print("ASR Connected")
            """
            Define the device axes and set speed to safe bounds
            """
            axisCount = self.zaberdevice.axis_count
            
            for ax in range(axisCount):
                name = f"axis{ax+1}"
                axis_instance = Axis(self.zaberdevice, ax+1)
                setattr(self, name, axis_instance)
                axis = getattr(self, name)
                
                vdefault = axis.settings.get_default("maxspeed")
                axis.settings.set("maxspeed",vdefault/10)
                self.axes.append(axis)

            print("Axes established:")
            """
            Perform homing if necessary (request user approval)
            """
            if self.zaberdevice.all_axes.is_homed() == 0:
                prompt = input("Confirm the microscope is safe to home? (y/n): ")
                if prompt == "y":
                    for axis in self.axes:
                        if not axis.is_homed():
                            self.home(axis)
                elif prompt == "n":
                    self.__exit__(None,None,None)
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
            The current position of the specified axis on the ASR device as a list
        
        Raises
        ------
        ValueError
            Unable to retrieve location information
        """
        unit = ASR.utils.lengthConversion(units)
        try:
            pos = axis.get_position(zaber_motion.Units[unit])
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
        unit = ASR.utils.lengthConversion(units)
        try:
            axis.move_absolute(target,zaber_motion.Units[unit],wait_until_idle=True)
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
        unit = ASR.utils.lengthConversion(units)
        try:
            axis.move_relative(step,zaber_motion.Units[unit],wait_until_idle=True)
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
            "um": ".LENGTH_MICROMETRES",
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
        def velocityConversion(unit):
            if unit:
                for key, value in ASR.utils.speed_map.items():
                    if unit == key:
                        return value
                else:
                    raise ValueError("Unrecognised units. Try cm/s, mm/s, um/s, or nm/s")
                    
        @staticmethod    
        def lengthConversion(unit):
            if unit:
                for key, value in ASR.utils.length_map.items():
                    if unit == key:
                        return value
                else:
                    raise ValueError("Unrecognised units. Try mm, um, nm, or native")
                
    class Settings:
   
        def __init__(self):
            self._parent = None
            
        def _set_parent(self, parent_instance):
            """Set the parent instance after creation."""
            self._parent = parent_instance
            return self

        
        # def set(self, setting, value):
        #     """
        #     Set a specific ASR setting for the given device.

        #     Parameters
        #     ----------
        #     setting : string
        #         The device setting to be altered
        #     value : string
        #         The value of the device setting to be altered

        #     Returns
        #     -------
        #     None.

        #     """
        #     internal_key = self.settings_map.get(setting)
        #     if not internal_key:
        #         print(f"'{setting}' is not a recognized setting.")
        #         return
        
        #     try:
        #         self.obj.settings.set_string(internal_key, value)
        #         value = self.device.settings.get_string(internal_key)
        #         print(f"{setting}: {value}")
        #     except Exception as e:
        #         print(f"Could not update '{setting}': {e}")
                            
        
        def get(self):
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
            accel = self._parent.zaberdevice.settings.get_from_all_axes("accel")
            temp = self._parent.zaberdevice.settings.get_from_all_axes("driver.temperature")
            knbdir = self._parent.zaberdevice.settings.get_from_all_axes("knob.dir")
            knbmode = self._parent.zaberdevice.settings.get_from_all_axes("knob.mode")
            maxspeed = self._parent.zaberdevice.settings.get_from_all_axes("maxspeed")
            pos = self._parent.zaberdevice.settings.get_from_all_axes("pos")
            
            settings_dict = {
                "accel": accel,
                "driver_temperature": temp,
                "knob_dir": knbdir,
                "knob_mode": knbmode,
                "maxspeed": maxspeed,
                "pos": pos,
            }
            
            return settings_dict


if __name__ == "__main__":
    
    # Instantiation of the ASR object
    with ASR(8) as asr:
        
    # Helps with the settings methods
        asr.settings._set_parent(asr)

    # Query the position of each axis on the connected device
        pos = [asr.getPosition(axis, "mm") for axis in asr.axes]
        
    # Move the device axis in various ways
        asr.moveAbsolute(asr.axis1, 1, "mm")
        asr.moveAbsolute(asr.axis2, 2, "mm")
        asr.moveRelative(asr.axis1, 1, "mm")
        asr.moveRelative(asr.axis2, 2, "mm")
        
    # Recall existing device settings
        devSettings = asr.settings.get()
        
    # Reference the device axes
        for axis in asr.axes:
            asr.home(axis)
    
    
    
        
