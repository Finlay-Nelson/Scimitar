
"""

Polymorphism:
    
Q545 = Q545(model,serial,origin)
ASR = ASR(channel,origin)
   
stages = [Q545, ASR]
for stage in stages:
    with stage:
        print(stage.getPos())
        
The code above means we can define a list of stages and for any overlapping method names, getPos() setPos() etc then we can execute each of these methods using that devices own interpretation of the call even if those interpretations are quite different

What we have here is a way of outlining all of the methods universal across all stage devices, as well as a way of outlining those only applicable to PI or Zaber devices, etc. If nothing else this script can serve as a template around which to introduce new devices


"""

import zaber_motion
import zaber_motion.ascii

from pipython import GCSDevice, pitools
from abc import ABC, abstractmethod

class Stage(ABC):
    """
    Abstract base class for all stages
    """
    @abstractmethod
    def setPos(self, **kwargs):
        """
        Set the position of the stage device

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass
    
    def getPos(self):
        """
        Query the position of the stage device

        Returns
        -------
        None.

        """
        pass
    
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        pass
    
    def __enter__(self):
        """
        Enter the context manager

        Returns
        -------
        None.

        """
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        """
        Exit the context manager

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass
    
class Zaber(Stage):
    """
    Zaber stage, a subclass of Stage
    """
    
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        super().__init__()
        
    def __enter__(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        """
        

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__exit__(exc_type,exc_value,traceback)
        
class PI(Stage):
    """
    PI Stage, a subclass of Stage
    """
    
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        super().__init__*()
        
    def __enter__(self):
        """
        

        Returns
        -------
        None.

        """
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        """
        

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__exit__(exc_type,exc_value,traceback)
        
class ASR(Zaber):
    """
    ASR Stage, a subclass of Zaber.
    """
    
    def __init__(self,channel,origin):
        """
        

        Parameters
        ----------
        channel : TYPE
            DESCRIPTION.
        origin : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__()
        self.channel = f'COM{channel}'
        self.origin = origin
        self.connection = None
        self.zaberdevice = None
        self.axis1 = None
        self.axis2 = None
        
    def __enter__(self):
        """
        Enter the context manager

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        try:
            self.connection = zaber_motion.ascii.Connection.open_serial_port(self.channel)
            self.zaberdevice = self.connection.detect_devices()[0]
            self.axis1 = zaber_motion.ascii.Axis(self.zaberdevice, 1)
            self.axis2 = zaber_motion.ascii.Axis(self.zaberdevice, 2)
            print("ASR Connected")
        except Exception as e:
            print(f"Error connecting to ASR {e}")
            raise
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        """
        Exit the context manager

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if self.connection:
            self.connection.__exit__(None,None,None)
        print("ASR Disconnected")
        super().__exit__(exc_type,exc_value,traceback)
        
    def getPos(self):
        """
        Query the current position of the stage

        Returns
        -------
        pos : TYPE
            DESCRIPTION.

        """
        pos = None
        try:
            
            pos = [self.axis1.get_position(zaber_motion.Units.LENGTH_MICROMETRES),
                   self.axis2.get_position(zaber_motion.Units.LENGTH_MICROMETRES)]
        except Exception as e:
            print(f"Cannot retrieve location data: {e}")
            raise
                
        return pos
    
    def setPos(self,**kwargs):
        """
        Translate the stage to the specified location

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        for key, value in kwargs.items():
            if key == "targetX":
                pass
            if key == "targetY":
                pass
            
class Q545(PI):
    """
    Q545 Piezoelectric stage, a subclass of PI
    """
    
    def __init__(self,model,serial,origin):
        """
        

        Parameters
        ----------
        model : TYPE
            DESCRIPTION.
        serial : TYPE
            DESCRIPTION.
        origin : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__()
        self.model = model
        self.serial = serial
        self.origin = origin
        self.pidevice = None
        
    def __enter__(self):
        """
        Enter the context manager

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        self.pidevice = GCSDevice(self.model)
        try:
            self.pidevice.ConnectUSB(serialnum=self.serial)
        except Exception as e:
            print(f"Error connecting to Q-545: {e}")
            raise
        self._initializeServo()
        print("Q-545 Connected")
        pitools.waitontarget(self.pidevice,1)
        return self
            
    def __exit__(self,exc_type,exc_value,traceback):
        """
        Exit the context manager

        Parameters
        ----------
        exc_type : TYPE
            DESCRIPTION.
        exc_value : TYPE
            DESCRIPTION.
        traceback : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.pidevice.MOV(1,0.0)
        pitools.waitontarget(self.pidevice,1)
        self.pidevice.__exit__(None,None,None)
        print("Q-545 Disconnected")
        super().__exit__(exc_type,exc_value,traceback)
        
    def _initializeServo(self):
        """
        Initialise the servo. Particularly useful where the stage has been turned off and by extension the servo deactivated.

        Returns
        -------
        None.

        """
        servo_status = self.pidevice.read('SVO?')
        if servo_status == str('1=0\n'):
            self.pidevice.SVO(1,1)
            self.pidevice.send('FNL')
        else:
            self.pidevice.MOV(1,0.0)
            
    def setPos(self,**kwargs):
        """
        Translate the stage to a target position.  Travel limits are imposed to within -6.5 and +6.5 mm for this model

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        for key, value in kwargs.items():
            if key == "targetZ":
                if value < -6.5 or value > 6.5:
                    raise ValueError("Target location out of bounds: -6.5 to 6.5mm")
                self.pidevice.MOV(1,value)
                pitools.waitontarget(self.pidevice,1)
                
    def getPos(self):
        """
        Query the stage position

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.pidevice.qPOS(1)[1]
                
        
    
