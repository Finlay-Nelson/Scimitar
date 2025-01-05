
from pipython import GCSDevice, pitools

class Q545():
    """
    Physike Instrumente Q545 Piezoelectric stage
    """

    def __init__(self, model="E-873", serial="121007658"):
        """
        

        Parameters
        ----------
        model : string
            "E-873"
        serial : string
            "121007658"

        Returns
        -------
        None.

        """
        self.model = model
        self.serial = serial
        self.pidevice = None

    def __enter__(self):
        self.pidevice = GCSDevice(self.model)
        try:
            self.pidevice.ConnectUSB(serialnum=self.serial)
            print("Q-545 Connected")
            while True:
                if not self.isHomed():
                    prompt = input("Confirm the piezo is safe to home? (y/n)")
                    if prompt == "y":
                        self.home()
                        print("Q-545 Homed")
                    elif prompt == "n":
                        self.__exit__(None,None,None)
                        break
                    else:
                        ValueError("Unrecognised input. Specify y or n") 
                        raise
        except Exception as e:
            print(f"Error connecting to Q-545: {e}")
            raise
        pitools.waitontarget(self.pidevice, 1)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An error occurred: {exc_value}")
        self.pidevice.MOV(1, 0.0)
        pitools.waitontarget(self.pidevice, 1)
        self.pidevice.__exit__(None, None, None)
        print("Q-545 Disconnected")
        
    def isHomed(self):
        servo_status = self.pidevice.read('SVO?')
        return servo_status

    def home(self):
        self.pidevice.SVO(1, 1)
        self.pidevice.send('FNL')
    
    def setPos(self, target):
        if target < -6.5 or target > 6.5:
            raise ValueError("Target location out of bounds: -6.5 to 6.5mm")
        try:
            self.pidevice.MOV(1, target)
            pitools.waitontarget(self.pidevice, 1)
            pos = self.getPos()
            print(pos)
        except Exception as e:
            print(e)

    def getPos(self):
        return self.pidevice.qPOS(1)[1]
    
if __name__ == "__main__":
    Q545 = Q545()
    Q545.setPos(0)
    Q545.pidevice._settings.keys()
    