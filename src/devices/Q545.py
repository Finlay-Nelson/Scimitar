
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
        self.UpperLim = 6.5
        self.LowerLim = -6.5
        self.home = 0.0

    def __enter__(self):
        self.pidevice = GCSDevice(self.model)
        try:
            self.pidevice.ConnectUSB(serialnum=self.serial)
            print("Q-545 Connected")
            while True:
                if not self.isReferenced():
                    prompt = input("Confirm the piezo is safe to reference? (y/n)")
                    if prompt == "y":
                        self.refernce()
                        print("Q-545 Referenced")
                    elif prompt == "n":
                        self.__exit__(None,None,None)
                        break
                    else:
                        ValueError("Unrecognised input. Specify y or n") 
                        raise
                else:
                    break
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
        
    def isReferenced(self):
        servo_status = self.pidevice.read('SVO?')
        return servo_status

    def reference(self):
        self.pidevice.SVO(1, 1)
        self.pidevice.send('FNL')
    
    def move_absolute(self, target):
        if target < self.LowerLim or target > self.UpperLim:
            raise ValueError("Target location out of bounds: -6.5 to 6.5mm")
        try:
            self.pidevice.MOV(1, target)
            pitools.waitontarget(self.pidevice, 1)
            pos = self.get_position()
            print(f"PI Position: {pos}")
        except Exception as e:
            print(e)
    def move_relative(self, step):
            pos = self.get_position()
            if pos + step < self.LowerLim or pos + step > self.UpperLim:
                raise ValueError("Specified travel would move stage out of range")
            else:
                try:
                    self.pidevice.MVR(1,step)
                    pitools.waitontarget(self.pidevice, 1)
                    pos = self.get_position()
                    print(f"PI Position: {pos}")
                except Exception as e:
                    print(e)

    def get_position(self):
        return self.pidevice.qPOS(1)[1]
    
if __name__ == "__main__":
    with Q545() as Q545:
        Q545.move_absolute(0.0)
        Q545.move_relative(1.0)
