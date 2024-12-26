
from pipython import GCSDevice, pitools
from stage import Stage

class PI(Stage):
    """
    PI Stage, a subclass of Stage
    """

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

class Q545(PI):
    """
    Q545 Piezoelectric stage, a subclass of PI
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
        self._initializeServo()
        print("Q-545 Connected")
        pitools.waitontarget(self.pidevice, 1)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pidevice.MOV(1, 0.0)
        pitools.waitontarget(self.pidevice, 1)
        self.pidevice.__exit__(None, None, None)
        print("Q-545 Disconnected")
        super().__exit__(exc_type, exc_value, traceback)

    def _initializeServo(self):
        servo_status = self.pidevice.read('SVO?')
        if servo_status == str('1=0\n'):
            self.pidevice.SVO(1, 1)
            self.pidevice.send('FNL')
        else:
            self.pidevice.MOV(1, 0.0)

    def setPos(self, **kwargs):
        for key, value in kwargs.items():
            if key == "targetZ":
                if value < -6.5 or value > 6.5:
                    raise ValueError("Target location out of bounds: -6.5 to 6.5mm")
                self.pidevice.MOV(1, value)
                pitools.waitontarget(self.pidevice, 1)

    def getPos(self):
        return self.pidevice.qPOS(1)[1]