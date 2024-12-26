

import zaber_motion
import zaber_motion.ascii
from stage import Stage

class Zaber(Stage):
    """
    Zaber stage, a subclass of Stage
    """

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

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
            print(f"Error connecting to ASR {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.__exit__(None, None, None)
        print("ASR Disconnected")
        super().__exit__(exc_type, exc_value, traceback)

    def getPos(self):
        try:
            pos = [
                self.axis1.get_position(zaber_motion.Units.LENGTH_MICROMETRES),
                self.axis2.get_position(zaber_motion.Units.LENGTH_MICROMETRES)
            ]
        except Exception as e:
            print(f"Cannot retrieve location data: {e}")
            raise
        return pos

    def setPos(self, **kwargs):
        for key, value in kwargs.items():
            if key == "targetX":
                pass
            if key == "targetY":
                pass