
"""

Contains the functions needed for routine use of Vortran devices. It so far has been configured solely for a Vortran Stradus laser diode. The example test code should perform the following routine:
- Connect
- Activate
- Set mode to continuous wave and return confirmation of mode
- Set power to 50 mW and return confirmation of power
- Wait 5 seconds
- Return power to 0mW and return confirmation
- Deactivate
- Disconnect
- 

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
    
    def connect(self):
        """
        Open the laser serial connection

        Returns
        -------
        None.

        """
        try:
            self.connection = serial.Serial(self.port,self.baudrate,timeout=self.timeout)
            print(f"Connected to Vortran device on COM{self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to Vortran device: {e}")
            raise
            
    def disconnect(self):
        """
        Close the laser serial connection

        Returns
        -------
        None.

        """
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected from Vortran device")
        
    def activate(self):
        """
        Turn laser emission ON

        Returns
        -------
        None.

        """
        self.sendCommand("LE=1")
        response = self.sendCommand("?LE")
        print(f"Vortran device ON response: {response}")
        
    def deactivate(self):
        """
        Turn laser emission OFF

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
        response = self.sendCommand("?LI")
        print(f"Device ID: {response}\r")
        response = self.sendCommand("?BPT")
        print(f"Baseplate temperature: {response}\r")
        response = self.sendCommand("?FV")
        print("Firmware version: {response}\r")
        response = self.sendCommand("?LH")
        print("Operating hours: {response}\r")
        response = self.sendCommand("?LS")
        print(f"Settings: {response}\r")
        response = [self.sendCommand("?LP"),self.sendCommand("?LPS")]
        print(f"Measured power: {response[0]} of Set power: {response[1]}\r")
        response = self.sendCommand("?LW")
        print(f"Measured wavelength: {response}nm\r")

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
            raise ValueError("Power percentage must be between 0 and 100")
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
        print(f"Current output power: {response}")
        
    def setMode(self,mode):
        """
        Specify the output type from the Vortran device. Note that external control should be off when using either "CW" or "DIGITAL", so "EPC=0" is called to reset the external control condition but is overwritten should the user require "ANALOG" control. Operating mode returned to the command line for user verification

        Parameters
        ----------
        mode : str
            Emission mode of the device ('CW','DIGITAL','ANALOG')

        Returns
        -------
        None.

        """
        self.sendCommand("EPC=0") # Reset external control
            
        mode_map = {
            "CW": "PUL=0",
            "DIGITAL": "PUL=1",
            "ANALOG": "EPC=1"
        }
        if mode not in mode_map:
            raise ValueError(f"Invalid mode. Supported modes are: {list(mode_map.keys())}")
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
            return "ANALOG"
        elif response == "0":
            response = self.sendCommand("?PUL")
            if response == "0":
                return "CW"
            elif response == "1":
                return "DIGITAL"
            else:
                raise Exception("Unrecognised response to digital modulation query")
        else:
            raise Exception("Unrecognised response to external control query")
            
        
    def sendCommand(self,command):
        """
        Send a command to the laser and return the response

        Parameters
        ----------
        command : str
            Command to send to the device. Format must align with Vortran documentation

        Raises
        ------
        ConnectionError
            The device hasn't been connected properly. Check the serial connection '

        Returns
        -------
        response : str
            The base command return from Vortran devices. Can be interpreted in conjunction with Vortran documentation. This has yet to be verified and may not function as intended

        """
        if not self.connection or not self.connection.is_open:
            raise ConnectionError("Connection to the Vortran device is not open")
        self.connection.write((command+'\r').encode())
        response = self.connection.readline().decode().strip()
        return response
   
        
"""
Example usage.
"""
if __name__ == "__main__":
    laser = Vortran()
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

