"""
The ASR120B100B driver has 2 dials controlling axes 1 and 2 respectively. 
- Holding either dial for 5 seconds during power-up performs a factory reset.
- Pressing and holding a dial for 1 second toggles between displacement and velocity control modes.
- In velocity mode, turning the dial adjusts speed according to its velocity profile
- Pressing a dial stops travel along the corresponding axis.
"""

import zaber_motion

from zaber_motion.ascii import Connection
from zaber_motion.ascii import Axis

class ASR:
    """
    Class to manage connection, control, and settings of the ASR120B100B device.
    """

    def __init__(self, port):
        """
        Initialize the ASR device.

        Parameters
        ----------
        port : int
            The COM port for the ASR device connection.
        """
        self.port = f"COM{port}"
        self.zaberdevice = None
        self.connection = None
        self.axes = []
        self.settings = self.Settings(self)
        
    def __enter__(self):
        """
        Establish connection and initialize the ASR device.
        """
        try:
            self.connection = Connection.open_serial_port(self.port)
            self.zaberdevice = self.connection.detect_devices()[0]
            print("ASR Connected")
    
            axis_count = self.zaberdevice.axis_count
            for ax in range(axis_count):
                axis_name = f"axis{ax + 1}"
                axis_instance = Axis(self.zaberdevice, ax + 1)
                setattr(self, axis_name, axis_instance)
                axis = getattr(self, axis_name)
                axis.name = axis_name
                self.axes.append(axis)
    
            print(f"ASR axes initialized: {[axis.name for axis in self.axes]}")
    
            if not self.zaberdevice.all_axes.is_homed():
                self._confirm_and_home_axes()
    
        except Exception as e:
            raise ConnectionError(f"Couldn't connect to ASR: {e}")
    
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the connection to the ASR device.
        """
        if self.connection:
            try:
                self.connection.__exit__(None, None, None)
                print("ASR Disconnected")
            except Exception as e:
                raise ConnectionError(f"Couldn't disconnect from ASR: {e}")
                
    def home(self, axis):
       """
       Home the specified axis.

       Parameters
       ----------
       axis : zaber_motion.ascii.Axis
           The axis to home.
       """
       try:
           axis.home(wait_until_idle=True)
           print(f"ASR homed: {axis.name}")
       except Exception as e:
           print(f"ASR couldn't home {axis.name}: {e}")
           
    def get_position(self, axis, units):
        """
        Get the position of a specified axis.

        Parameters
        ----------
        axis : zaber_motion.ascii.Axis
            The axis to query.
        units : str
            Unit of measurement (mm, um, nm, or native).

        Returns
        -------
        float
            The position of the axis.
        """
        unit = ASR.utils.length_conversion(units)
        try:
            return axis.get_position(zaber_motion.Units[unit])
        except Exception as e:
            raise ValueError(f"Failed to retrieve position for {axis.name}: {e}")
            
    def move_absolute(self, targets, units):
        """
        Move axes to absolute positions.

        Parameters
        ----------
        targets : list of float
            Target positions for each axis.
        units : str
            Unit of measurement for the targets (mm, um, nm, or native).
        """
        if len(targets) != len(self.axes):
            raise ValueError("Number of targets does not match number of axes.")
        
        unit = ASR.utils.length_conversion(units)
        for axis, target in zip(self.axes, targets):
            try:
                axis.move_absolute(target, zaber_motion.Units[unit])
                print(f"Moved {axis.name} to {target} {units}.")
            except Exception as e:
                print(f"Failed to move {axis.name}: {e}")
            
    def move_relative(self, steps, units):
        """
        Move axes by relative distances.

        Parameters
        ----------
        steps : list of float
            Distances to move for each axis.
        units : str
            Unit of measurement for the steps (mm, um, nm, or native).
        """
        if len(steps) != len(self.axes):
            raise ValueError("Number of steps does not match number of axes.")
        
        unit = ASR.utils.length_conversion(units)
        for axis, step in zip(self.axes, steps):
            try:
                axis.move_relative(step, zaber_motion.Units[unit])
                print(f"Moved {axis.name} by {step} {units}.")
            except Exception as e:
                print(f"Failed to move {axis.name}: {e}")
                
    def _confirm_and_home_axes(self):
        """
        Confirm and home all axes if required.
        """
        prompt = input("Confirm the microscope is safe to home? (y/n): ").lower()
        if prompt == "y":
            for axis in self.axes:
                if not axis.is_homed():
                    self.home(axis)
        elif prompt == "n":
            self.__exit__(None, None, None)
        else:
            raise ValueError("Unrecognized input. Specify 'y' or 'n'.")
            
    class utils:
        """
        Utility class for unit conversions.
        """

        length_map = {
            "mm": "LENGTH_MILLIMETRES",
            "um": "LENGTH_MICROMETRES",
            "nm": "LENGTH_NANOMETRES",
            "native": "NATIVE"
        }

        @staticmethod
        def length_conversion(unit):
            """
            Convert human-readable length units to internal representation.

            Parameters
            ----------
            unit : str
                Human-readable unit.

            Returns
            -------
            str
                Internal unit representation.
            """
            return ASR.utils.length_map.get(unit, None) or ValueError("Invalid unit.")
        
    class Settings:
        """
        Class to handle device settings.
        """

        def __init__(self, parent):
            self._parent = parent

        def set(self, setting, values):
            """
            Set a device setting for all axes.

            Parameters
            ----------
            setting : str
                The setting to modify.
            values : list
                Values for each axis.
            """
            if len(values) != len(self._parent.axes):
                print("Value count does not match axis count.")
                return
            
            for axis, value in zip(self._parent.axes, values):
                try:
                    axis.settings.set(setting, value)
                    print(f"Set {setting} for {axis.name}.")
                except Exception as e:
                    print(f"Failed to set {setting} for {axis.name}: {e}")

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
            a_const = 0.15625e1/1.6348**2
            v_const = 0.15625e-3/1.6348
            
        
            return {
                "accel": [axis.settings.get("accel")*a_const for axis in self._parent.axes],
                "drive_temp": [axis.settings.get("driver.temperature") for axis in self._parent.axes],
                "knob_dir": [axis.settings.get("knob.dir") for axis in self._parent.axes],
                "knob_mode": [axis.settings.get("knob.mode") for axis in self._parent.axes],
                "maxspeed": [axis.settings.get("maxspeed")*v_const for axis in self._parent.axes]
                }
            

if __name__ == "__main__":
    
    a_const = 0.15625e1/1.6348**2
    v_const = 0.15625e-3/1.6348
    
    with ASR(8) as asr:
        asr.settings.set("accel",[60/a_const,60/a_const])
        asr.settings.set("maxspeed", [10/v_const, 10/v_const])
        asr.move_relative([5, 10], "mm")
        for axis in asr.axes:
            asr.home(axis)
