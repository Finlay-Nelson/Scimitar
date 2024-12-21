"""
Created on Sat Sep 28 10:09:32 2024

Controls stage devices
- Zaber: ASR100B120B-T3A / A-MCB2 (controller)
- Physike Instrumente: Q-545.140 Q-Motion / E-873 (controller)

"""
###############################################################################

# devices/stages.py
import zaber_motion
import zaber_motion.ascii
import time

from pipython import GCSDevice, pitools
from abc import ABC, abstractmethod

###############################################################################

class Stage(ABC):
    """
    Abstract base class for all stages.
    """
    @abstractmethod
    def setPos(self, **kwargs):
        """Set the position of the stage."""
        pass
    
    @abstractmethod
    def getPos(self):
        """Get the current position of the stage."""
        pass
    
    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager."""
        pass


class Zaber(Stage):
    """
    Zaber Stage, a subclass of Stage.
    """
    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)


class PI(Stage):
    """
    PI Stage, a subclass of Stage.
    """
    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

###############################################################################

class ASR(Zaber):
    """
    ASR Stage, a subclass of Zaber.
    """
    def __init__(self, channel, origin):
        super().__init__()
        self.channel = f'COM{channel}'
        self.origin = origin
        self.connection = None
        self.zaberdevice = None
        self.axis1 = None
        self.axis2 = None
        
    def __enter__(self):
        try:
            self.connection = zaber_motion.ascii.Connection.open_serial_port(self.channel)
            self.zaberdevice = self.connection.detect_devices()[0]
            self.axis1 = zaber_motion.ascii.Axis(self.zaberdevice, 1)  
            self.axis2 = zaber_motion.ascii.Axis(self.zaberdevice, 2)  
            print("ASR Connected")
        except Exception as e:
            print(f"Error connecting to ASR: {e}")
            raise
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.__exit__(None, None, None)
        print("ASR Disconnected")
        time.sleep(0.1)
        super().__exit__(exc_type, exc_value, traceback)
        
    def setPos(self, **kwargs):
        """
        Move the stage to the specified position.
        """
        for key, value in kwargs.items():
            if key == "targetX":
                self.axis1.move_absolute(value, zaber_motion.Units.NATIVE, True)
            if key == "targetY":
                self.axis2.move_absolute(value, zaber_motion.Units.NATIVE, True)
                
    def getPos(self):
        """
        Get the current position of the stage.
        """
        pos = [
            self.axis1.get_position(zaber_motion.Units.LENGTH_MICROMETRES),
            self.axis2.get_position(zaber_motion.Units.LENGTH_MICROMETRES)
        ]
        return pos

###############################################################################

class Q545(PI):
    """
    Q545 Piezoelectric Stage, a subclass of PI.
    """
    def __init__(self, model, serial, origin):
        super().__init__()
        self.model = model
        self.serial = serial
        self.origin = origin
        self.pidevice = None
        
    def __enter__(self):
        self.pidevice = GCSDevice(self.model)
        try:
            self.pidevice.ConnectUSB(serialnum=self.serial)
        except Exception as e:
            print(f"Error connecting to Q-545: {e}")
            raise
        self._initialize_servo()
        print('Q-545 Connected')
        pitools.waitontarget(self.pidevice, 1)
        time.sleep(0.1)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.pidevice.MOV(1, 0.0)
        pitools.waitontarget(self.pidevice, 1)
        self.pidevice.__exit__(None, None, None)
        print('Q-545 Disconnected')
        time.sleep(0.1)
        super().__exit__(exc_type, exc_value, traceback)
    
    def _initialize_servo(self):
        """
        Initialize the servo status.
        """
        servo_status = self.pidevice.read('SVO?')
        if servo_status == str('1=0\n'):
            self.pidevice.SVO(1, 1)
            self.pidevice.send('FNL')
        else:
            self.pidevice.MOV(1, 0.0)
            
    def setPos(self, **kwargs):
        """
        Move the piezoelectric stage to the specified position.
        """
        for key, value in kwargs.items():
            if key == "targetZ":
                if value < -6.5 or value > 6.5:
                    raise ValueError("Target location exceeds travel range (-6.5 to 6.5 mm).")
                self.pidevice.MOV(1, value)
                pitools.waitontarget(self.pidevice, 1)

    def getPos(self):
         """
         Get the current position of the piezoelectric stage.
         """
         return self.pidevice.qPOS(1)[1]
###############################################################################
