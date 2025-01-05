
"""
Routine functions for Vortran devices (specifically the Stradus diode). 
"""

import serial
import time

class Vortran:
    
    def __init__(self,port,baudrate=115200,timeout=1):
        """
        Initialize connection to a Vortran laser

        Parameters
        ----------
        port : int
            Serial port (e.g. 'COM3')
        baudrate : int, optional
            Communication speed. The default is 115200.
        timeout : float, optional
            Read timeout in seconds. The default is 1.

        Returns
        -------
        None.

        """
        self.port = f"COM{port}"
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        self.mode = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.disconnect()
        else:
            print("No Vortran device connected")
        if exc_type:
            print(f"An error occurred: {exc_value}")
    
    def connect(self):
        try:
            self.connection = serial.Serial(self.port,self.baudrate,timeout=self.timeout)
            print(f"Connected to Vortran device on COM{self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to Vortran device: {e}")
            
    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected from Vortran device")
        
    def activate(self):
        """
        Turn ON laser emission

        Returns
        -------
        None.

        """
        self.sendCommand("LE=1")
        response = self.sendCommand("?LE")
        print(f"Vortran device ON response: {response}")
        
    def deactivate(self):
        """
        Turn OFF laser emission

        Returns
        -------
        None.

        """
        self.sendCommand("LE=0")
        response = self.sendCommand("?LE")
        print(f"Vortran device OFF response: {response}")
        
    def getConditions(self):
        """
        Return laser operating conditions
        
        Returns
        -------
        None.

        """
        
        settings = {"Device ID": "?LI",
                    "Firmware version": "?FV",
                    "Baseplate temperature": "?LH",
                    "Operating hours": "?LH",
                    "Settings": "?LS",
                    "Measured power": "?LP",
                    "Set power": "?LPS",
                    "Measured wavelength": "?LW"}
        for key,command in settings.items():
            response = self.sendCommand(command)
            print(f"{key}: {response}\r")
        
    def setPower(self,power):
        """
        Set the laser output power. Prints output power to the command line

        Parameters
        ----------
        power : float
            Desired output power [mW]. In range 0 <= power <= 100

        Returns
        -------
        None.

        """
        if not (0 <= power <= 100):
            ValueError("Power percentage must be between 0 and 100")
        self.sendCommand(f"LP={power}")
        self.getPower
        
    def getPower(self):
        """
        Query the current device output power. Returns the laser power measured
by the light loop.

        Returns
        -------
        None.

        """
        response = self.sendCommand("?LP")
        print(f"Measured output power: {response}")
        
    def setMode(self,mode):
        """
        Specify the output type from the Vortran device. Note that external control should be off when using either "CW" or "DIGITAL", so "EPC=0" is called to reset the external control condition but is overwritten should the user require "ANALOG" control. Operating mode returned to the command line for user verification

        Parameters
        ----------
        mode : string
            Emission mode of the device ('CW','DIGITAL','ANALOG')

        Returns
        -------
        None.

        """
        # Reset external control
        self.sendCommand("EPC=0")
            
        mode_map = {
            "CW": "PUL=0",
            "DIGITAL": "PUL=1",
            "ANALOG": "EPC=1"
        }
        if mode not in mode_map:
            ValueError(f"Invalid mode. Supported modes are: {list(mode_map.keys())}")
        self.sendCommand(mode_map[mode])
        response = self.getMode()
        print(f"Output mode: {response}")
        
    def getMode(self):
        """
        Query the current output mode of the Vortran device

        Raises
        ------
        Exception
            Unrecognised response to digital modulation query (?PUL)
            Unrecognised response to external control query (?EPC)

        Returns
        -------
        str
            Output mode (CW, DIGITAL, ANALOG)

        """
        response = self.sendCommand("?EPC")
        if response == "1":
            self.mode = "ANALOG"
        elif response == "0":
            response = self.sendCommand("?PUL")
            if response == "0":
                self.mode = "CW"
            elif response == "1":
                self.mode = "DIGITAL"
            else:
                Exception("Unrecognised response to digital modulation query")
        else:
            Exception("Unrecognised response to external control query")
        return self.mode
            
        
    def sendCommand(self,command):
        """
        Send a command to the laser and return the response

        Parameters
        ----------
        command : string
            Command to send to the device. Format must align with Vortran documentation

        Raises
        ------
        ConnectionError
            The device hasn't been connected properly. Check the serial connection '

        Returns
        -------
        response : string
            The base command return from Vortran devices. Can be interpreted in conjunction with Vortran documentation. This has yet to be verified and may not function as intended

        """
        if not self.connection or not self.connection.is_open:
            ConnectionError("Connection to the Vortran device is not open")
            return
        self.connection.write((command+'\r').encode())
        response = self.connection.readline().decode().strip()
        return response
   
        
"""
Example usage.
"""
if __name__ == "__main__":
    laser = Vortran(3)
    try:
        laser.connect()
        laser.activate()
        laser.getConditions()
        laser.setMode("CW")
        laser.setPower(50)
        time.sleep(5)
        laser.setPower(0)
        laser.deactivate()
    finally:
        laser.disconnect()
    
        
        
        
            
        
        
        
        
        
        
        
        
        
        
        

